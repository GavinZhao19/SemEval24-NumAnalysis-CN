import json

def save_formatted_json(input_file_path, output_file_path):
    """
    读取JSON文件并将格式化后的数据保存到另一个文件。
    
    参数:
    input_file_path: str - 原始JSON文件的路径。
    output_file_path: str - 保存格式化JSON数据的文件路径。
    """
    try:
        # 打开并读取JSON文件
        with open(input_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 格式化JSON数据
        formatted_json = json.dumps(data, indent=4, ensure_ascii=False)

        # 将格式化后的数据写入到新文件
        with open(output_file_path, 'w', encoding='utf-8') as new_file:
            new_file.write(formatted_json)
    
    except FileNotFoundError:
        print("文件未找到，请检查路径。")
    except json.JSONDecodeError:
        print("文件不是有效的JSON格式。")

# 示例文件路径
input_file_path = 'data/new-task/DryRun_Numerical_Reasoning.json'
output_file_path = 'formatted_DryRun_Numerical_Reasoning.json'

# 调用函数
save_formatted_json(input_file_path, output_file_path)