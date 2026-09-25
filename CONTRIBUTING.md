# Engineering Workflow

## One task, one branch, one pull request

1. Start from an accepted Task Issue.
2. Update local `main`.
3. Create a short-lived branch using `<type>/<issue-id>-<slug>`.
4. Implement the smallest complete change.
5. Run `make check`.
6. Open a pull request and link the Task Issue.
7. Preserve verification evidence in the pull request or `docs/evidence/`.
8. Run `make merge PR=<number>` after all checks pass.
9. Delete the source branch.

Allowed branch types:

- `feat`
- `fix`
- `refactor`
- `test`
- `docs`
- `ops`
- `chore`

## Local quality gate

Run:

```bash
make check
```

This command checks lint, formatting, types, and tests. Add migration,
integration, contract, container, and deployment checks as those capabilities
enter the project.

## Zero-cost merge guard

GitHub Free private repositories do not include every native branch-protection
feature. The included merge guard verifies that a pull request targets `main`,
is open, is not a draft, is mergeable, is current, and has passing CI checks.
It then squash-merges the exact verified head commit and deletes the branch.

Authenticate GitHub CLI, verify a pull request without merging, then merge:

```bash
gh auth login
make merge PR=123 DRY_RUN=1
make merge PR=123
```

Preserve the pull-request URL, Actions URL, and merge commit in
`docs/evidence/ledger.md`.

## Data and secrets

- Use synthetic restaurant and customer data.
- Never commit `.env`, credentials, access tokens, private keys, or real PII.
- Keep hosted model adapters optional.
- Keep deterministic tests independent from hosted model availability.
