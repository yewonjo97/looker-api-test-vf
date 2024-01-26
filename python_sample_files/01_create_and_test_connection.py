from functools import reduce
import sys
from typing import cast, MutableSequence, Sequence
import os
import json

import looker_sdk
from looker_sdk import models40 as models


def main(db_username: str, db_password: str, db_database:str, db_jdbc_param: str):
    connection_name = sys.argv[1] if len(sys.argv) > 1 else ""

    if not connection_name:
        raise Exception("Please provide a connection name")
    elif connection_name in ["looker", "looker__internal__analytics"]:
        raise Exception(
            f"Connection '{connection_name}' is internal and cannot be tested."
        )

    create_connection(connection_name, db_username, db_password,db_database, db_jdbc_param)
    print("Create Connection")

    connection = get_connections(connection_name)
    print("### Get Connection ###")
    
    results = test_connection(connection)
    print("### Test Connection ###")
    
    output_results(cast(str, connection.name), results)    



def create_connection(name: str, username: str, password: str, database: str, jdbc_param: str) -> models.WriteDBConnection:
    sdk.create_connection(
        body=models.WriteDBConnection(
            name=name,
            host="athena.ap-northeast-2.amazonaws.com",
            port="443",
            username=username,
            password=password,
            database=database,
            db_timezone="asia-seoul",
            query_timezone="asia-seoul",
            max_connections=5,
            jdbc_additional_params=jdbc_param,
            pool_timeout=120,
            dialect_name="athena",
            pdt_concurrency=1,
            ssl=False,
            verify_ssl=False,
            user_db_credentials=False,
            sql_runner_precache_tables=False,
            sql_writing_with_info_schema=False,
            custom_local_port=0,
            uses_tns=False,
            disable_context_comment=False,
            always_retry_failed_builds=False,
            cost_estimate_enabled=False,
            pdt_api_control_enabled=False
        ))


def get_connections(name: str) -> models.DBConnection:
    connection = sdk.connection(name, fields="name, dialect")
    return connection


def test_connection(
    connection: models.DBConnection,
) -> Sequence[models.DBConnectionTestResult]:
    """Run supported tests against a given connection."""
    assert connection.name
    assert connection.dialect and connection.dialect.connection_tests
    supported_tests: MutableSequence[str] = list(connection.dialect.connection_tests)
    test_results = sdk.test_connection(
        connection.name, models.DelimSequence(supported_tests)
    )
    return test_results


def output_results(
    connection_name: str, test_results: Sequence[models.DBConnectionTestResult]
):
    """Prints connection test results."""
    errors = list(filter(lambda test: cast(str, test.status) == "error", test_results))
    if errors:
        report = reduce(
            lambda failures, error: failures + f"\n  - {error.message}",
            errors,
            f"{connection_name}:",
        )
    else:
        report = f"All tests for connection '{connection_name}' were successful."
    print(report)


if __name__ == '__main__':


    os.environ["LOOKERSDK_BASE_URL"] = "@@@@@" #If your looker URL has .cloud in it (hosted on GCP), do not include :19999 (ie: https://your.cloud.looker.com).
    os.environ["LOOKERSDK_API_VERSION"] = "4.0" #As of Looker v23.18+, the 3.0 and 3.1 versions of the API are removed. Use "4.0" here.
    os.environ["LOOKERSDK_VERIFY_SSL"] = "true" #Defaults to true if not set. SSL verification should generally be on unless you have a real good reason not to use it. Valid options: true, y, t, yes, 1.
    os.environ["LOOKERSDK_TIMEOUT"] = "120" #Seconds till request timeout. Standard default is 120.

    #Get the following values from your Users page in the Admin panel of your Looker instance > Users > Your user > Edit API keys. If you know your user id, you can visit https://your.looker.com/admin/users/<your_user_id>/edit.
    os.environ["LOOKERSDK_CLIENT_ID"] =  "@@@@@" #No defaults.
    os.environ["LOOKERSDK_CLIENT_SECRET"] = "@@@@@" #No defaults. This should be protected at all costs. Please do not leave it sitting here, even if you don't share this document.

    print("All environment variables set.")

    db_username="@@@@@"              # IAM Access Key
    db_password="@@@@@"              # IAM Seceret Key
    db_database="@@@@@"              # Athena Database
    db_jdbc_param="Workgroup=@@@@@"  # Athena Workgroup 사용시 작업그룹 이름 작성, by default = primary


    sdk = looker_sdk.init40()
    my_user = sdk.me()

    print(my_user.first_name)
    print(my_user.last_name)
    
    main(db_username, db_password, db_database, db_jdbc_param)
