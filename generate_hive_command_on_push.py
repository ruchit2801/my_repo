import datetime
import json
import os
from copy import deepcopy
from croniter import croniter
from typing import Any, Dict, List, Optional, Set, Tuple
from github import Github, Repository, PullRequest
from github.File import File
from github.PaginatedList import PaginatedList
from utils.constants import HIVE_SUPPORTED_DATA_TYPES, REQUIRED_KEYS, DATA_TYPE_COMPATIBILITY_MAP, SUPPORTED_INPUT_FORMATS

class CommandGenerator:
    def __init__(self):
        self.repo_name: str = str(os.environ['REPO_NAME'])
        self.pr_num: int = int(os.environ['PULL_NUMBER'])
        self.github_token: str = str(os.environ['GITHUB_TOKEN'])
        self.github = Github(login_or_token=self.github_token)
        self.repo: Repository = self.github.get_repo(full_name_or_id=self.repo_name)
        self.pull_request_obj: PullRequest = self._get_pull_request_obj()
        self.changed_files: PaginatedList[File] = self._get_changed_files()

    
    def _get_pull_request_obj(self) -> PullRequest:
        print(f"checking for #{self.pr_num} in {self.repo_name}")
        pull_request: PullRequest = self.repo.get_pull(number=self.pr_num)
        print("Fetched pull_request object.")
        return pull_request

    def _get_changed_files(self):
        return self.pull_request_obj.get_files()

    def setup_command_generation(self):
        for page in range(self.changed_files.totalCount):
            files: List[File] = self.changed_files.get_page(page=page)
            for file in files:
                file_status: str = file.status
                print(f"Checking for {file.filename} with status: {file_status}")
                _, file_extension = os.path.splitext(file.filename)
                if file_extension == ".json":
                    if file_status == "removed":
                        json_data = self._get_json_from_file_path(file.filename)
                        # hive_command = generate_hive_command_from_json("removed", json_data)
                    elif file_status == "modified":
                        new_content : Dict[str, Dict[str, Any]] = self._get_json_from_file_path(file.filename)
                        old_content : Dict[str, Dict[str, Any]] = json.loads(self.repo.get_contents(file.filename).decoded_content.decode())

                        print(new_content)
                        print(old_content)

                        # hive_command = generate_hive_command_from_json("modified", modifications)
                    elif file_status == "created":
                        json_schema : Dict[str, Dict[str, Any]] = self._get_json_from_file_path(file.filename)

                        print(json_schema)

generator = CommandGenerator()
generator.setup_command_generation()