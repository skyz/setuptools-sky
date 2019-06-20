import os

import pytest


@pytest.fixture
def wd(wd):
    wd("git init")
    wd("git config user.email test@example.com")
    wd('git config user.name "a test"')
    wd.add_command = "git add ."
    wd.commit_command = "git commit -m test-{reason}"

    return wd


def test_git_develop_branch_increments_patch(wd):
    os.environ["BRANCH_NAME"] = "develop"
    wd("git checkout -b develop")

    assert wd.version == "0.0.1-beta.0"

    wd.commit_testfile()

    assert wd.version == "0.0.1-beta.1"

    wd("git tag 0.1.0")
    wd.commit_testfile()

    assert wd.version == "0.1.1-beta.1"


def test_git_release_branch_increments_patch(wd):
    os.environ["BRANCH_NAME"] = "release"
    wd("git checkout -b release")

    assert wd.version == "0.0.1-rc.0"

    wd.commit_testfile()

    assert wd.version == "0.0.1-rc.1"

    wd("git tag 0.1.0")
    wd.commit_testfile()

    assert wd.version == "0.1.1-rc.1"


def test_git_master_branch_increments_patch(wd):
    os.environ["BRANCH_NAME"] = "master"
    wd("git checkout -b master")

    assert wd.version == "0.0.1"

    wd.commit_testfile()
    wd("git tag 0.0.1")

    wd.commit_testfile()
    wd.commit_testfile()

    assert wd.version == "0.0.2"


def test_git_pr_to_develop_branch_increments_patch(wd):
    os.environ["BRANCH_NAME"] = "PR-123"
    os.environ["CHANGE_TARGET"] = "develop"

    wd("git checkout -b PR-123")

    assert wd.version == "0.0.1-alpha.0"

    wd.commit_testfile()

    assert wd.version == "0.0.1-alpha.1"

    wd("git tag 0.1.0")
    wd.commit_testfile()
    wd.commit_testfile()

    assert wd.version == "0.1.1-alpha.2"


def test_git_pr_to_release_branch_increments_patch(wd):
    os.environ["BRANCH_NAME"] = "PR-123"
    os.environ["CHANGE_TARGET"] = "release"

    wd("git checkout -b PR-123")

    assert wd.version == "0.0.1-rc.0"

    wd.commit_testfile()

    assert wd.version == "0.0.1-rc.1"

    wd("git tag 0.1.0")
    wd.commit_testfile()

    assert wd.version == "0.1.1-rc.1"


def test_git_pr_to_master_branch_increments_patch(wd):
    os.environ["BRANCH_NAME"] = "PR-123"
    os.environ["CHANGE_TARGET"] = "master"

    wd("git checkout -b PR-123")

    assert wd.version == "0.0.1"

    wd.commit_testfile()

    assert wd.version == "0.0.1"

    wd("git tag 0.1.1")
    wd.commit_testfile()

    assert wd.version == "0.1.2"
