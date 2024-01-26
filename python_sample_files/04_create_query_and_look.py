from functools import reduce
import sys
from typing import cast, MutableSequence, Sequence
import os
import json

import looker_sdk
from looker_sdk import models40 as models


def main(folder_id:str):
    look_name = sys.argv[1] if len(sys.argv) > 1 else ""
    model_name = sys.argv[2] if len(sys.argv) > 1 else ""
    src_look_id = sys.argv[3] if len(sys.argv) > 1 else ""

    if not look_name:
        raise Exception("Please provide a look name")

    if not model_name:
        raise Exception("Please provide a model name")

    model, view, fields, fill_fields, sorts, vis_config, filters, filter_expression, filter_config, dynamic_fields,pivots = get_look_info(src_look_id)
    
    query_id = create_query(model_name, view, fields, fill_fields, sorts, vis_config,filters,filter_expression,filter_config,dynamic_fields,pivots).id

    look_result = create_look(look_name, query_id, folder_id)

    print("[Look ID : "+look_result.id+"] is Created at Folder [Name : "+look_result.folder.name+" / ID : "+look_result.folder_id+"]")


def get_look_info(look_id:str) :
    look = sdk.look(look_id=look_id)

    model=look.query.model
    view=look.query.view
    fields=look.query.fields
    fill_fields=look.query.fill_fields
    sorts=look.query.sorts
    vis_config=look.query.vis_config
    filters = look.query.filters
    filter_expression = look.query.filter_expression
    filter_config = look.query.filter_config
    dynamic_fields = look.query.dynamic_fields
    pivots=look.query.pivots

    return model, view, fields, fill_fields, sorts, vis_config, filters, filter_expression, filter_config,dynamic_fields,pivots


def create_query(
    model:str,
    view:str,
    fields:list,
    fill_fields:list,
    sorts:list,
    vis_config:list,
    filters:list,
    filter_expression:list,
    filter_config:list,
    dynamic_fields:list,
    pivots:list
    ):
    
    response = sdk.create_query(
        body=models.WriteQuery(
            model = model,
            view = view,
            fields=fields,
            fill_fields=fill_fields,
            sorts=sorts,
            vis_config=vis_config,
            filters=filters,
            filter_expression=filter_expression,
            filter_config=filter_config,
            dynamic_fields = dynamic_fields,
            pivots = pivots,
            query_timezone="Asia/Seoul"
        )
    )

    return(response)


def create_look(
    look_name:str,
    query_id:str,
    folder_id:str
    ):

    response = sdk.create_look(
        body=models.WriteLookWithQuery(
            title=look_name,
            query_id=query_id,
            folder_id=folder_id
        )
    )   

    return response




if __name__ == '__main__':

    os.environ["LOOKERSDK_BASE_URL"] = "@@@@@" #If your looker URL has .cloud in it (hosted on GCP), do not include :19999 (ie: https://your.cloud.looker.com).
    os.environ["LOOKERSDK_API_VERSION"] = "4.0" #As of Looker v23.18+, the 3.0 and 3.1 versions of the API are removed. Use "4.0" here.
    os.environ["LOOKERSDK_VERIFY_SSL"] = "true" #Defaults to true if not set. SSL verification should generally be on unless you have a real good reason not to use it. Valid options: true, y, t, yes, 1.
    os.environ["LOOKERSDK_TIMEOUT"] = "120" #Seconds till request timeout. Standard default is 120.

    #Get the following values from your Users page in the Admin panel of your Looker instance > Users > Your user > Edit API keys. If you know your user id, you can visit https://your.looker.com/admin/users/<your_user_id>/edit.
    os.environ["LOOKERSDK_CLIENT_ID"] =  "@@@@@" #No defaults.
    os.environ["LOOKERSDK_CLIENT_SECRET"] = "@@@@@" #No defaults. This should be protected at all costs. Please do not leave it sitting here, even if you don't share this document.

    print("All environment variables set.")


    sdk = looker_sdk.init40()
    sdk.update_session({"workspace_id":"dev"})

    #src_look_id="@@@@@"
    folder_id="@@@@@"
    

    main(folder_id)
