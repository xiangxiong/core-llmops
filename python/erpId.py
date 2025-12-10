import json

def main(arg1:str) -> dict:

    data = json.loads(arg1)

    # Create a list of objects with taskId and erpDeptId keys
    task_objects = [{"taskId": record['taskId'], "erpDeptId": record['erpDeptId']} for record in data['data']['records']]

    return {
        "result": task_objects
    }