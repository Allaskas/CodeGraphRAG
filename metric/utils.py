import javalang
import os


# 获取项目中所有的 Java 文件并按相对路径结构返回
def get_all_java_files_with_path(directory):
    java_files = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):
                # 计算文件的相对路径
                relative_path = os.path.relpath(os.path.join(root, file), directory)
                java_files[relative_path] = os.path.join(root, file)
    return java_files
