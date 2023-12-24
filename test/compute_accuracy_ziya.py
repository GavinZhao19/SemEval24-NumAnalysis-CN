import json
import re

def read_json_file(file_path):
    # 读取JSON文件
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def extract_output_letter(text):
    # 从output中提取正确选项的字母
    match = re.search(r'正確的選項是: \((\w)\)', text)
    return match.group(1) if match else None

def extract_response_letter(text):
    # 从response中提取答案字母，从后向前查找第一个符合格式的字母
    for match in re.finditer(r'\((\w)\)', text):
        pass  # 遍历所有匹配项，最后一个匹配项会被返回
    return match.group(1) if match else None

def extract_response_letter2(text):
    # 从response中提取答案字母，适应不同的格式，如“(C)”、“C)”或“答案：C”
    matches = list(re.finditer(r'\(?([A-D])\)?(?=[^A-D]*$)', text))
    return matches[-1].group(1) if matches else None


def calculate_accuracy(data):
    # 计算正确率
    correct_count = 0
    incorrect_ids = []

    for item in data:
        output = item["output"]["value"]
        output_letter = extract_output_letter(output)
        response = item["response"]["text"]
        response_letter = extract_response_letter2(response)

        if output_letter and response_letter and output_letter == response_letter:
            correct_count += 1
        else:
            incorrect_ids.append(item.get('message_id', ''))

    accuracy = correct_count / len(data) * 100 if data else 0
    return accuracy, incorrect_ids

def write_incorrect_ids_to_file(incorrect_ids, file_path):
    # 将错误的message_id写入文本文件
    with open(file_path, 'w', encoding='utf-8') as file:
        for id in incorrect_ids:
            file.write(f"{id}\n")

# 示例使用
json_file_path = 'test/ziya_responses.json'  # 替换为你的JSON文件路径
incorrect_ids_file_path = 'incorrect_ids_ziya.txt'

data = read_json_file(json_file_path)
accuracy, incorrect_ids = calculate_accuracy(data)
write_incorrect_ids_to_file(incorrect_ids, incorrect_ids_file_path)

print(f"Accuracy: {accuracy}%")
