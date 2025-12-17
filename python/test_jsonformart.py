import json
from jsonFormart import main

# 测试用例
test_input = {
    "dify_json_str": "```json\n{\n    \"time\": \"2025-09\",\n    \"platform\": \"753844372306399235\",\n    \"creator\": \"\",\n    \"company_store\": \"\",\n    \"task_id\": \"\",\n    \"error_msg\": \"\"\n}\n```"
}

# 调用函数并打印结果
result = main(test_input['dify_json_str'])
print(result)
