from utils import get_all_java_files_with_path

if __name__ == "__main__":
    original_project_directory = "/data/sanglei/反模式修复数据集构建/extract_antipatterns_and_repair/final/CH/apache/doris/commit_1600/29/score_repair_success_0.8/static_after"
    refactored_project_directory = "/data/sanglei/CodeGraphRAG/tmp/ch/apache/doris/commit_1600/29/ap_cg_full"
    original_code_files = get_all_java_files_with_path(original_project_directory)
    refactored_code_files = get_all_java_files_with_path(refactored_project_directory)
    print(f"original_code_files: {original_code_files}")
    print(f"refactored_code_files: {refactored_code_files}")
