import json
import random

# 读取第一个 JSON 文件
with open('output.json', 'r', encoding='utf-8') as file:
    data1 = json.load(file)

# 读取第二个 JSON 文件
with open('output2.json', 'r', encoding='utf-8') as file:
    data2 = json.load(file)

# 合并两个数据集
combined_data = data1 + data2

# 打乱数据
random.shuffle(combined_data)

# 分割数据集
valid_set = combined_data[:4000]
test_set = combined_data[4000:8000]
train_set = combined_data[8000:]

# 将分割后的数据集写入新的文件
with open('train.json', 'w', encoding='utf-8') as file:
    json.dump(train_set, file, ensure_ascii=False, indent=4)

with open('valid.json', 'w', encoding='utf-8') as file:
    json.dump(valid_set, file, ensure_ascii=False, indent=4)

with open('test.json', 'w', encoding='utf-8') as file:
    json.dump(test_set, file, ensure_ascii=False, indent=4)
