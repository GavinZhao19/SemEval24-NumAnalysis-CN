import json
import re
from transformers import AutoTokenizer, AutoModel
from tqdm import tqdm
import torch
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "2"
# 加载模型
tokenizer = AutoTokenizer.from_pretrained("checkpoint-8000", trust_remote_code=True)
model = AutoModel.from_pretrained("checkpoint-8000", trust_remote_code=True, device='cuda')
# 确保模型使用指定的GPU
model = model.to('cuda')
model = model.eval()

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def process_data(json_data, output_file):
    for item in tqdm(json_data[1000:1500]):
        instruction = item['instruction']
        input_text = item['input']['value']
        input_sentence = f"\n{instruction}\n{input_text}\n"
        print(input_sentence)

        # 模型生成回应
        response, _ = model.chat(tokenizer, input_sentence, history=[])

        # 将生成的回应添加到每个条目的字典中
        item['response'] = response

        # 实时写入文件
        with open(output_file, 'a', encoding='utf-8') as file:
            json.dump(item, file, ensure_ascii=False, indent=4)
            file.write("\n")  # 为每个条目添加换行符，以便于阅读

# 主逻辑
file_path = 'test.json'
output_file = 'processed_data_3.json'  # 处理后的数据将写入此文件
json_data = read_json(file_path)
process_data(json_data, output_file)