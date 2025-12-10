import json
import erpId

# Test data with erpDeptId field
test_data = {
    "data": {
        "records": [
            {"taskId": "1", "erpDeptId": "dept1"},
            {"taskId": "2", "erpDeptId": "dept2"},
            {"taskId": "3", "erpDeptId": "dept3"}
        ]
    }
}

# Convert test data to JSON string
arg1 = json.dumps(test_data)

# Call the main function
result = erpId.main(arg1)

# Print the result
print("Test Result:")
print(json.dumps(result, indent=2))

# Verify the result
assert "result" in result, "Result key not found in response"
assert isinstance(result["result"], list), "Result is not a list"
assert len(result["result"]) == 3, "Result list length mismatch"

for i, item in enumerate(result["result"]):
    assert "taskId" in item, f"taskId not found in item {i}"
    assert "erpDeptId" in item, f"erpDeptId not found in item {i}"
    assert item["taskId"] == test_data["data"]["records"][i]["taskId"], f"taskId mismatch in item {i}"
    assert item["erpDeptId"] == test_data["data"]["records"][i]["erpDeptId"], f"erpDeptId mismatch in item {i}"

print("All tests passed!")