"""Git helpers
"""
import os
import re
from pathlib import Path
from pydash import py_

from eze.utils.error import EzeFileAccessError
from eze.utils.io.file import load_text
from eze.utils.log import log_error

MAX_RECURSION: int = 10

try:
    import git
except ImportError:
    # WORKAROUND: see "ImportError: Bad git executable."
    # see https://github.com/gitpython-developers/GitPython/issues/816
    log_error("Git not installed, eze will not be able to detect git branches")


def clean_url(url: str) -> str:
    """Clean up url and remove any embedded credentials, remove trailing .git to normalise git url"""
    cleaned_url = re.sub("//[^@]+@", "//", url)
    cleaned_url = re.sub("\\.git$", "", cleaned_url)
    return cleaned_url


def get_active_branch(git_dir: str) -> object:
    """recursive git repo check will return branch object if found"""
    git_path = Path(git_dir)
    i = 0
    while git_path and i < MAX_RECURSION:
        branch = _get_active_branch(git_path)
        if branch:
            return branch
        git_path /= ".."
        i += 1

    return None


def _get_active_branch(git_dir: str) -> object:
    """non-recursive git repo check will return branch object if found"""
    try:
        repo = git.Repo(git_dir)
        git_branch = repo.active_branch
    except NameError:
        # INFO: git will not exist when git not installed
        git_branch = None
    except git.GitError:
        # in particular git.InvalidGitRepositoryError
        git_branch = None
    except TypeError:
        # INFO: CI often checkout as detached head which doesn't technically have a branch
        # aka throws "TypeError: HEAD is a detached symbolic reference as it points to xxxx"
        git_branch = None
    except OSError:
        git_branch = None

    return git_branch


def get_active_branch_uri(git_dir: str) -> str:
    """given dir will check repo latest uri"""
    branch = get_active_branch(git_dir)
    git_uri = py_.get(branch, "repo.remotes.origin.url", None)
    if git_uri:
        # remove any credentials inside repo url
        return clean_url(git_uri)

    ci_uri = (
        # FROM Microsoft ADO: Build.Repository.Uri = BUILD_REPOSITORY_URI
        # https://docs.microsoft.com/en-us/azure/devops/pipelines/build/variables?view=azure-devops&tabs=yaml
        os.environ.get("BUILD_REPOSITORY_URI")
        # FROM AWS Amplify: AWS_CLONE_URL
        # https://docs.aws.amazon.com/amplify/latest/userguide/environment-variables.html#amplify-console-environment-variables
        or os.environ.get("AWS_CLONE_URL")
        # FROM JENKINS toolchain: GIT_LOCAL_BRANCH & GIT_BRANCH
        # https://plugins.jenkins.io/git/#environment-variables
        # FROM IBMCLOUD toolchain: GIT_URL
        # https://github.com/ibm-cloud-docs/ContinuousDelivery/blob/master/pipeline_deploy_var.md
        or os.environ.get("GIT_URL")
        # GCP ci: _REPO_URL
        # https://cloud.google.com/build/docs/configuring-builds/substitute-variable-values
        or os.environ.get("_REPO_URL")
        # FROM Gitlab CI: CI_REPOSITORY_URL
        # https://docs.gitlab.com/ee/ci/variables/predefined_variables.html
        or os.environ.get("CI_REPOSITORY_URL")
        # FROM Github CI: GITHUB_SERVER_URL + GITHUB_REPOSITORY
        # https://docs.github.com/en/actions/reference/environment-variables
        or (
            os.environ.get("GITHUB_SERVER_URL")
            and (os.environ.get("GITHUB_SERVER_URL") + "/" + os.environ.get("GITHUB_REPOSITORY"))
        )
    )
    if not ci_uri:
        return None
    # remove any credentials inside repo url
    return clean_url(ci_uri)


def get_active_branch_name(git_dir: str) -> str:
    """given dir will check repo latest branch"""
    branch = get_active_branch(git_dir)
    git_branchname = py_.get(branch, "name", None)
    if git_branchname:
        return git_branchname

    # SPECIAL ADO PULL REQUEST LOGIC
    # when BUILD_SOURCEBRANCH starts with 'refs/heads/' normal BUILD_SOURCEBRANCHNAME
    # when BUILD_SOURCEBRANCH starts with 'refs/pull/' pr, SYSTEM_PULLREQUEST_SOURCEBRANCH contains merge
    # https://docs.microsoft.com/en-us/azure/devops/pipelines/build/variables?view=azure-devops&tabs=yaml
    ado_source_branch = os.environ.get("BUILD_SOURCEBRANCH")
    if ado_source_branch and ado_source_branch.startswith("refs/pull/"):
        return os.environ.get("SYSTEM_PULLREQUEST_SOURCEBRANCH").replace("refs/heads/", "")

    ci_branchname = (
        # FROM ADO: Standard ADO non PR case, BUILD_SOURCEBRANCHNAME
        # https://docs.microsoft.com/en-us/azure/devops/pipelines/build/variables?view=azure-devops&tabs=yaml
        os.environ.get("BUILD_SOURCEBRANCHNAME")
        # FROM AWS Amplify: AWS_BRANCH
        # https://docs.aws.amazon.com/amplify/latest/userguide/environment-variables.html#amplify-console-environment-variables
        or os.environ.get("AWS_BRANCH")
        # FROM JENKINS toolchain: GIT_LOCAL_BRANCH & GIT_BRANCH
        # https://plugins.jenkins.io/git/#environment-variables
        # FROM IBMCLOUD toolchain: GIT_BRANCH
        # https://github.com/ibm-cloud-docs/ContinuousDelivery/blob/master/pipeline_deploy_var.md
        or os.environ.get("GIT_LOCAL_BRANCH")
        or os.environ.get("GIT_BRANCH")
        # FROM GCP ci: BRANCH_NAME
        # https://cloud.google.com/build/docs/configuring-builds/substitute-variable-values
        or os.environ.get("BRANCH_NAME")
        #  Gitlab CI: CI_COMMIT_BRANCH & CI_DEFAULT_BRANCH
        # https://docs.gitlab.com/ee/ci/variables/predefined_variables.html
        or os.environ.get("CI_COMMIT_BRANCH")
        or os.environ.get("CI_MERGE_REQUEST_TARGET_BRANCH_NAME")
        or os.environ.get("CI_EXTERNAL_PULL_REQUEST_TARGET_BRANCH_NAME")
        or os.environ.get("CI_DEFAULT_BRANCH")
        # FROM Github CI: GITHUB_REF
        # https://docs.github.com/en/actions/reference/environment-variables
        or os.environ.get("GITHUB_REF")
    )
    if ci_branchname:
        return ci_branchname

    return None


def get_gitignore_paths(git_dir: str = None) -> list:
    """will retrieve list of gitignore paths"""
    if git_dir:
        git_path = Path(git_dir)
    else:
        git_path = Path.cwd()
    gitignore = git_path / ".gitignore"
    try:
        gitignore_txt = load_text(gitignore)
    except EzeFileAccessError:
        return []
    gitignore_lines = [x for x in gitignore_txt.split("\n") if not x.strip().startswith("#") and not x.strip() == ""]
    return list(set(gitignore_lines))
