import json
from collections import Counter

def main(json_str: str) -> list:
    # 解析JSON数据
    data = json.loads(json_str)
    results = data.get("result", [])
    
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
    echarts_data = []
    for error, count in error_counter.items():
        echarts_data.append({"name": error, "value": count})
    
    # 输出ECharts数据
    print("ECharts饼图数据:")
    print(json.dumps(echarts_data, ensure_ascii=False, indent=2))
    
    # 保存ECharts数据到文件
    with open('echarts_pie_data.json', 'w', encoding='utf-8') as f:
        json.dump(echarts_data, f, ensure_ascii=False, indent=2)
    
    print("\nECharts数据已保存到: echarts_pie_data.json")
    
    # 返回最终数据
    return echarts_data

# 测试数据
if __name__ == "__main__":
    # 从文件中读取JSON数据
    with open('test_data.json', 'r', encoding='utf-8') as f:
        json_data = f.read()
    # 调用main函数并获取返回值
    result = main(json_data)
    # 验证返回值
    print("\n函数返回值类型:", type(result))
    print("函数返回值数量:", len(result))
