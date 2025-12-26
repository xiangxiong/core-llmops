import unittest
import sys
import os

# 将当前目录添加到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from express1 import main

class TestExpress1(unittest.TestCase):
    def test_main_function(self):
        """测试 main 函数是否能正常执行并返回预期结果"""
        result = main("test")
        
        # 验证返回值是字典类型
        self.assertIsInstance(result, dict)
        
        # 验证返回值包含预期的键
        if "data" in result and "list" in result["data"]:
            # 验证 list 是列表类型
            self.assertIsInstance(result["data"]["list"], list)
            print(f"测试通过: main 函数返回了 {len(result['data']['list'])} 条订单数据")
        else:
            # 验证空结果的格式
            self.assertIn("result", result)
            self.assertIsInstance(result["result"], list)
            print("测试通过: main 函数返回了空结果，格式正确")

if __name__ == "__main__":
    unittest.main()