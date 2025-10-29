import argparse
import os
import shutil
import subprocess

from generate_test_case import generate_test_case

def compare_outputs(test_case_id):
    """对比两个输出的文件是否完全一致"""
    host_output = f"host_output/output_{test_case_id}.txt"
    user_output = f"user_output/output_{test_case_id}.txt"
    
    try:
        with open(host_output, 'r', encoding='utf-8') as f_host, \
             open(user_output, 'r', encoding='utf-8') as f_user:
            host_lines = f_host.readlines()
            user_lines = f_user.readlines()
            
            if len(host_lines) != len(user_lines):
                return False
            
            for host_line, user_line in zip(host_lines, user_lines):
                if host_line.strip() != user_line.strip():
                    return False
            
            return True
    except FileNotFoundError:
        return False

def run_java_jar(java_code_path, test_case_id, output_dir):
    """运行Java JAR文件"""
    input_file = f"input_data/input_{test_case_id}.txt"
    
    # 查找JAR文件
    if not os.path.exists(java_code_path):
        return False
    
    jar_files = [f for f in os.listdir(java_code_path) if f.endswith('.jar')]
    if not jar_files:
        print(f"No JAR file found in {java_code_path}")
        return False
    
    jar_file = os.path.join(java_code_path, jar_files[0])
    
    try:
        output_file = f"{output_dir}/output_{test_case_id}.txt"
        with open(input_file, 'r', encoding='utf-8') as f_in, \
             open(output_file, 'w', encoding='utf-8') as f_out:
            subprocess.run(
                ["java", "-jar", jar_file],
                stdin=f_in,
                stdout=f_out,
                check=True,
                encoding='utf-8'
            )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def main():
    parser = argparse.ArgumentParser(description="A test suite for Java programs with comparison.")
    parser.add_argument("--host_path", type=str, default="host_code",
                        help="The path to the host Java code directory. (default: host_code)")
    parser.add_argument("--user_path", type=str, default="user_code",
                        help="The path to the user Java code directory. (default: user_code)")
    parser.add_argument("-n", "--num_tests", type=int, default=10, 
                        help="The number of test cases to generate and run. (default: 10)")
    parser.add_argument("-op", "--num_operations", type=int, default=100, 
                        help="The number of operations per test case. (default: 100)")
    
    args = parser.parse_args()

    host_code_path = args.host_path
    user_code_path = args.user_path
    num_test_cases = args.num_tests
    num_operations = args.num_operations

    # <----------------------- 生成测试用例 ----------------------->
    
    print("--- Generating test cases ---")
    input_dir = "input_data"
    if os.path.exists(input_dir):
        shutil.rmtree(input_dir)
    os.makedirs(input_dir)

    for i in range(1, num_test_cases + 1):
        generate_test_case(i, num_operations)
    
    print("\n--- Running host code ---")
    # 创建host输出目录
    host_output_dir = "host_output"
    if os.path.exists(host_output_dir):
        shutil.rmtree(host_output_dir)
    os.makedirs(host_output_dir)
    
    # 运行host代码
    for i in range(1, num_test_cases + 1):
        success = run_java_jar(host_code_path, i, host_output_dir)
        if not success:
            print(f"Host code failed for test case {i}.")
            continue
        print(f"Host test case {i} completed.")
    
    print("\n--- Running user code ---")
    # 创建user输出目录
    user_output_dir = "user_output"
    if os.path.exists(user_output_dir):
        shutil.rmtree(user_output_dir)
    os.makedirs(user_output_dir)
    
    # 运行user代码
    for i in range(1, num_test_cases + 1):
        success = run_java_jar(user_code_path, i, user_output_dir)
        if not success:
            print(f"User code failed for test case {i}.")
            continue
        print(f"User test case {i} completed.")
    
    # <----------------------- 对比输出 ----------------------->
    print("\n--- Comparing outputs ---")
    mismatched = []
    
    for i in range(1, num_test_cases + 1):
        if compare_outputs(i):
            print(f"Test case {i} PASSED.")
        else:
            print(f"Test case {i} FAILED.")
            mismatched.append(i)
    
    # <----------------------- 输出最终结果 ----------------------->
    print("\n" + "="*50)
    if mismatched:
        print(f"不一致的测试用例编号: {mismatched}")
    else:
        print("全部一致！所有测试用例都通过了对比。")
    print("="*50)

if __name__ == "__main__":
    main()
