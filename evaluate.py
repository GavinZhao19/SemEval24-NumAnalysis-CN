import json
import re
from transformers import AutoTokenizer, AutoModel

# 加载模型
tokenizer = AutoTokenizer.from_pretrained("checkpoint-8000", trust_remote_code=True)
model = AutoModel.from_pretrained("checkpoint-8000", trust_remote_code=True, device='cuda')
model = model.eval()
def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def extract_answer(text):
    match = re.search(r"\((A|B|C|D)\) .+", text)
    return match.group() if match else None

def process_data(json_data):
    results = []
    for item in json_data:
        instruction = item['instruction']
        input_text = item['input']['value']
        input_sentence = f"<|system|>\n{instruction}<|user|>\n{input_text}<|assistant|>\n"

        # 模型生成回应
        response, _ = model.chat(tokenizer, input_sentence, history=[])

        generate_answer = extract_answer(response)
        org_answer = extract_answer(item['output']['value'])

        is_correct = generate_answer == org_answer
        results.append({
            'generate_answer': generate_answer,
            'org_answer': org_answer,
            'is_correct': is_correct
        })

    return results

def calculate_accuracy(results):
    correct_count = sum(result['is_correct'] for result in results)
    return correct_count / len(results)

# 主逻辑
file_path = 'test.json'
json_data = read_json(file_path)
processed_data = process_data(json_data)
accuracy = calculate_accuracy(processed_data)
print(f"Accuracy: {accuracy * 100:.2f}%")