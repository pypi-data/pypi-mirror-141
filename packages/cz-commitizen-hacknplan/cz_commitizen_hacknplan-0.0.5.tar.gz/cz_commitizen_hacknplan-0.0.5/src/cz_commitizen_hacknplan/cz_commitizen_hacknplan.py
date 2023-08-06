import json
import os
import re
from collections import OrderedDict, defaultdict
from datetime import date
from typing import Callable, Dict, Iterable, List, Optional

import requests
from commitizen import defaults, git, config
from commitizen.cz.base import BaseCommitizen
from commitizen.config.base_config import BaseConfig
from commitizen.cz.utils import multiple_line_breaker, required_validator
from commitizen.defaults import Questions

__all__ = ["ConventionalHackNPlanCz"]


def parse_scope(text):
    if not text:
        return ""

    scope = text.strip().split()
    if len(scope) == 1:
        return scope[0]

    return "-".join(scope)


def parse_subject(text):
    if isinstance(text, str):
        text = text.strip(".").strip()

    return required_validator(text, msg="Subject is required.")


class ConventionalHackNPlanCz(BaseCommitizen):
    bump_pattern = defaults.bump_pattern
    bump_map = defaults.bump_map
    commit_parser = defaults.commit_parser
    version_parser = defaults.version_parser
    change_type_map = {
        "feat": "Feat",
        "fix": "Fix",
        "docs": "Documentation",
        "style": "Styling",
        "refactor": "Refactor",
        "perf": "Performance",
        "test": "Test",
        "build": "Build",
        "ci": "CI",
    }

    # Read the config file
    conf = config.read_cfg()

    git_base_url = conf.settings.get("git_base_url", "https://github.com/")
    use_gitlab = conf.settings.get("use_gitlab", False)
    git_repo = conf.settings.get("git_repo", "")
    projectid = conf.settings.get("projectid", 0)


    hnp_key = os.environ.get("HNP_KEY")
    hnp_base_url = "https://api.hacknplan.com"
    hnp_app_url = "https://app.hacknplan.com"
    projects_endpoint = "/v0/projects"
    workitems_endpoint = "/v0/projects/{projectId}/workitems"
    workitem_endpoint = "/v0/projects/{projectId}/workitems/{workItemId}"

    def questions(self) -> Questions:
        if "git_repo" not in self.conf.settings:
            print("Please add the key git_repo to your .cz.yaml|json|toml config file.")
            quit()

        if "projectid" not in self.conf.settings:
            print("Please add the key projectid to your .cz.yaml|json|toml config file.")
            quit()

        questions: Questions = [
            {
                "type": "list",
                "name": "prefix",
                "message": "Select the type of change you are committing",
                "choices": [
                    {
                        "value": "fix",
                        "name": "🐛 fix: A bug fix. Correlates with PATCH in SemVer",
                        "key": "x",
                    },
                    {
                        "value": "feat",
                        "name": "🎉 feat: A new feature. Correlates with MINOR in SemVer",
                        "key": "f",
                    },
                    {
                        "value": "docs",
                        "name": "📜 docs: Documentation only changes",
                        "key": "d",
                    },
                    {
                        "value": "style",
                        "name": (
                            "😎 style: Changes that do not affect the "
                            "meaning of the code (white-space, formatting,"
                            " missing semi-colons, etc)"
                        ),
                        "key": "s",
                    },
                    {
                        "value": "refactor",
                        "name": (
                            "🔧 refactor: A code change that neither fixes "
                            "a bug nor adds a feature"
                        ),
                        "key": "r",
                    },
                    {
                        "value": "perf",
                        "name": "🚀 perf: A code change that improves performance",
                        "key": "p",
                    },
                    {
                        "value": "test",
                        "name": (
                            "🚦 test: Adding missing or correcting " "existing tests"
                        ),
                        "key": "t",
                    },
                    {
                        "value": "build",
                        "name": (
                            "🚧 build: Changes that affect the build system or "
                            "external dependencies (example scopes: pip, docker, npm)"
                        ),
                        "key": "b",
                    },
                    {
                        "value": "ci",
                        "name": (
                            "🛸 ci: Changes to our CI configuration files and "
                            "scripts (example scopes: GitLabCI)"
                        ),
                        "key": "c",
                    },
                    {
                        "value": "chore",
                        "name": (
                            "🧹 chore: General housekeeping chores"
                        ),
                        "key": "h",
                    },
                ],
            },
            {
                "type": "input",
                "name": "scope",
                "message": (
                    "What is the scope of this change? (class or file name): (press [enter] to skip)\n"
                ),
                "filter": parse_scope,
            },
            {
                "type": "input",
                "name": "subject",
                "filter": parse_subject,
                "message": (
                    "Write a short and imperative summary of the code changes: (lower case and no period)\n"
                ),
            },
            {
                "type": "checkbox",
                "name": "tasks",
                "message": "Tasks(optional):\n",
                "choices": []
            },
            {
                "type": "input",
                "name": "body",
                "message": (
                    "Provide additional contextual information about the code changes: (press [enter] to skip)\n"
                ),
                "filter": multiple_line_breaker,
            },
            {
                "type": "confirm",
                "message": "Is this a BREAKING CHANGE? Correlates with MAJOR in SemVer",
                "name": "is_breaking_change",
                "default": False,
            },
            {
                "type": "input",
                "name": "footer",
                "message": (
                    "Footer. Information about Breaking Changes and "
                    "reference issues that this commit closes: (press [enter] to skip)\n"
                ),
            },
        ]

        url = self.hnp_base_url + self.workitems_endpoint.format(projectId=self.projectid)

        headers = {"Authorization": "ApiKey " + str(self.hnp_key)}

        r = requests.get(url, headers=headers)
        response_data = json.loads(r.text)

        for question in filter(lambda q: q["name"] == "tasks", questions):
            for task in response_data['items']:
                if task["isBlocked"] == False:
                    question["choices"].append(
                        {
                            "value": task["workItemId"],
                            "name": task["title"]
                        }
                    )
        return questions

    def message(self, answers: dict) -> str:
        prefix = answers["prefix"]
        scope = answers["scope"]
        subject = answers["subject"]
        body = answers["body"]
        footer = answers["footer"]
        tasks = answers["tasks"]
        tasks_text = ""
        is_breaking_change = answers["is_breaking_change"]

        if scope:
            scope = f"({scope})"
        if body:
            body = f"\n\n{body}"
        if is_breaking_change:
            footer = f"BREAKING CHANGE 🚨: {footer}"
        if footer:
            footer = f"\n\n{footer}"
        if tasks:
            tasks_text = ' ,'.join([f'#{task_id}' for task_id in tasks])
            tasks_text = f"\n\nTasks: {tasks_text}"

        message = f"{prefix}{scope}: {subject}{body}{footer}{tasks_text}"

        return message

    def example(self) -> str:
        return (
            "fix(code): correct minor typos in code\n"
            "\n"
            "see the issue for details on the typos fixed\n"
            "\n"
            "closes issue #12"
            "\n"
            "Task: #12"
        )

    def schema(self) -> str:
        return (
            "<change_type>(<scope>): <subject>\n"
            "<BLANK LINE>\n"
            "<body>\n"
            "<BLANK LINE>\n"
            "(BREAKING CHANGE: )<footer>\n"
            "Tasks: <tasks>"
        )

    def schema_pattern(self) -> str:
        PATTERN = (
            r"(build|ci|docs|feat|fix|perf|refactor|style|test|chore|revert|bump)"
            r"(\(\S+\))?!?:(\s.*)"
        )
        return PATTERN

    def info(self) -> str:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        filepath = os.path.join(dir_path, "cz_commitizen_hacknplan_info.txt")
        with open(filepath, "r") as f:
            content = f.read()
        return content

    def process_commit(self, commit: str) -> str:
        pat = re.compile(self.schema_pattern())
        m = re.match(pat, commit)
        if m is None:
            return ""
        return m.group(3).strip()

    def workitem_url_builder(self, workitemid: int) -> str:
        url = self.hnp_base_url + self.workitem_endpoint.format(projectId=self.projectid, workItemId=workitemid)

        headers = {"Authorization": "ApiKey " + str(self.hnp_key)}
        r = requests.get(url, headers=headers)
        response_data = json.loads(r.text)
        url = "/p/{projectid}/kanban?categoryId=0&boardId={boardid}&taskId={taskid}&tabId=basicinfo".format(projectid=self.projectid, boardid=response_data['board']['boardId'],taskid=workitemid)
        return url

    def changelog_message_builder_hook(
        self, parsed_message: dict, commit: git.GitCommit
    ) -> dict:
        commit_parser = r"^(?P<change_type>feat|fix|refactor|perf|BREAKING CHANGE)(?:\((?P<scope>[^()\r\n]*)\)|\()?(?P<breaking>!)?:\s(?P<message>.*)Tasks: (?P<tasks>.*)?"
        body_map_pat = re.compile(commit_parser, re.MULTILINE | re.DOTALL)

        message = body_map_pat.match(commit.message)
        parsed_body: Dict = message.groupdict()

        """add gitlab and hacknplan links to the changelog"""
        rev = commit.rev
        m = parsed_body["message"]
        s = parsed_message["scope"]
        if parsed_body["tasks"]:
            parsed_message["scope"] = parsed_body["tasks"]
            parsed_message["scope"] = " ".join(
                [
                    f"({s}) - [Task #{task_id}]({self.hnp_app_url}{self.workitem_url_builder(task_id)})"
                    for task_id in parsed_body["tasks"].replace("#", "").split(",")
                ]
            )

        if self.use_gitlab:
            parsed_message[
                "message"
            ] = f"[{rev[:5]}]({self.git_base_url}/{self.git_repo}/-/tree/{commit.rev}) {m}"
        else:
            parsed_message[
                "message"
            ] = f"[{rev[:5]}]({self.git_base_url}/{self.git_repo}/commit/{commit.rev}) {m}"

        return parsed_message
