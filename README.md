# OOpre hw6 Difference评测机

## 用前须知

`user_code`文件夹里直接放你的java代码构建的jar

## 用法

在评测机目录下打开终端，输入：

```shell
python main.py -n <测试次数> -op <每次测试生成多少条指令>
```

e.g.

```shell
python main.py -n 10 -op 2000
```

## 注意

一次评测结束后，根目录下会生成以下目录：

`input_data`：输入样例

`host_output`：笔者的输出

`user_output`：你的输出

## 输出示例

```shell
--- Generating test cases ---
--- Running host code ---
Host test case 1 completed.
...

--- Running user code ---
User test case 1 completed.
...

--- Comparing outputs ---
Test case 1 PASSED.
Test case 2 FAILED.
...

==================================================
不一致的测试用例编号: [2, 5, 8]
==================================================
```