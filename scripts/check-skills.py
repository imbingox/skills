#!/usr/bin/env python3
"""Check the curated skill surface and bundled references without network access."""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {'grill-with-docs', 'to-spec', 'implement'}
errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding='utf-8')
    except (OSError, UnicodeError) as exc:
        errors.append(f'{path.relative_to(ROOT)}: {exc}')
        return ''


skills = sorted((ROOT / 'skills').rglob('SKILL.md'))
require({p.parent.name for p in skills} == EXPECTED and len(skills) == 3,
        'Exactly the three curated skill entries must be discoverable')

for path in skills:
    text = read(path)
    parts = text.split('---', 2)
    require(len(parts) == 3 and parts[0] == '', f'{path}: invalid frontmatter')
    front = parts[1] if len(parts) == 3 else ''
    require(f'name: {path.parent.name}\n' in front, f'{path}: name mismatch')
    require('disable-model-invocation: true' in front, f'{path}: implicit invocation enabled')
    description = re.search(r'^description: (.+)$', front, re.MULTILINE)
    try:
        require(description is not None and bool(json.loads(description.group(1))),
                f'{path}: missing quoted description')
    except (ValueError, AttributeError):
        errors.append(f'{path}: invalid description')
    policy = read(path.parent / 'agents/openai.yaml')
    require(policy.strip() == 'policy:\n  allow_implicit_invocation: false',
            f'{path}: explicit-invocation policy missing')
    for doc in path.parent.rglob('*.md'):
        body = re.sub(r'```.*?```', '', read(doc), flags=re.DOTALL)
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', body):
            if urlparse(target).scheme or target.startswith('#'):
                continue
            resolved = (doc.parent / unquote(target.split('#')[0])).resolve()
            require(resolved.is_relative_to(path.parent.resolve()),
                    f'{doc}: reference escapes standalone skill package: {target}')
            require(resolved.exists(), f'{doc}: missing bundled reference: {target}')

try:
    plugin = json.loads(read(ROOT / '.claude-plugin/plugin.json'))
    marketplace = json.loads(read(ROOT / '.claude-plugin/marketplace.json'))
    paths = [f'./skills/engineering/{name}' for name in EXPECTED]
    require(sorted(plugin['skills']) == sorted(paths), 'Plugin skill list differs from curated set')
    require(plugin['name'] == 'bingo-skills', 'Fork plugin identity is incorrect')
    require(marketplace['plugins'][0]['name'] == plugin['name'], 'Marketplace/plugin mismatch')
    require(marketplace['plugins'][0]['source'] == './', 'Marketplace must target this fork')
except (ValueError, KeyError, IndexError, TypeError) as exc:
    errors.append(f'Invalid plugin manifest: {exc}')

for doc in [ROOT / 'README.md', ROOT / 'CLAUDE.md', ROOT / 'skills/engineering/README.md',
            *sorted((ROOT / 'docs').rglob('*.md'))]:
    body = re.sub(r'```.*?```', '', read(doc), flags=re.DOTALL)
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', body):
        if urlparse(target).scheme or target.startswith('#'):
            continue
        require((doc.parent / unquote(target.split('#')[0])).exists(),
                f'{doc}: broken documentation link: {target}')

for name in EXPECTED:
    require((ROOT / f'docs/engineering/{name}.md').exists(), f'Missing docs for {name}')

if errors:
    print('\n'.join(f'ERROR: {error}' for error in errors), file=sys.stderr)
    raise SystemExit(1)
print('PASS: 3 skill entries, explicit invocation, standalone references, manifests and docs')
print('Static checks only; agent behavior and live installation are not exercised.')
