import requests
import json

def main(arg1: str) -> dict:
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
    
    result = []
    
    try:
        # 使用json参数代替data参数，requests会自动处理编码和Content-Type
        response = requests.post(url, headers=headers, cookies=cookies, json=data)
        response.raise_for_status()
        result = response.json();
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
    except json.JSONDecodeError:
        print(f"响应不是有效的JSON: {response.text}")
    
    if result and "data" in result and "list" in result["data"]:
        # 遍历result.data.list中的数据，按照要求的结构返回
        formatted_result = []
        for item in result["data"]["list"]:
            # 直接使用API返回的结构，因为已经包含了所有需要的字段
            formatted_item = {
                "logisticsId": item.get("logisticsId"),
                "logisticsExpressId": item.get("logisticsExpressId"),
                "externalId": item.get("externalId"),
                "orderSource": item.get("orderSource"),
                "appointSource": item.get("appointSource"),
                "noodlesSource": item.get("noodlesSource"),
                "orderSourceDescribe": item.get("orderSourceDescribe"),
                "noodlesSourceDescribe": item.get("noodlesSourceDescribe"),
                "appointDescribe": item.get("appointDescribe"),
                "expressStateDescribe": item.get("expressStateDescribe"),
                "expressState": item.get("expressState"),
                "senderCity": item.get("senderCity"),
                "senderCountry": item.get("senderCountry"),
                "exceptionJsonMsg": item.get("exceptionJsonMsg"),
                "senderDetail": item.get("senderDetail"),
                "senderDistrict": item.get("senderDistrict"),
                "senderProvince": item.get("senderProvince"),
                "senderMobile": item.get("senderMobile"),
                "senderName": item.get("senderName"),
                "senderPhone": item.get("senderPhone"),
                "senderTown": item.get("senderTown"),
                "logisticsServices": item.get("logisticsServices"),
                "orderChannelsType": item.get("orderChannelsType"),
                "recipientCity": item.get("recipientCity"),
                "recipientCountry": item.get("recipientCountry"),
                "recipientDetail": item.get("recipientDetail"),
                "recipientDistrict": item.get("recipientDistrict"),
                "recipientProvince": item.get("recipientProvince"),
                "recipientTown": item.get("recipientTown"),
                "recipientMobile": item.get("recipientMobile"),
                "recipientName": item.get("recipientName"),
                "wpCode": item.get("wpCode"),
                "wpCodeName": item.get("wpCodeName"),
                "waybillCode": item.get("waybillCode"),
                "createTime": item.get("createTime"),
                "updateTime": item.get("updateTime"),
                "logisticsCode": item.get("logisticsCode"),
                "sourceShopId": item.get("sourceShopId"),
                "sourceShopName": item.get("sourceShopName"),
                "warehouseCode": item.get("warehouseCode"),
                "channelDeptId": item.get("channelDeptId"),
                "channelDeptName": item.get("channelDeptName"),
                "channelId": item.get("channelId"),
                "channelName": item.get("channelName"),
                "sendChannelDeptId": item.get("sendChannelDeptId"),
                "sendChannelDeptName": item.get("sendChannelDeptName"),
                "sendChannelId": item.get("sendChannelId"),
                "sendChannelName": item.get("sendChannelName"),
                "remarks": item.get("remarks"),
                "orderId": item.get("orderId"),
                "templateUrl": item.get("templateUrl"),
                "templateId": item.get("templateId"),
                "deliveryId": item.get("deliveryId"),
                "logisticsInfoId": item.get("logisticsInfoId"),
                "warehouseName": item.get("warehouseName"),
                "expressEstimatedPrice": item.get("expressEstimatedPrice"),
                "packageEstimatedWeight": item.get("packageEstimatedWeight"),
                "lanshouState": item.get("lanshouState"),
                "lanshouStateTime": item.get("lanshouStateTime"),
                "ruguiStateTime": item.get("ruguiStateTime"),
                "qianshouStateTime": item.get("qianshouStateTime"),
                "lanshouContext": item.get("lanshouContext"),
                "newestState": item.get("newestState"),
                "newestStateTime": item.get("newestStateTime"),
                "newestContext": item.get("newestContext"),
                "logisticsStrategy": item.get("logisticsStrategy"),
                "logisticsStrategyDescribe": item.get("logisticsStrategyDescribe"),
                "interceptCode": item.get("interceptCode"),
                "interceptResult": item.get("interceptResult")
            }
            formatted_result.append(formatted_item)
        return {"result": json.dumps(formatted_result, ensure_ascii=False)}
    return {"result": ""}   # 返回空列表，保持一致的返回类型
