import requests
import json

url = "https://logistics.lbxcn.com/manage/express/orderListB2C"

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Origin": "https://logistics.lbxcn.com",
    "Referer": "https://logistics.lbxcn.com/B2C/expressFace/list",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    "X-Token": "vF_cbdoY83RjFrRJw_PBBp150lKrwbqZ2d__",
    "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"'
}

cookies = {
    "gdp_user_id": "4c64519a-0e92-4697-b630-580e3e6edc08",
    "ajs_user_id": "7c3ac7aaf5c4fb200bbc603d7a2fa50428eb1e41",
    "ajs_anonymous_id": "6765c65f-6c73-4ab1-a7e5-a2b772e75fc1",
    "94b19b09d2877f5a_gdp_esid": "3538",
    "X-Token": "vF_cbdoY83RjFrRJw_PBBp150lKrwbqZ2d__",
    "Admin-Token": "vF_cbdoY83RjFrRJw_PBBp150lKrwbqZ2d__",
    "TokenKey": "X-Token",
    "sidebarStatus": "0"
}

data = {
    "pageNum": 1,
    "pageSize": 20,
    "isPage": 1,
    "expressState": "12",
    "orderStartTime": "2025-12-26 00:00:00",
    "orderEndTime": "2025-12-26 23:59:59"
}

try:
    # 使用json参数代替data参数，requests会自动处理编码和Content-Type
    response = requests.post(url, headers=headers, cookies=cookies, json=data)
    response.raise_for_status()
    result = response.json()
    print(json.dumps(result, ensure_ascii=False, indent=2))
except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")
except json.JSONDecodeError:
    print(f"响应不是有效的JSON: {response.text}")
