import json 
  
def main(dify_json_str: str) -> dict: 
    """ 
    解析Dify返回的JSON字符串，处理必填项校验和字段提取 
    :param dify_json_str: Dify返回的JSON字符串 
    :return: 解析后的字典，包含是否成功的标识 
    """ 
    # 初始化默认值，避免异常时变量未定义 
    time = "" 
    platform = "" 
    creator = "" 
    companystore = "" 
    taskId = "" 
    
    try: 
        # 移除可能存在的Markdown代码块标记
        clean_json_str = dify_json_str.strip()
        if clean_json_str.startswith('```json'):
            clean_json_str = clean_json_str[7:]
        if clean_json_str.startswith('```'):
            clean_json_str = clean_json_str[3:]
        if clean_json_str.endswith('```'):
            clean_json_str = clean_json_str[:-3]
        clean_json_str = clean_json_str.strip()
        
        result = json.loads(clean_json_str) 
        # 检查必填项是否齐全 
        if result.get("error_msg"): 
            return { 
                "success": False, 
                "message": result["error_msg"], 
                "time": '', 
                "platform":'', 
                "creator":'', 
                "companystore":'', 
                "taskId":'' 
            } 
        # 提取有效数据 
        time = result.get("time", "") 
        platform = result.get("platform", "") 
        creator = result.get("creator", "") 
        companystore = result.get("company_store", "") 
        taskId = result.get("task_id", "") 
        
        return { 
            "success": True, 
            "message": "信息提取成功", 
            "time": time, 
            "platform":platform, 
            "creator":creator, 
            "companystore":companystore, 
            "taskId":taskId 
        } 
    except json.JSONDecodeError: 
        return { 
            "success": False, 
            "message": "解析返回数据失败，请检查格式", 
            "time": time, 
            "platform":platform, 
            "creator":creator, 
            "companystore":companystore, 
            "taskId":taskId 
        }