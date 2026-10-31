# Security policy

## Reporting a vulnerability

Report privately. Do not open a public issue, pull request or discussion about it.

1. GitHub: open this repository's Security tab and choose "Report a vulnerability". This
   creates a private advisory that only the maintainers can see. If that option is not shown,
   private vulnerability reporting has not been enabled for this repository yet; use email.
2. Email: drake@aienos.com with the subject `[atlas] security report`.

Include the commit or release you tested, the component (path), steps to reproduce, and what an
attacker gains. If the report involves a secret, say where it was exposed and do not send the
secret itself. Encrypted mail is not required; do not post proof-of-concept payloads publicly.

## Response targets

This project has one maintainer; the targets below are best effort and stated honestly.

- Acknowledgement: within 3 working days.
- Triage and severity: within 7 days of acknowledgement.
- Fix or mitigation for confirmed issues: aim for 30 days for high and critical, 90 days
  otherwise, with a status update at least every 14 days until closed.
- Disclosure: coordinated. An advisory is published with credit (unless you ask otherwise)
  once the fix is on the default branch. Default embargo 90 days, negotiable.

## Scope

Atlas is a 1,480-byte AArch64 boot seed (`atlas.bin`) that checks the next boot stage against a
pinned SHA-256 digest, hands control to it, and refuses and halts if the check fails.

In scope:

- Any input to `atlas.bin` that makes it hand off to a payload whose SHA-256 is not the pinned
  digest, or that lets it run past the fail-closed halt (`wfe; b .`).
- A flaw in `sha256_clean.c` or `sha256_clean.s` that produces a wrong digest.
- A stack or descriptor overlap that contradicts `atlas.memory-map`.
- A way for `run_m1_gates.sh` or `tools/m1tool.c` to report a gate as passed when it failed, to
  interpret an artifact path as shell, or to write outside its private temporary directory.

Out of scope:

- The next-stage boot artifacts, which live in `aien-dev/physics`.
- `history/alpha/` (historical record only; no gate reads it).
- QEMU, gcc, binutils and the host operating system.

## Supported versions

Only the default branch `master`; there is no release. Reports against older commits are welcome but fixes land on the default branch only.

## Status

Milestone 1 is qualified in QEMU only; native DGX Spark qualification is pending and has no runner
in this repository (AGENTS.md). No certification, no bug bounty. See AUDIT_SCOPE.md for what to review and how to build and test it.
