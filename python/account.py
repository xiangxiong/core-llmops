import json
import requests  # 新增：导入请求库，用于调用HTTP接口

def main(arg1: str) -> dict:
    # 初始化变量，解决作用域问题
    start_date = ""
    table_data = {  # 新增：初始化表格数据结构
        "header": [],  # 表头
        "rows": []     # 行数据
    }
    try:
        # ========== 原有逻辑：解析JSON字符串提取日期 ==========
        arg1_obj = json.loads(arg1)
        start_date = arg1_obj.get("startDate", "")
        
        # ========== 新增逻辑：调用调账任务列表接口 ==========
        # 1. 接口配置
        api_url = "https://mall-admin-uat.lbxcn.com/scc-finance/finance/reconciliation/o2o/task/pageList"
        # 接口入参（可根据解析的start_date动态替换accountDate/time）
        request_data = {
            "accountDate": "2025-10",  # 可替换为start_date的年月部分，如start_date[:7]
            "appId": "836021804215570432",
            "current": 1,
            "isPage": 1,
            "page": 1,
            "pageSize": 10,
            "roleId": "836025954349355008",
            "tenantId": 1000001,
            "time": "2025-10",        # 同上，可动态替换
            "userId": "18"
        }
        # 2. 动态替换日期（可选：用解析的start_date替换固定日期）
        if start_date:  # 若解析到start_date，提取年月（如2025-05-01 → 2025-05）
            year_month = start_date[:7]
            request_data["accountDate"] = year_month
            request_data["time"] = year_month
        
        # 3. 发送POST请求调用接口（添加超时、异常捕获）
        headers = {
            "Content-Type": "application/json",  # 必选：指定JSON格式请求体
            # 可选：添加接口鉴权头，如Token/Cookie（根据实际接口要求补充）
            "scc-auth": "bearer eyJ0eXAiOiJKc29uV2ViVG9rZW4iLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJpc3N1c2VyIiwiYXVkIjoiYXVkaWVuY2UiLCJ0ZW5hbnRfaWQiOiIxMDAwMDAxIiwiZGVwdF9jb2RlIjoiIiwidXNlcl9pZCI6IjE4IiwidXNlcl9uYW1lIjoiYml1Yml1Yml1IiwiZW52IjoidWF0IiwiZGVwdF9pZCI6Ii0xIiwiYWNjb3VudCI6ImJpdWJpdWJpdSIsInJvbGVfaWRzIjoiW3tcInJvbGVJZFwiOjgzNjAyNTk1NDM0OTM1NTAwOCxcInRlbmFudElkXCI6LTEsXCJ0ZW5hbnRDb2RlXCI6XCJcIixcImRhdGFTY29wZVwiOjEsXCJyb2xlVHlwZVwiOjEsXCJjaGFubmVsU2NvcGVcIjotMSxcImRlcHREVE9MaXN0XCI6W10sXCJjaGFubmVsRFRPTGlzdFwiOltdfV0iLCJjbGllbnRfaWQiOiJzYWJlciIsImV4cCI6MTc2NDA5NzIwMCwibmJmIjoxNzY0MDQ3Mzc2fQ.Ssyqrirq9VpBmprY0lTTn5BFFoEdJjTW5CLFNRKexfE",
            # "Cookie": "your_cookie_here"
        }
        response = requests.post(
            url=api_url,
            headers=headers,
            json=request_data,  # 自动序列化JSON，无需手动dumps
            timeout=30  # 超时时间，避免无限等待
        )
        response.raise_for_status()  # 抛出HTTP状态码异常（如404/500）
        
        # 4. 解析接口返回数据
        api_result = response.json()

        print("接口返回数据：", api_result)
        
        # 5. 格式化接口数据为表格结构（需根据接口实际返回字段调整）
        # 假设接口返回结构：{"code":200,"data":{"list":[{...},...],"total":10}}
        if api_result.get("code") == 200 and "records" in api_result.get("data", {}):
            task_list = api_result["data"]["records"]
            if task_list:
                # 提取表头（取第一条数据的所有键作为表头）
                table_data["header"] = list(task_list[0].keys())
                # 提取行数据（按表头顺序组装每行值）
                table_data["rows"] = [
                    [row[col] for col in table_data["header"]] 
                    for row in task_list
                ]
        
        # ========== 返回最终结果 ==========
        return {
            "result": start_date,
            "table_data": table_data,  # 新增：表格数据，供Dify展示
            "success": True,           # 新增：标识接口调用成功
            "error": ""
        }
    
    # 捕获JSON解析错误（原有）
    except json.JSONDecodeError as e:
        return {
            "result": "",
            "table_data": table_data,  # 空表格
            "success": False,
            "error": f"JSON解析失败：{str(e)}"
        }
    # 新增：捕获接口请求异常（网络/超时/HTTP错误）
    except requests.exceptions.RequestException as e:
        return {
            "result": start_date,
            "table_data": table_data,  # 空表格
            "success": False,
            "error": f"接口调用失败：{str(e)}"
        }
    # 捕获其他所有异常（兜底）
    except Exception as e:
        return {
            "result": start_date,
            "table_data": table_data,  # 空表格
            "success": False,
            "error": f"处理失败：{str(e)}"
        }

# ========== 调用示例 ==========
if __name__ == "__main__":
    # 示例1：传入含startDate的JSON字符串（触发动态日期替换）
    test_arg1 = '{"startDate":"2025-10-01","endDate":"2025-10-31"}'
    result1 = main(test_arg1)
    print("示例1 - 解析的日期：", result1["result"])
    print("示例1 - 表格表头：", result1["table_data"]["header"])
    print("示例1 - 表格行数据：", result1["table_data"]["rows"])
    print("示例1 - 执行状态：", result1["success"])
    print("="*50)

    # 示例2：传入非法JSON字符串（触发解析失败）
    test_arg2 = "2025年10月"
    result2 = main(test_arg2)
    print("示例2 - 错误信息：", result2["error"])
    print("示例2 - 表格数据：", result2["table_data"])