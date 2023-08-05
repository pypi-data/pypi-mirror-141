"""TruffleHog Python tool class"""
import re
import shlex
import time

from pydash import py_

from eze.core.enums import VulnerabilityType, VulnerabilitySeverityEnum, ToolType, SourceType, Vulnerability
from eze.core.tool import (
    ToolMeta,
    ScanResult,
)
from eze.utils.cli.run import run_async_cli_command
from eze.utils.io.file import (
    load_json,
    create_tempfile_path,
    is_windows_os,
    normalise_windows_regex_file_path,
    remove_non_folders,
    create_absolute_path,
)
from eze.utils.log import log
from eze.utils.io.file_scanner import IGNORED_FOLDERS, cache_workspace_into_tmp
from eze.utils.git import get_gitignore_paths


def extract_leading_number(value: str) -> str:
    """Take output and check for common version patterns"""
    leading_number_regex = re.compile("^[0-9.]+")
    leading_number = re.search(leading_number_regex, value)
    if leading_number:
        return value[leading_number.start() : leading_number.end()]
    return ""


class TruffleHogTool(ToolMeta):
    """TruffleHog Python tool class"""

    MAX_REASON_SIZE: int = 1000

    TOOL_NAME: str = "trufflehog"
    TOOL_URL: str = "https://pypi.org/project/truffleHog3/"
    TOOL_TYPE: ToolType = ToolType.SECRET
    SOURCE_SUPPORT: list = [SourceType.ALL]
    SHORT_DESCRIPTION: str = "opensource secret scanner"
    INSTALL_HELP: str = """In most cases all that is required to install truffleHog3 is python and pip install
pip install truffleHog3
trufflehog3 --help
pip show truffleHog3"""
    MORE_INFO: str = """https://pypi.org/project/truffleHog3/

Tips and Tricks
===============================
- use EXCLUDE to exclude compiled and dependency folders to gain a big speed increases
  aka "node_modules"
- use EXCLUDE to not run scan in tests
  aka to avoid high enthropy ids, or mock passwords in unit test fixtures, (or package-lock.json)
- use IGNORED_FILES to ignore false positives in files and folders
- false positives can be individually omitted with post fixing line with "# nosecret" and "// nosecret"
"""

    LICENSE: str = """GPL"""
    VERSION_CHECK: dict = {"FROM_EXE": "trufflehog3", "FROM_PIP": "truffleHog3"}

    EZE_CONFIG: dict = {
        "SOURCE": {
            "type": list,
            "default": ".",
            "required": True,
            "help_text": """TruffleHog3 list of source folders to scan for secrets""",
        },
        "EXCLUDE": {
            "type": list,
            "default": [],
            "help_text": """array of regex str of folders/files to exclude from scan for secrets
eze will automatically normalise folder separator "/" to os specific versions, "/" for unix, "\\\\" for windows""",
            "help_example": ["PATH-TO-EXCLUDED-FOLDER/.*", "PATH-TO-EXCLUDED-FILE.js", ".*\\.jpeg"],
        },
        "NO_ENTROPY": {
            "type": bool,
            "default": False,
            "help_text": """disable entropy checks, maps to flag --no-entropy""",
        },
        "DISABLE_DEFAULT_IGNORES": {
            "type": bool,
            "default": False,
            "help_text": f"""by default ignores common binary assets folder, ignore list
{ToolMeta.DEFAULT_IGNORED_LOCATIONS}""",
        },
        "CONFIG_FILE": {
            "type": str,
            "help_text": """TruffleHog3 config file to use
see https://github.com/feeltheajf/trufflehog3
see https://github.com/feeltheajf/truffleHog3/blob/master/examples/trufflehog.yaml""",
        },
        "INCLUDE_FULL_REASON": {
            "type": bool,
            "default": True,
            "help_text": """Optional include the full reason in report
Warning: on production might want to set this to False to prevent found Secrets appearing in reports""",
        },
        "REPORT_FILE": {
            "type": str,
            "default": create_tempfile_path("tmp-truffleHog-report.json"),
            "default_help_value": "<tempdir>/.eze-temp/tmp-truffleHog-report.json",
            "help_text": "output report location (will default to tmp file otherwise)",
        },
        "USE_GIT_IGNORE": {
            "type": bool,
            "default": True,
            "help_text": """ignore files specified in .gitignore""",
        },
        "USE_SOURCE_COPY": {
            "type": bool,
            "default": True,
            "environment_variable": "USE_SOURCE_COPY",
            "help_text": """speeds up SAST tools by using copied folder with no binary/dependencies assets
for mono-repos can speed up scans from 800s to 30s, by avoiding common dependencies such as node_modules
stored: TMP/.eze/cached-workspace""",
        },
    }
    DEFAULT_SEVERITY = VulnerabilitySeverityEnum.high.name

    TOOL_CLI_CONFIG = {
        "CMD_CONFIG": {
            # tool command prefix
            "BASE_COMMAND": shlex.split("trufflehog3 --no-history -f json"),
            # eze config fields -> arguments
            "ARGUMENTS": ["SOURCE"],
            # eze config fields -> flags
            "FLAGS": {
                "CONFIG_FILE": "-c ",
                "REPORT_FILE": "-o ",
            },
            "FLAGS_WITH_MULTI_FIELDS": {
                "EXCLUDE": "--exclude",
            },
            "SHORT_FLAGS": {"NO_ENTROPY": "--no-entropy"},
        }
    }

    BINARY_FILE_PATTERNS = [
        "*.woff",
        "*.woff2",
        "*.lock",
        "*.map",
        "*.exe",
        "*.ttf",
        "*.png",
        "*.eot",
        "*.svg",
        "*.png",
        "*.jpeg",
        "*.jpg",
        "*.webp",
        "*.ico",
        "*.zip",
        ".DS_Store",
        # IDEs and Configs
        # TERRAFORM
        "errored.tfstate",
        "*.lock.hcl",
        # NODE
        "package-lock.json",
        "*.min.js",
        "*.min.css",
        # PYTHON
    ]

    async def run_scan(self) -> ScanResult:
        """
        Method for running a synchronous scan using tool

        :raises EzeError
        """

        tic = time.perf_counter()

        scan_config = self.config.copy()
        # make REPORT_FILE absolute in-case cwd changes
        scan_config["REPORT_FILE"] = create_absolute_path(scan_config["REPORT_FILE"])
        cwd = cache_workspace_into_tmp() if self.config["USE_SOURCE_COPY"] else None
        completed_process = await run_async_cli_command(
            self.TOOL_CLI_CONFIG["CMD_CONFIG"], scan_config, self.TOOL_NAME, cwd=cwd
        )
        toc = time.perf_counter()
        total_time = toc - tic
        if total_time > 10:
            log(
                f"trufflehog scan took a long time ({total_time:0.2f}s), "
                f"you can often speed up trufflehog significantly by excluding dependency or binary folders like node_modules or sbin"
            )
        parsed_json = load_json(self.config["REPORT_FILE"])
        report = self.parse_report(parsed_json)
        if completed_process.stderr:
            report.warnings.append(completed_process.stderr)

        return report

    def _trufflehog_v3_line(self, report_event):
        """ab-712: Post Aug 2021 - Trufflehog3 v3 format parse support"""
        path = report_event["path"]
        line = report_event["line"]
        reason = report_event["rule"]["message"]

        name = f"Found Hardcoded '{reason}' Pattern"
        summary = f"Found Hardcoded '{reason}' Pattern in {path}"
        recommendation = (
            f"Investigate '{path}' Line {line} for '{reason}' strings (add '# nosecret' to line if false positive)"
        )

        # only include full reason if include_full_reason true
        if self.config["INCLUDE_FULL_REASON"]:
            line_containing_secret = report_event["context"][line]
            if len(line_containing_secret) > self.MAX_REASON_SIZE:
                recommendation += f" Full Match: <on long line ({len(line_containing_secret)} characters)>"
            else:
                recommendation += " Full Match: " + line_containing_secret
        return Vulnerability(
            {
                "vulnerability_type": VulnerabilityType.secret.name,
                "name": name,
                "version": None,
                "overview": summary,
                "recommendation": recommendation,
                "language": "file",
                "severity": report_event["rule"]["severity"],
                "identifiers": {},
                "metadata": None,
                "file_location": {"path": path, "line": line},
            }
        )

    def _trufflehog_v2_line(self, report_event):
        """ab-712: Pre Aug 2021 - Trufflehog3 v2 format parse support"""
        path = report_event["path"]
        reason = report_event["reason"]
        found = "\n".join(report_event["stringsFound"])
        line = extract_leading_number(found)

        name = f"Found Hardcoded '{reason}' Pattern"
        summary = f"Found Hardcoded '{reason}' Pattern in {path}"
        recommendation = (
            f"Investigate '{path}' Line {line} for '{reason}' strings (add '# nosecret' to line if false positive)"
        )

        # only include full reason if include_full_reason true
        if self.config["INCLUDE_FULL_REASON"]:
            if len(found) > self.MAX_REASON_SIZE:
                recommendation += f" Full Match: <on long line ({len(found)} characters)>"
            else:
                recommendation += " Full Match: " + found
        return Vulnerability(
            {
                "vulnerability_type": VulnerabilityType.secret.name,
                "name": name,
                "version": None,
                "overview": summary,
                "recommendation": recommendation,
                "language": "file",
                "severity": self.DEFAULT_SEVERITY,
                "identifiers": {},
                "metadata": None,
                "file_location": {"path": path, "line": line},
            }
        )

    def parse_report(self, parsed_json: list) -> ScanResult:
        """convert report json into ScanResult"""
        report_events = parsed_json
        vulnerabilities_list = []

        for report_event in report_events:
            is_v3_report = py_.get(report_event, "rule.message", False)
            if is_v3_report:
                vulnerability = self._trufflehog_v3_line(report_event)
                vulnerabilities_list.append(vulnerability)
            else:
                vulnerability = self._trufflehog_v2_line(report_event)
                vulnerabilities_list.append(vulnerability)

        report: ScanResult = ScanResult(
            {
                "tool": self.TOOL_NAME,
                "vulnerabilities": vulnerabilities_list,
                "warnings": [],
            }
        )
        return report

    def _parse_config(self, eze_config: dict) -> dict:
        """take raw config dict and normalise values"""
        parsed_config = super()._parse_config(eze_config)

        # ADDITION PARSING: EXCLUDE
        # convert to space separated, clean os specific regex
        if not parsed_config["DISABLE_DEFAULT_IGNORES"]:
            ignored_folders = IGNORED_FOLDERS
            parsed_config["EXCLUDE"].extend(ignored_folders)
            parsed_config["EXCLUDE"].extend(self.BINARY_FILE_PATTERNS)

        # ADDITION PARSING: EXCLUDE
        # add git ignore onto excludes
        if parsed_config["USE_GIT_IGNORE"]:
            gitignore_paths = get_gitignore_paths()
            parsed_config["EXCLUDE"].extend(gitignore_paths)

        # ADDITION PARSING: EXCLUDE
        # convert to space separated, clean os specific regex
        if len(parsed_config["EXCLUDE"]) > 0:
            if is_windows_os():
                parsed_config["EXCLUDE"] = list(map(normalise_windows_regex_file_path, parsed_config["EXCLUDE"]))
            # normalise paths for duplicates
            parsed_config["EXCLUDE"] = sorted(set(parsed_config["EXCLUDE"]))

        # ADDITIONAL PARSING: AB-848: detect non folders being set as source
        # remove from SOURCE
        parsed_config["SOURCE"] = remove_non_folders(parsed_config["SOURCE"], ["."], "trufflehog")

        return parsed_config
