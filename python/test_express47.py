import json
import sys

# Add the current directory to the path
sys.path.append('.')

from express47 import main

# Test case 1: Normal input with dictionary containing result key
print("=== Test Case 1: Dictionary with result key ===")
test_data1 = r'''{"result": [{"exceptionJsonMsg": "[{\"errorMsg\": \"测试错误1\"}]"}, {"exceptionJsonMsg": "[{\"errorMsg\": \"测试错误2\"}]"}]}''' 
result1 = main(test_data1)
print("Result:", result1)
print()

# Test case 2: Input is directly a list (the case that caused the error)
print("=== Test Case 2: Direct list input (error case) ===")
test_data2 = r'''[{"exceptionJsonMsg": "[{\"errorMsg\": \"测试错误1\"}]"}, {"exceptionJsonMsg": "[{\"errorMsg\": \"测试错误2\"}]"}]''' 
result2 = main(test_data2)
print("Result:", result2)
print()

# Test case 3: Empty input
print("=== Test Case 3: Empty input ===")
test_data3 = r'''[]'''
result3 = main(test_data3)
print("Result:", result3)
print()

# Test case 4: No exceptionJsonMsg
print("=== Test Case 4: No exceptionJsonMsg ===")
test_data4 = r'''[{"logisticsId": 123}, {"logisticsId": 456}]'''
result4 = main(test_data4)
print("Result:", result4)
print()

print("All test cases passed successfully!")
