# SemEval24-NumAnalysis-CN
**SemEval-2024 Task 7 - NumEval: Task 2 - Reading Comprehension of the Numerals in Text (Chinese)**

## Introduction
This repository hosts the development for Task 2 of SemEval-2024's NumEval challenge, focusing on the reading comprehension of numerals in Chinese text (https://sites.google.com/view/numeval/tasks). Our approach is inspired by the training strategy outlined in paper (https://arxiv.org/pdf/2311.09198.pdf) and involves constructing a dataset and training a model capable of accurately identifying numerical answers in context.

## Methodology
The training approach follows a Chain of Thought (CoT) methodology, adapting it for numeral-focused language understanding. The original data format consists of a text passage and question options. We transform this into a structured format where the input includes an instruction, the text passage, and the question options. The output consists of a summary of the numerical content in the text, a repetition of the question, the options, and the selected answer.

Key dependencies and highlights include:
- Attention score influence as visualized [here](https://huggingface.co/IDEA-CCNL/Ziya-Reader-13B-v1.0/tree/main).
- Base model: `ChatGLM3`.
- Comparative models for future evaluation include `GPT-3.5-Turbo`, `Gemini-Pro`, and `Ziya-13B-v1.1`.

## Data Construction Format
The data for this project is constructed using a specific format to facilitate effective training and accurate comprehension of numerals in text. The format is divided into two main parts - Input and Output:

Input Format:
- Instruction: A brief directive explaining what needs to be done with the text and question (你是總結大師，需要閱讀下面文章，從四個選項中選出正確的選項，選項內容都為數字，填在問題的___中，使整個句子符合文章表達的意思。\n).
- Text Passage: news_article
- Question Options: question_stem + answer_options

Output Format:
- Summary of Numerals in Text: sentences_containing_the_numeral_in_answer_options
- Repetition of the Question: question_stem
- Repetition of Question Options: answer_options
- Selected Answer: ans + target_num

An example of the original dataset is as follows:
```json
{
        "news_article": [
            "美國頁岩油敗事有餘，但成事卻不足。過去1年半以來，頁岩油打破石油輸出國組織（OPEC）壟佔的局面，讓油價一路從每桶一百美元跌至40美元不到。不過，頁岩油開始減產後卻無法即時令油價起死回升，瑞士信貸預言低油價情形恐至少持續至2020年。",
            "低油價反映全球需求不足，但供給持續增加，瑞士信貸表示，原油市場需透過低油價的市場力量，一方面刺激需求、另一方面抑制產出來達成供需再平衡。（BusinessInsider）",
            "瑞士信貸主要假設情境預測，油價可能在35美元附近觸底，大約在65美元左右達成供需平衡，不過期間的不確定風險仍然很多。",
            "全球石油業者今年飽受低油價之苦，裁員、減支消息屢屢見報，眼看今年油價復甦無望，法國Total與英國BP等石油公司都將被迫再次勒緊褲袋。據能源顧問公司Rystad Energy估計，今年全球石油天然氣業者資本支出將再砍22%，成為六年新低的5,220億美元。（路透社）",
            "＊編者按：本文僅供參考之用，並不構成要約、招攬或邀請、誘使、任何不論種類或形式之申述或訂立任何建議及推薦，讀者務請運用個人獨立思考能力，自行作出投資決定，如因相關建議招致損失，概與《精實財經媒體》、編者及作者無涉。"
        ],
        "question_stem": "挖苦阿！低油價還有五年，能源投資___恐再砍兩成                                                       ",
        "answer_options": [
            "2020",
            "35",
            "40",
            "65"
        ],
        "ans": 0,
        "target_num": "2020",
        "sentences_containing_the_numeral_in_answer_options": [
            [
                "瑞士信貸預言低油價情形恐至少持續至2020年"
            ],
            [
                "油價可能在35美元附近觸底"
            ],
            [
                "讓油價一路從每桶一百美元跌至40美元不到"
            ],
            [
                "大約在65美元左右達成供需平衡"
            ]
        ]
    }
```

An example of the preprocessed dataset is as follows:
```json
{
    "message_id": "8898315043651790",
    "instruction": "你是總結大師，需要閱讀下面文章，從四個選項中選出正確的選項，選項內容都為數字，填在問題的___中，使整個句子符合文章表達的意思。\n",
    "input": {
        "from": "user",
        "metadata": "",
        "value": "文章內容：\n普氏能源資訊7月8日報導，沙烏地阿拉伯投資銀行賈瓦投資公司（Jadwa Investment）報告表示，沙國第二季原油日均加工量年增每日23.5萬桶或12%，主要因為該國延布煉油廠（Yasref）量產至完全產能（每日40萬桶）的帶動，並預估今年第三季的原油加工量可以達到每日300萬桶。延步煉油廠是由沙國國家石油公司（Saudi Aramco）持股62.5%，以及大陸中石化（Sinopec）持股37.5%的合資企業。沙國國內原油需求增加可能會減損其出口能力。 賈瓦投資表示，沙國第二季的原油日產量年增6%至1,030萬桶，2015全年日均產量預估為980萬桶，日均出口量預估持平於700萬桶，國內原油日均消費量則預估為270萬桶。沙烏地阿拉伯國家石油公司執行理事Ahmed Al-Subaey表示，沙國原油日產量處於歷史最高水平，同時，由於夏季用電高峰的到來，沙國國內原油消耗也達到高峰；儘管如此，以沙國現有的儲量和產能，完全可以進一步提升產量，滿足全球範圍內原油需求增長。 根據美國能源部，沙國是全球最大的原油出口國，並且擁有全球最高的原油產能，其證實石油儲量佔全球的16%。沙國有半數的石油儲量位於該國最大的八處油田當中，其中加瓦爾油田（Ghawar）是世界最大油田，儲量達到750億桶，在全球僅次於七個國家。沙國也擁有全球第五大的天然氣儲量，但該國天然氣的產量有限。 普氏能源資訊7月6日公佈的調查顯示，石油輸出國組織（OPEC）6月份原油日產量較前月增加17萬桶達到3,128萬桶，為連續第四個月增加，並且創下2012年8月以來的近三年新高，主要是受到沙烏地阿拉伯以及伊拉克產量增長的帶動。6月份，沙國原油日產量持續增加至1,035萬桶，因該國夏季的用電高峰帶動石油發電的需求增加、國內煉油廠新增產能需求更多的原油，以及沙國在國際市場上持續捍衛其出口份額的影響。 \n問題：沙國Q3國內原油加工量預估將達每日___萬桶\n選項：(A) 270; (B) 300; (C) 40; (D) 62.5; \n"
    },
    "output": {
        "from": "assistant",
        "metadata": "",
        "value": "文章與數字相關的內容可以總結成四個部分：(A) 國內原油日均消費量則預估為270萬桶; (B) 並預估今年第三季的原油加工量可以達到每日300萬桶; (C) 主要因為該國延布煉油廠（Yasref）量產至完全產能（每日40萬桶）的帶動; (D) 延步煉油廠是由沙國國家石油公司（Saudi Aramco）持股62.5%; 針對問題：沙國Q3國內原油加工量預估將達每日___萬桶 四個選項：(A) 270; (B) 300; (C) 40; (D) 62.5;  \n正確的選項是: (B) 300"
    },
    "history": []
}
```


## Training
The current training regimen is set for 10 epochs. However, due to an observed increase in eval loss starting from epoch 6, the training was halted early. 
```text
epoch: 10
batch size: 64
gpus: 16
learning rate: 1e-6
warmup ratio: 0.01
```

## Evaluation
The evaluation metrics are as follows:
```json
{
    "predict_bleu-4": 4.4259450000000005,
    "predict_rouge-1": 22.057102999999998,
    "predict_rouge-2": 15.536357999999998,
    "predict_rouge-l": 15.456871000000001,
    "predict_runtime": 74.7412,
    "predict_samples_per_second": 1.338,
    "predict_steps_per_second": 0.054
}
```