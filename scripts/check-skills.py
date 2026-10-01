#!/usr/bin/env python3
"""Check the curated skill surface and repository references without network access."""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
MANUAL = {'setup', 'grill', 'to-spec', 'implement', 'fast-implement', 'finish', 'diagnosing-bugs'}
AUTOMATIC = {'writing-for-agents'}
EXPECTED = MANUAL | AUTOMATIC
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
require({p.parent.name for p in skills} == EXPECTED and len(skills) == len(EXPECTED),
        'Exactly the curated skill entries must be discoverable')

for path in skills:
    require(path.parent.parent == ROOT / 'skills', f'{path}: skill must be directly under skills/')
    text = read(path)
    parts = text.split('---', 2)
    require(len(parts) == 3 and parts[0] == '', f'{path}: invalid frontmatter')
    front = parts[1] if len(parts) == 3 else ''
    require(f'name: {path.parent.name}\n' in front, f'{path}: name mismatch')
    automatic = path.parent.name in AUTOMATIC
    invocation = re.findall(r'^disable-model-invocation:\s*(.*?)\s*$', front, re.MULTILINE)
    require(invocation == ([] if automatic else ['true']),
            f'{path}: incorrect Claude invocation policy')
    description = re.search(r'^description: (.+)$', front, re.MULTILINE)
    try:
        require(description is not None and bool(json.loads(description.group(1))),
                f'{path}: missing quoted description')
    except (ValueError, AttributeError):
        errors.append(f'{path}: invalid description')
    policy = read(path.parent / 'agents/openai.yaml')
    expected_policy = 'true' if automatic else 'false'
    require(policy.strip() == f'policy:\n  allow_implicit_invocation: {expected_policy}',
            f'{path}: incorrect Codex invocation policy')
    for doc in path.parent.rglob('*.md'):
        body = re.sub(r'```.*?```', '', read(doc), flags=re.DOTALL)
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', body):
            if urlparse(target).scheme or target.startswith('#'):
                continue
            resolved = (doc.parent / unquote(target.split('#')[0])).resolve()
            require(resolved.is_relative_to(ROOT.resolve()),
                    f'{doc}: reference escapes repository: {target}')
            require(resolved.exists(), f'{doc}: missing reference: {target}')

try:
    plugin = json.loads(read(ROOT / '.claude-plugin/plugin.json'))
    marketplace = json.loads(read(ROOT / '.claude-plugin/marketplace.json'))
    paths = [f'./skills/{name}' for name in EXPECTED]
    require(sorted(plugin['skills']) == sorted(paths), 'Plugin skill list differs from curated set')
    require(plugin['name'] == 'bingo-skills', 'Plugin identity is incorrect')
    require(plugin['repository'] == 'https://github.com/imbingox/skills',
            'Plugin repository must target this repository')
    require(re.fullmatch(r'\d+\.\d+\.\d+', plugin['version']) is not None,
            'Plugin version must use major.minor.patch')
    require(marketplace['plugins'][0]['name'] == plugin['name'], 'Marketplace/plugin mismatch')
    require(marketplace['plugins'][0]['source'] == './', 'Marketplace must target this repository')
except (ValueError, KeyError, IndexError, TypeError) as exc:
    errors.append(f'Invalid plugin manifest: {exc}')

readme = read(ROOT / 'README.md')
require(set(re.findall(r'\(skills/([\w-]+)/SKILL\.md\)', readme)) == EXPECTED,
        'README entry table differs from curated set')
require(set(re.findall(r'--skill ([\w-]+)', readme)) == EXPECTED,
        'README install command differs from curated set')

for doc in [ROOT / 'README.md', ROOT / 'AGENTS.md', ROOT / 'CONTEXT.md']:
    body = re.sub(r'```.*?```', '', read(doc), flags=re.DOTALL)
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', body):
        if urlparse(target).scheme or target.startswith('#'):
            continue
        require((doc.parent / unquote(target.split('#')[0])).exists(),
                f'{doc}: broken documentation link: {target}')

if errors:
    print('\n'.join(f'ERROR: {error}' for error in errors), file=sys.stderr)
    raise SystemExit(1)
print(f'PASS: {len(EXPECTED)} skill entries, invocation policies, repository references, manifests, README and docs')
print('Static checks only; agent behavior and live installation are not exercised.')
