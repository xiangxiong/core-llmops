from lastChange import main

# 测试数据
arg1 = {
    "arg1": [
        {"taskId": "test_task_id_1"}
    ]
}
arg2 = "test_auth_token"

# 调用main函数
try:
    result = main(arg1, arg2)
    print(f"函数返回结果: {result}")
    print(f"返回类型: {type(result)}")
except Exception as e:
    print(f"测试过程中出现错误: {e}")
    import traceback
    traceback.print_exc()
