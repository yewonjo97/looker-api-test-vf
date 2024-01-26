from functools import reduce
import sys
from typing import cast, MutableSequence, Sequence
import os
import json

import looker_sdk
from looker_sdk import models40 as models

from github import Github

def main(git_token):
    project_name = sys.argv[1] if len(sys.argv) > 1 else ""

    git_name = sys.argv[2] if len(sys.argv) > 1 else ""


    if not project_name:
        raise Exception("Please provide a project name")
    elif project_name in ["looker", "looker__internal__analytics"]:
        raise Exception(f"Project {project_name} Already Exists")

    if not git_name:
        raise Exception("Please provide a git name")


    create_git_repo(git_name, git_token)

    create_project(project_name)

    get_project(project_name)

    update_proejct_git(project_name, git_name, git_token)


def create_git_repo(git_name: str, git_token:str ) :
    g = Github(git_token) 
    user = g.get_user()

    user.create_repo(git_name, private=False, auto_init=True)

    print("Git Repo is Created")


def create_project(prj_name: str) -> models.WriteProject:
    sdk.create_project(
        body=models.WriteProject(
            name=prj_name
            ))    
    print("Project Created")


def get_project(prj_name: str) -> models.Project:
    project = sdk.project(prj_name, fields="name")

    print("Check if Projet is Created")

    return project


def update_proejct_git(prj_name: str, git_name, git_token) -> models.WriteProject:
    url = f'https://github.com/@@@@@/{git_name}.git'

    sdk.update_project(
        project_id=prj_name,
        body=models.WriteProject(
            git_username="token",
            git_password=git_token,
            git_remote_url=url,
            pull_request_mode="off"))

    print("Finish Git Configuration")



if __name__ == '__main__':

    os.environ["LOOKERSDK_BASE_URL"] = "@@@@@" #If your looker URL has .cloud in it (hosted on GCP), do not include :19999 (ie: https://your.cloud.looker.com).
    os.environ["LOOKERSDK_API_VERSION"] = "4.0" #As of Looker v23.18+, the 3.0 and 3.1 versions of the API are removed. Use "4.0" here.
    os.environ["LOOKERSDK_VERIFY_SSL"] = "true" #Defaults to true if not set. SSL verification should generally be on unless you have a real good reason not to use it. Valid options: true, y, t, yes, 1.
    os.environ["LOOKERSDK_TIMEOUT"] = "120" #Seconds till request timeout. Standard default is 120.

    #Get the following values from your Users page in the Admin panel of your Looker instance > Users > Your user > Edit API keys. If you know your user id, you can visit https://your.looker.com/admin/users/<your_user_id>/edit.
    os.environ["LOOKERSDK_CLIENT_ID"] =  "@@@@@" #No defaults.
    os.environ["LOOKERSDK_CLIENT_SECRET"] = "@@@@@" #No defaults. This should be protected at all costs. Please do not leave it sitting here, even if you don't share this document.

    print("All environment variables set.")

    git_token = "@@@@@"

    sdk = looker_sdk.init40()
    # 프로젝트 생성 및 Deploy는 Dev 모드에서만 가능하기 때문에 반드시 설정
    sdk.update_session({"workspace_id":"dev"})

    my_user = sdk.me()

    main(git_token)
