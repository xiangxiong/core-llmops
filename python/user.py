import json
import requests
import time
from collections import Counter

def main(arg1: dict) -> dict:
    
    # 输入数据
    input_data = arg1;
    
    # 通用请求头
    headers = {
        'appId': '836021804215570432',
        'Authorization': 'Basic c2FiZXI6c2FiZXJfc2VjcmV0',
        'sec-ch-ua-platform': '"Windows"',
        'Referer': '',
        'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'scc-auth': 'bearer eyJ0eXAiOiJKc29uV2ViVG9rZW4iLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJpc3N1c2VyIiwiYXVkIjoiYXVkaWVuY2UiLCJ0ZW5hbnRfaWQiOiIxMDAwMDAxIiwiZGVwdF9jb2RlIjoiIiwidXNlcl9pZCI6IjE4IiwidXNlcl9uYW1lIjoiYml1Yml1Yml1IiwiZW52IjoidWF0IiwiZGVwdF9pZCI6Ii0xIiwiYWNjb3VudCI6ImJpdWJpdWJpdSIsInJvbGVfaWRzIjoiW3tcInJvbGVJZFwiOjgzNjAyNTk1NDM0OTM1NTAwOCxcInRlbmFudElkXCI6LTEsXCJ0ZW5hbnRDb2RlXCI6XCJcIixcImRhdGFTY29wZVwiOjEsXCJyb2xlVHlwZVwiOjEsXCJjaGFubmVsU2NvcGVcIjotMSxcImRlcHREVE9MaXN0XCI6W10sXCJjaGFubmVsRFRPTGlzdFwiOltdfV0iLCJjbGllbnRfaWQiOiJzYWJlciIsImV4cCI6MTc2NTIyMDQwMCwibmJmIjoxNzY1MTU3NjgyfQ.hX-bL4Tvn6x9zIZee4mzNO0NzmS7MOZXacgCuH46qs0'
    }

    print(f"发送的请求头 input_data: {input_data}")
    
    # 第一步：获取所有taskId
    # 支持两种输入格式：1. 字典包含arg1键 2. 直接传入列表
    input_list = input_data['arg1'] if isinstance(input_data, dict) else input_data
    task_ids = [item['taskId'] for item in input_list]
    print(f"提取的taskIds: {task_ids}")
    
    # 最终汇总的列表
    final_records = []
    
    # 第二步和第三步：遍历每个taskId，发起请求
    for task_id in task_ids:
        print(f"\n处理taskId: {task_id}")
        
        # 第二个请求：deptCollectPageList
        url1 = 'https://mall-admin-uat.lbxcn.com/scc-finance/finance/reconciliation/result/deptCollectPageList'
        data1 = {
            "_t": int(time.time() * 1000),
            "appId": "836021804215570432",
            "current": 1,
            "isPage": 1,
            "page": 1,
            "pageSize": 100,
            "roleId": "836025954349355008",
            "taskId": task_id,
            "tenantId": 1000001,
            "userId": "18"
        }
        
        print(f"发送的请求数据: {data1}")
        print(f"发送的请求头: {headers}")
        print(f"发送的请求URL: {url1}")

        try:
            response1 = requests.post(url1, headers=headers, json=data1)
            response1.raise_for_status()
            result1 = response1.json()
            
            if result1.get('success'):
                # 获取第二个请求的records
                records1 = result1.get('data', {}).get('records', [])
                print(f"第二个请求返回的records数量: {len(records1)}")
                
                # 遍历第二个请求的records，获取每个taskId并发起第三个请求
                for record1 in records1:
                    sub_task_id = record1.get('taskId')
                    erp_dept_id = record1.get('erpDeptId')
                    if sub_task_id:
                        # 第三个请求：pageList
                        url2 = 'https://mall-admin-uat.lbxcn.com/scc-finance/finance/reconciliation/result/pageList'
                        data2 = {
                            "appId": "836021804215570432",
                            "current": 1,
                            "erpDeptId": erp_dept_id,
                            "isPage": 1,
                            "page": 1,
                            "pageSize": 10000,
                            "roleId": "836025954349355008",
                            "taskId": sub_task_id,
                            "tenantId": 1000001,
                            "userId": "18"
                        }

                        print(f"第三个请求发送的请求数据: {data2}")
                        print(f"第三个请求url2的请求数据: {url2}")
                        print(f"第三个请求data2发送的请求数据: {data2}")

                        try:
                            response2 = requests.post(url2, headers=headers, json=data2)
                            response2.raise_for_status()
                            result2 = response2.json()
                            
                            if result2.get('success'):
                                # 获取第三个请求的records并汇总
                                records2 = result2.get('data', {}).get('records', [])
                                print(f"第三个请求返回的records数量: {len(records2)}")
                                final_records.extend(records2)
                            else:
                                print(f"第三个请求失败: {result2.get('msg')}")
                        except requests.exceptions.RequestException as e:
                            print(f"第三个请求异常: {e}")
            else:
                print(f"第二个请求失败: {result1.get('msg')}")
        except requests.exceptions.RequestException as e:
            print(f"第二个请求异常: {e}")
    
    # 统计remark出现次数
    remark_counter = Counter()
    for record in final_records:
        if 'remark' in record and record['remark'] and record['remark'].strip():
            remark = record['remark'].strip()
            remark_counter[remark] += 1
    
    # 生成echarts饼状图配置
    pie_data = [
        {
            "name": remark,
            "value": count
        }
        for remark, count in remark_counter.items()
    ]
    
    echarts_option = {
        "title": {
            "text": "调账原因分布",
            "left": "center"
        },
        "tooltip": {
            "trigger": "item",
            "formatter": "{b}: {c} ({d}%)"
        },
        "legend": {
            "orient": "vertical",
            "left": "left",
            "data": [item["name"] for item in pie_data]
        },
        "series": [
            {
                "name": "调账原因",
                "type": "pie",
                "radius": "50%",
                "center": ["50%", "60%"],
                "data": pie_data,
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)"
                    }
                },
                "label": {
                    "show": True,
                    "formatter": "{b}: {d}%"
                }
            }
        ]
    }

    # 生成输出文件
    output = "```echarts\n" + json.dumps(echarts_option, ensure_ascii=False, indent=2) + "\n```"
    
    return {
        "result": output
    }