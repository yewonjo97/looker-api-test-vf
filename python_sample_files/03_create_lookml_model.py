from functools import reduce
import sys
from typing import cast, MutableSequence, Sequence
import os
import json

import looker_sdk
from looker_sdk import models40 as models

from github import Github

def main(git_token:str):
    connection_name = sys.argv[1] if len(sys.argv) > 1 else ""
    git_name = sys.argv[2] if len(sys.argv) > 1 else ""
    project_name = sys.argv[3] if len(sys.argv) > 1 else ""
    model_name = sys.argv[4] if len(sys.argv) > 1 else ""

    view_name = "superstore"
    schema_name = "@@@@@"
    table_name = "superstore"


    if not connection_name:
        raise Exception("Please provide a connection name")
    elif connection_name in ["looker", "looker__internal__analytics"]:
        raise Exception(
            f"Connection '{connection_name}' is internal and cannot be tested."
        )

    if not git_name:
        raise Exception("Please provide a git name")


    if not project_name:
        raise Exception("Please provide a project name")
    elif project_name in ["looker", "looker__internal__analytics"]:
        raise Exception(f"Project {project_name} Already Exists")


    if not model_name:
        raise Exception("Please provide a model name")
    elif model_name in ["looker", "looker__internal__analytics"]:
        raise Exception(f"Project {model_name} Already Exists")



    model_file, view_file = create_files_in_local(connection_name, model_name, view_name, schema_name, table_name)

    upload_files_to_github(git_name, git_token, project_name, model_name, view_name, schema_name, table_name, model_file, view_file)

    pull_and_deploy_project(project_name)


# (텍스트 처리를 위해서 파일을 읽어오는 방법으로 작성함)
# 파일을 새로 작성해주는 부분은, 편한 방법대로 해주시면 됩니다.
# 모델 이름, Connection 명, 테이블 정보(스키마, 테이블명)만 소스가 되는 정보로 작성해주시면 됩니다.

def create_files_in_local(
    connection_name: str, 
    model_name: str, 
    view_name: str,
    schema_name: str,
    table_name: str,
    ):

    model_r = open("/Users/mzc01-ywjo/lookersdk_test/sample_files/model_template.txt","r")
    model_w = open("/Users/mzc01-ywjo/lookersdk_test/sample_files/model_new.txt","a")

    model_file = model_r.read().replace("Your_Connection", connection_name)
    model_w.write(model_file)

    model_r.close()
    model_w.close()
    
    new_model_r = open("/Users/mzc01-ywjo/lookersdk_test/sample_files/model_new.txt","r")
    new_model_file = new_model_r.read()

    new_model_r.close()


    view_r = open("/Users/mzc01-ywjo/lookersdk_test/sample_files/view_template.txt","r")
    view_w = open("/Users/mzc01-ywjo/lookersdk_test/sample_files/view_new.txt","a")

    view_file = view_r.read().replace("Your_Schema", schema_name)
    view_file = view_file.replace("Your_Table", table_name)

    view_w.write(view_file)

    view_r.close()
    view_w.close()
    
    new_view_r = open("/Users/mzc01-ywjo/lookersdk_test/sample_files/view_new.txt","r")
    new_view_file = new_view_r.read()
    
    new_view_r.close()

    print("Model and View Files are Created in Local")

    return new_model_file, new_view_file


def upload_files_to_github(
    git_name: str, 
    git_token: str,
    project_name: str,
    model_name: str,
    view_name: str,
    schema_name: str,
    table_name: str,
    new_model_file,
    new_view_file
    ):

    g = Github(git_token)
    user = g.get_user()
    repo = user.get_repo(git_name)

    branch = sdk.all_git_branches(project_id = project_name)
    names = [branch.name for branch in branch]

    target_branch = [branch for branch in names if my_user.first_name.lower() in branch.lower() and my_user.last_name.lower() in branch.lower()][0]


    git_model_prefix = 'models/'
    git_model_file = git_model_prefix+f'{model_name}.model.lkml'

    repo.create_file(git_model_file, "committing files", new_model_file, branch=target_branch)  

    print("model uploaded")
    

    git_view_prefix = 'views/'
    git_view_file = git_view_prefix+f'{view_name}.view.lkml'

    repo.create_file(git_view_file, "committing files", new_view_file, branch=target_branch)

    print("view uploaded")


def pull_and_deploy_project(project_name:str):
    sdk.reset_project_to_remote(project_id=project_name)
    print("Pull From Remote")

    sdk.deploy_to_production(project_id=project_name)
    print("Deploy to Production")


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

    # looker_sdk 초기화
    sdk = looker_sdk.init40()
    # 프로젝트 생성 및 Deploy는 Dev 모드에서만 가능하기 때문에 반드시 설정
    sdk.update_session({"workspace_id":"dev"})

    my_user = sdk.me()

    main(git_token)
