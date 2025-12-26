import json
from collections import Counter

def main(json_str: str) -> dict:
    # 解析JSON数据
    data = json.loads(json_str)
    # 处理两种情况：1. data是字典有result字段 2. data直接是列表
    if isinstance(data, dict):
        results = data.get("result", [])
    else:
        results = data
    
    # 提取errorMsg
    error_messages = []
    for result in results:
        exception_json = result.get("exceptionJsonMsg")
        if exception_json:
            exceptions = json.loads(exception_json)
            for exc in exceptions:
                error_msg = exc.get("errorMsg")
                if error_msg:
                    error_messages.append(error_msg)
    
    # 统计errorMsg
    error_counter = Counter(error_messages)
    
    # 生成ECharts饼图数据格式
    pie_data = []
    for error, count in error_counter.items():
        pie_data.append({"name": error, "value": count})
    
    # 生成完整的ECharts饼图配置结构
    echarts_pie_config = {
        "title": {
            "text": "快递异常原因分布",
            "left": "center",
            "top": 20
        },
        "tooltip": {
            "trigger": "item",
            "formatter": "{a} <br/>{b}: {c} ({d}%)"
        },
        "series": [
            {
                "name": "异常原因",
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
                }
            }
        ]
    }
    
    # 输出ECharts饼图配置
    print("ECharts饼图配置结构:")
    print(json.dumps(echarts_pie_config, ensure_ascii=False, indent=2))
    
        # 生成输出文件
    output = "```echarts\n" + json.dumps(echarts_pie_config, ensure_ascii=False, indent=2) + "\n```"

    # 返回最终数据
    return {
        "result":output
    }