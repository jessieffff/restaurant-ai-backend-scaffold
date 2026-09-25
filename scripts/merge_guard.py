from __future__ import annotations

import argparse
import json
import subprocess
from collections.abc import Sequence, Set
from typing import TypedDict, cast


class PullRequest(TypedDict):
    baseRefName: str
    headRefOid: str
    isDraft: bool
    mergeable: str
    mergeStateStatus: str
    number: int
    state: str
    url: str


class Check(TypedDict):
    bucket: str
    link: str
    name: str


class MergeCommit(TypedDict):
    oid: str


class MergedPullRequest(TypedDict):
    mergeCommit: MergeCommit | None
    url: str


def run_gh_json(
    arguments: Sequence[str],
    allowed_exit_codes: Set[int] = frozenset({0}),
) -> object:
    result = subprocess.run(
        ["gh", *arguments],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode not in allowed_exit_codes:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown GitHub CLI error"
        raise RuntimeError(detail)

    try:
        payload: object = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError("GitHub CLI returned invalid JSON.") from error
    return payload


def validate_pull_request(pull_request: PullRequest, checks: Sequence[Check]) -> list[str]:
    errors: list[str] = []

    if pull_request["state"] != "OPEN":
        errors.append("Pull request is not open.")
    if pull_request["baseRefName"] != "main":
        errors.append("Pull request must target main.")
    if pull_request["isDraft"]:
        errors.append("Pull request is still a draft.")
    if pull_request["mergeable"] != "MERGEABLE":
        errors.append(f"Pull request is not mergeable: {pull_request['mergeable']}.")
    if pull_request["mergeStateStatus"] != "CLEAN":
        errors.append(
            "Pull request is not current and clean: "
            f"{pull_request['mergeStateStatus']}. Update the branch and rerun checks."
        )
    if not checks:
        errors.append("No CI checks were found.")

    for check in checks:
        if check["bucket"].lower() != "pass":
            errors.append(f"Check '{check['name']}' is {check['bucket']}.")

    return errors


def merge_pull_request(pr_number: int, dry_run: bool) -> int:
    pull_request = cast(
        PullRequest,
        run_gh_json(
            [
                "pr",
                "view",
                str(pr_number),
                "--json",
                "baseRefName,headRefOid,isDraft,mergeable,mergeStateStatus,number,state,url",
            ]
        ),
    )
    checks = cast(
        list[Check],
        run_gh_json(
            ["pr", "checks", str(pr_number), "--json", "bucket,link,name"],
            allowed_exit_codes=frozenset({0, 1, 8}),
        ),
    )

    errors = validate_pull_request(pull_request, checks)
    if errors:
        print(f"Merge guard rejected {pull_request['url']}:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Merge guard passed {pull_request['url']}.")
    for check in checks:
        print(f"- {check['name']}: {check['link']}")

    if dry_run:
        print("Dry run complete; no merge was performed.")
        return 0

    subprocess.run(
        [
            "gh",
            "pr",
            "merge",
            str(pr_number),
            "--squash",
            "--delete-branch",
            "--match-head-commit",
            pull_request["headRefOid"],
        ],
        check=True,
    )
    merged_pull_request = cast(
        MergedPullRequest,
        run_gh_json(["pr", "view", str(pr_number), "--json", "mergeCommit,url"]),
    )
    merge_commit = merged_pull_request["mergeCommit"]
    merge_oid = merge_commit["oid"] if merge_commit is not None else "unavailable"
    print(f"Merged {merged_pull_request['url']} at {merge_oid}.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify CI and pull-request state before squash-merging into main."
    )
    parser.add_argument("pr", type=int, help="Pull-request number")
    parser.add_argument("--dry-run", action="store_true", help="Verify without merging")
    arguments = parser.parse_args()
    try:
        return merge_pull_request(
            pr_number=cast(int, arguments.pr),
            dry_run=cast(bool, arguments.dry_run),
        )
    except FileNotFoundError:
        print("GitHub CLI is required. Install gh and run 'gh auth login'.")
        return 2
    except (RuntimeError, subprocess.CalledProcessError) as error:
        print(f"Merge guard failed: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
