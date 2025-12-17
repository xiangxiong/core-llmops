import json

# 测试不同格式的输入
markdown_json = "```json\n{\n    \"time\": \"2025-09\"\n}\n```"
pure_json = "{\"time\": \"2025-09\"}"

print("测试Markdown格式的JSON字符串:")
try:
    result = json.loads(markdown_json)
    print(f"成功解析: {result}")
except Exception as e:
    print(f"解析失败: {type(e).__name__}: {e}")

print("\n测试纯JSON字符串:")
try:
    result = json.loads(pure_json)
    print(f"成功解析: {result}")
except Exception as e:
    print(f"解析失败: {type(e).__name__}: {e}")
