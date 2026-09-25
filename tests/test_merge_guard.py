from scripts.merge_guard import Check, PullRequest, validate_pull_request


def valid_pull_request() -> PullRequest:
    return {
        "baseRefName": "main",
        "headRefOid": "abc123",
        "isDraft": False,
        "mergeable": "MERGEABLE",
        "mergeStateStatus": "CLEAN",
        "number": 12,
        "state": "OPEN",
        "url": "https://github.com/example/repository/pull/12",
    }


def test_merge_guard_accepts_clean_pull_request() -> None:
    checks: list[Check] = [
        {
            "bucket": "pass",
            "link": "https://github.com/example/repository/actions/runs/1",
            "name": "quality",
        }
    ]

    assert validate_pull_request(valid_pull_request(), checks) == []


def test_merge_guard_rejects_draft_without_checks() -> None:
    pull_request = valid_pull_request()
    pull_request["isDraft"] = True

    errors = validate_pull_request(pull_request, [])

    assert "Pull request is still a draft." in errors
    assert "No CI checks were found." in errors


def test_merge_guard_rejects_outdated_branch_and_failed_check() -> None:
    pull_request = valid_pull_request()
    pull_request["mergeStateStatus"] = "BEHIND"
    checks: list[Check] = [
        {
            "bucket": "fail",
            "link": "https://github.com/example/repository/actions/runs/2",
            "name": "quality",
        }
    ]

    errors = validate_pull_request(pull_request, checks)

    assert any("not current and clean" in error for error in errors)
    assert "Check 'quality' is fail." in errors
