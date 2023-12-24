import json
import random
import string
from tqdm import tqdm

# 生成16位随机数字字符串作为message_id
def generate_message_id():
    return ''.join(random.choices(string.digits, k=16))

# 原始 JSON 文件路径
input_json_file = 'data/train.json'
# 新 JSON 文件路径
output_json_file = 'output.json'

# 读取原始 JSON 文件
with open(input_json_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 修改数据结构并生成新的字典列表
new_data = []
for item in tqdm(data):
    # 合并文章内容
    article_content = ''.join(item['news_article'])

    # 创建新字典
    new_dict = {
        "message_id": generate_message_id(),
        "instruction": "你是總結大師，需要閱讀下面文章，從四個選項中選出正確的選項，選項內容都為數字，填在問題的___中，使整個句子符合文章表達的意思。\n",
        "input": {
            "from": "user",
            "metadata": "",
            "value": ""
        },
        "output": {
            "from": "assistant",
            "metadata": "",
            "value": ""
        },
        "history": []
    }

    # 在新字典中添加问题和选项  問題：文章內容：選項：文章可以總結成四個部分：針對問題：正確的選項是
    question_stem = item['question_stem'].strip()
    answer_options = item['answer_options']
    ans = int(item['ans'])

    new_dict['input']['value'] += "文章內容：\n" + article_content + "\n問題：" + question_stem + "\n選項："
    for idx, option in enumerate(answer_options):
        new_dict['input']['value'] += f"({chr(65 + idx)}) {option}; "
    new_dict['input']['value'] += "\n"

    # 设置 output 的 value
    output_value = "文章與數字相關的內容可以總結成四個部分："
    sentences_containing = item['sentences_containing_the_numeral_in_answer_options']
    for idx, sentence_list in enumerate(sentences_containing):
        output_value += f"({chr(65 + idx)}) {''.join(sentence_list)}; "
    
    new_dict['output']['value'] += output_value + "針對問題：" + question_stem + " 四個選項：" 
    for idx, option in enumerate(answer_options):
        new_dict['output']['value'] += f"({chr(65 + idx)}) {option}; "
    new_dict['output']['value'] += " \n正確的選項是: " + f"({chr(65 + ans)}) {answer_options[ans]}"

    new_data.append(new_dict)

# 写入新 JSON 文件
with open(output_json_file, 'w', encoding='utf-8') as file:
    json.dump(new_data, file, ensure_ascii=False, indent=4)
