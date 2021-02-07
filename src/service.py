import json
import os
import sys
from env_setup import getPassword
from autocorrelation import getBuildingDF,getBuildingCases,getAutoCorrelationByBuild,predictAreaCase
def handler(event, context):
    try:
        service_password = os.environ['SERVICE_PASS']
    except KeyError:
        # path not yet set
        getPassword()
        service_password = os.environ['SERVICE_PASS']

    try:
        input_pass = json.loads(event["body"] or "{}").get("password","wrong")
        input_method = json.loads(event["body"] or "{}").get("method",None)
    except:
        input_pass = event["body"].get("password","wrong")
        input_method = event["body"].get("method",None)
    print(input_pass)
    if  input_pass != service_password:
        message = "Wrong Password"
        status_code = 403
        print("check")
    else:
        message,status_code = "Place Holder",200
        case_df = getBuildingDF()
        if input_method == "autocorrelation":
            message = json.dumps(getAutoCorrelationByBuild(case_df))
        elif input_method == "prediction":
            ranked_correlation = getAutoCorrelationByBuild(case_df)
            message = json.dumps(predictAreaCase(ranked_correlation,case_df))
        elif input_method == "stats":
            message = getBuildingCases(case_df).to_json()
        else:
            message = "couldn't understand the method"
            status_code = 500

    # Check date format
    return {
        "statusCode": status_code,
        "headers": { "Content-Type": "application/json"},
        "body": message
    }