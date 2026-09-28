# CLI configuration reference

Setup 只管理少量可明确归属的用户级配置，默认是 status line。

## General

- Existing user configuration wins.
- Missing config may be proposed.
- Backup before write.
- Parse, merge, validate; never replace a whole config just to add one key.
- Secrets are out of scope.
- Managed / organization policy wins over user preferences.

## Codex

User config: `~/.codex/config.toml`.

Codex currently supports a native TUI footer configured under `[tui].status_line`. Prefer native status-line items over an external renderer.

Because item names evolve, check the installed client / current schema before writing. If a recommended item is unavailable, omit it.

## Claude Code

User config: `~/.claude/settings.json`.

Claude Code statusLine is command-based. The bundled renderer reads JSON from stdin and prints one line. It intentionally tolerates absent optional fields and does not access credentials.

If the user already has a `statusLine`, do not replace it automatically.
