import datetime
import json
import os
from copy import deepcopy
from croniter import croniter
from typing import Any, Dict, List, Optional, Set, Tuple
from github import Github, Repository, PullRequest
from github.File import File
from github.PaginatedList import PaginatedList
from utils.constants import HIVE_SUPPORTED_DATA_TYPES, REQUIRED_KEYS, DATA_TYPE_COMPATIBILITY_MAP

class JsonValidator:
    def __init__(self):
        self.repo_name: str = str(os.environ["REPO_NAME"])
        self.pr_num: int = int(os.environ["PULL_NUMBER"])
        self.github_token: str = str(os.environ["GITHUB_TOKEN"])
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

    @staticmethod
    def _check_if_required_keys_present(json_data: Dict[str, Dict[str, Any]], filename: str):
        print("Checking if required keys are present")
        for key in REQUIRED_KEYS:
            assert key in json_data

    @staticmethod
    def _check_if_only_hive_supported_data_types_present(json_data: Dict[str, Dict[str, Any]], filename: str):
        for column_name, data_type in json_data["columns"].items():
            assert data_type in HIVE_SUPPORTED_DATA_TYPES


    @staticmethod
    def _validate_json_data(json_data: Dict[str, Dict[str, Any]], filename: str):
        self._check_if_required_keys_present(json_data, filename)
        self._check_if_only_hive_supported_data_types_present(json_data, filename)

    @staticmethod
    def _validate_columns(old_columns, new_columns):
        len_old = len(old_columns)
        len_new = len(new_columns)

        assert len_old <= len_new

        old_column_names = set()
        for i, column in enumerate(old_columns):
            assert column["name"] == new_columns[i]["name"]
            
            if(column["type"] != new_columns[i]["type"]):
                assert new_columns[i]["type"] in DATA_TYPE_COMPATIBILITY_MAP[column["type"]]

            old_column_names.add(column["name"])
            
        
        for i in range(len_old, len_new):
            assert "name" in new_columns[i]
            assert "type" in new_columns[i]

            _name, _type = new_columns[i]["name"], new_columns[i]["type"]

            assert _type in HIVE_SUPPORTED_DATA_TYPES

            assert new_columns[i]["name"] not in old_column_names

            old_column_names.add(_name)

    def validate_file_modification(self, old_content: Dict[str, Dict[str, Any]], new_content: Dict[str, Dict[str, Any]]):
        self._validate_columns(old_content["columns"], new_content["columns"])

        if "partitioned" in old_content:
            assert "partitioned" in new_content

            self._validate_columns(old_content["partitioned"], new_content["partitioned"])

    @staticmethod
    def _get_json_from_file_path(file_path: str) -> Optional[Dict[str, Dict[str, Any]]]:
        res_data: Optional[Dict[str, Dict[str, Any]]] = None
        try:
            with open(file_path) as json_file:
                res_data: Dict[str, Dict[str, Any]] = json.load(json_file)
        except Exception as e:
            print(e)
        return res_data

    def parse_changed_files_for_validation(self):
        for page in range(self.changed_files.totalCount):
            files: List[File] = self.changed_files.get_page(page=page)
            for file in files:
                file_status: str = file.status
                print(f"Checking for {file.filename} with status: {file_status}")
                _, file_extension = os.path.splitext(file.filename)
                if file_status == "removed":
                    # TODO : Implement dropping tables flow
                    pass
                
                if file_status == "modified":

                    new_content : Dict[str, Dict[str, Any]] = self._get_json_from_file_path(file.filename)
                    old_content : Dict[str, Dict[str, Any]] = json.loads(self.repo.get_contents(file.filename).decoded_content.decode())

                    # self._validate_json_data(new_content)
                    self.validate_file_modification(old_content, new_content)

                    

validator = JsonValidator()
validator.parse_changed_files_for_validation()