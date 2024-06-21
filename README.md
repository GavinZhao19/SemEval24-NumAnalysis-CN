# SemEval24-NumAnalysis-CN • [![twitter](https://img.shields.io/twitter/url/https/shields.io.svg?style=social)](https://x.com/nicolayr_/status/1803707694169100397)
![](https://img.shields.io/badge/Python-3.10-lightgreen.svg)
[![twitter](https://img.shields.io/twitter/url/https/shields.io.svg?style=social)](https://x.com/nicolayr_/status/1803705227108847866)

**SemEval-2024 Task 7 - NumEval: Task 2 - Reading Comprehension of the Numerals in Text (Chinese)**

## Introduction
This repository hosts the development for Task 2 of SemEval-2024's NumEval challenge, focusing on the [reading comprehension of numerals in Chinese text](https://sites.google.com/view/numeval/tasks). Our approach is inspired by the [training strategy outlined in "**Never Lost in The Middle**"-paper](https://arxiv.org/pdf/2311.09198.pdf) and involves constructing a dataset and training a model capable of accurately identifying numerical answers in context.

## Methodology
The training approach follows a Chain of Thought (CoT) methodology, adapting it for numeral-focused language understanding. The original data format consists of a text passage and question options. We transform this into a structured format where the input includes an instruction, the text passage, and the question options. The output consists of a summary of the numerical content in the text, a repetition of the question, the options, and the selected answer.

Key dependencies and highlights include:
- Attention score influence as visualized
![attention_score.png](image/heatmap_attention_score.png)
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
![Eval Loss](image/eval_loss)

![Train Loss](image/train_loss)

![Train Epoch](image/train_epoch)

## Evaluation
The evaluation metrics for the model are detailed below. These metrics were computed based on the performance of the model on a test dataset consisting of 4,000 data points (located in `test/combined_data.json`). The `output` field represents the correct answers, whereas `response` denotes the answers generated by the model. The overall accuracy of the model is **90.12%**. The `message_id` of the incorrect responses can be found in the `incorrect_ids.txt` file (`test/incorrect_ids.txt`).

Additionally, results from the `Ziya-13B-v1.1` model are available in the `test/ziya_responses.json` file. Incorrect responses from this model are listed in the `test/incorrect_ids_ziya.txt` file. The accuracy rate for the `Ziya-13B-v1.1` model is **43.9%**.

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

## Test
**Downloading Model Weights:** The model weights can be downloaded from the following URL: 
https://huggingface.co/GavinZhao23/NumAnalysis-Chatglm3-6B (Now set private)
<img width="1298" alt="image" src="https://github.com/GavinZhao19/SemEval24-NumAnalysis-CN/assets/133320285/6cf9e5b9-f809-4a58-b7dd-f39ea389654d">

```python
from transformers import AutoTokenizer, AutoModel
tokenizer = AutoTokenizer.from_pretrained("GavinZhao23/NumAnalysis-Chatglm3-6B", trust_remote_code=True)
model = AutoModel.from_pretrained("GavinZhao23/NumAnalysis-Chatglm3-6B", trust_remote_code=True, device='cuda')
model = model.eval()
input_sentence = input_sentence = """
<|system|>
你是總結大師，需要閱讀下面文章，從四個選項中選出正確的選項，選項內容都為數字，填在問題的___中，使整個句子符合文章表達的意思。
<|user|>
文章內容：
麗清(3346)公布2016年4月合併營收2.21億元，月增8.1%、年減4.75%；累計1至4月合併營收8.98億元、年減1.88%。麗清表示，4月雖受清明連假致使工作天數較少，但營收表現仍較上月成長，在於主要客戶長城汽車4月在中國新車市場保持熱銷，而公司為長城汽車Tier 1(一階)供應商，因此，在長城汽車保持良好銷售表現下，亦帶動整體備貨力道持續增溫。展望第二季，麗清保持審慎樂觀看法；公司表示，第一季部分客戶訂單遞延，預期在第二季起將逐步恢復正常，可望為營運表現增添助力；此外，中國新車銷售市場在購置稅減半政策下，使得小車與售價較低的中國自主品牌車廠展現良好銷售表現，成為帶動整體中國新車市場的主要成長動力。麗清表示，公司為中國最大SUV品牌車廠長城汽車之Tier 1供應商，並供應長城汽車全車系LED車燈產品，可望隨著長城汽車持續推出更多購車優惠、刺激銷量表現下，創造未來整體營運逐季成長的動力；此外，旗下主要客戶尚包括上海小糸、廣州小糸等中國主要Tier 1車燈供應商，合計市占率達三成，隨著各品牌車廠針對汽車電子朝向安全、智慧化以及節能減碳的配備趨勢不變，將有助公司掌握良好的訂單能見度，並站穩中國最大LED車燈廠地位。
問題：麗清4月營收月增8%；Q___接單回穩料為營運添助力
選項：(A) 1; (B) 1.88; (C) 2.21; (D) 4; 
<|assistant|>

"""
response, history = model.chat(tokenizer, input_sentence, history=[])
print(response)
>>>
文章與數字相關的內容可以總結成四個部分：
(A) 累計1至4月合併營收8.98億元而公司為長城汽車Tier 1(一階)供應商公司為中國最大SUV品牌車廠長城汽車之Tier 1供應商廣州小糸等中國主要Tier 1車燈供應商; (B) 年減1.88%; (C) 麗清(3346)公布2016年4月合併營收2.21億元; (D) 麗清(3346)公布2016年4月合併營收2.21億元累計1至4月合併營收8.98億元4月雖受清明連假致使工作天數較少在於主要客戶長城汽車4月在中國新車市場保持熱銷;
針對問題：麗清4月營收月增8%；Q___接單回穩料為營運添助力 四個選項：(A) 1; (B) 1.88; (C) 2.21; (D) 4;
正確的選項是: (B) 1.88
```

### Test examples
```text
Right answer:  15

input:
<|system|>
你是總結大師，需要閱讀下面文章，從四個選項中選出正確的選項，選項內容都為數字，填在問題的___中，使整個句子符合文章表達的意思。
<|user|>
文章內容：\n受惠臨床檢驗業務遞增式成長，F-合富(4745)去年12月營收達2.32億元，去年第四季營收5.92億元，季增0.68%，全年營收25.8億元，年增15%，其中，臨床檢驗業務貢獻突破20億元，年成長三成。法人估計，該公司去年每股稅後盈餘將超過5元，再創歷年新高。事實上，受到大陸政府審批作業流程影響，F-合富去年放射腫瘤業務僅認列兩台機台銷售，低於前一年度的三台，但整體營收還能繳出兩位數的年增成長，主要功臣來自臨床檢驗業務；去年12月該事業群營收貢獻達2.1億元，年成長63%，全年營收貢獻更首度突破20億元達20.56億元，年成長30.2%，達內部上修後預期的高標，佔整體營收比重也逼近八成。而該公司近兩年臨床檢驗業務成長加速，主要受益於中國醫改政策及層峰計畫的合作醫院增加，且隨合富代理銷售的營業規模逐年增加，也可取得與原廠較好的交易條件，因此利潤空間也放大。法人也估計，以合富上季營收5.92億元，略優於去年第三季的5.88億元，且產品比重差距不大下，上季獲利有機會略優於前季，去年全年每股稅後盈餘可望超過5元，再創歷年新高。為加速新事業佈局，F-合富去年第四季董事會也通過辦理4億元可轉換公司債，去年底送件後，如果沒有問題，下周可望申報生效，內部預期，整體籌資可望於農曆年後完成。\n問題：F-合富去年營收增___%，臨床檢驗業務年增3成\n選項：(A) 12; (B) 15; (C) 20; (D) 20.56; \n
<|assistant|>

output:
文章與數字相關的內容可以總結成四個部分：(A) F-合富(4745)去年12月營收達2.32億元去年12月該事業群營收貢獻達2.1億元; (B) 年增15%; (C) 臨床檢驗業務貢獻突破20億元全年營收貢獻更首度突破20億元達20.56億元; (D) 全年營收貢獻更首度突破20億元達20.56億元; 針對問題：F-合富去年營收增___%，臨床檢驗業務年增3成 四個選項：(A) 12; (B) 15; (C) 20; (D) 20.56;  \n正確的選項是: (B) 15
```

```text
Right answer:  4

input:
<|system|>
你是總結大師，需要閱讀下面文章，從四個選項中選出正確的選項，選項內容都為數字，填在問題的___中，使整個句子符合文章表達的意思。
<|user|>
文章內容：\n西柏(3541)今(2016)年8月營收創歷史新高，主因為北美第2大客戶拉貨旺，且有前月部分出貨遞延至8月所帶動，法人表示，9月營收估較前月修正，整體第3季營收可優於前季，毛利率也看季成長，惟受到費用較高，以及業外匯損影響，單季獲利估僅略優於前季表現，第4季因第2大客戶拉貨告一段落，單季營收表現估較前季修正。西柏為專業影音產品製造商，以HDBaseT及HDMI產品為大宗，目前ODM約佔7成、OEM約佔2成、品牌佔近1成；市場營收結構方面，美洲佔66%、歐洲23%、亞洲4%、其餘為其他。受惠北美第1、2大客戶拉貨暢旺所帶動，西柏上半年營收達8.43億元、年增29.39%，營業利益1.43億元、年增38.28%，EPS達2.50元、優於2015年同期的1.90元。西柏今年8月營收達2.12億元，月增54.23%、年增99.80%，創歷史新高，主因為北美第2大客戶拉貨旺，且有前月部分出貨遞延至8月所帶動，法人表示，9月營收估較前月修正，整體第3季營收可優於前季，由於經濟規模提升，毛利率也看季成長，惟受到RD以及參展費用較高，以及業外匯損影響，單季獲利估僅略優於前季表現。法人表示，第4季第1大客戶拉貨持穩，不過第2大客戶拉貨高峰已告一段落，因此整體來看，單季營收表現估較前季修正。全年來看，法人表示，受惠北美第1大客戶今年出貨展望正向，以及第2大客戶出貨表現明顯成長下，今年西柏營收估增逾3成，不過因費用較高(調薪、RD費用增加)，且業外可能有匯損，因此估獲利成長幅度低於營收增幅。西柏近年切入在專業影音具高市佔率的北美品牌客戶，2014年已小量出貨，2015年下單金額約達近億元，隨雙方合作已有一定基礎，今年下單量逐步提升；以今年上半年來看，該客戶下單金額較去年同期大幅成長數倍，並已躍居為西柏第2大客戶。法人表示，西柏第2大客戶今年出貨以延長器為主，明年則有機會出貨ASP(產品平均單價)較佳的分配器、切換器等產品，整體而言，明年該客戶下單金額可持續成長，有機會成為西柏第一大客戶。\n問題：西柏Q3有匯損影響；Q___營收估較前季修正\n選項：(A) 2.12; (B) 2.50; (C) 3; (D) 4; \n

<|assistant|>

output:
文章與數字相關的內容可以總結成四個部分：(A) 西柏今年8月營收達2.12億元; (B) EPS達2.50元; (C) 整體第3季營收可優於前季整體第3季營收可優於前季今年西柏營收估增逾3成; (D) 第4季因第2大客戶拉貨告一段落亞洲4%第4季第1大客戶拉貨持穩; 針對問題：西柏Q3有匯損影響；Q___營收估較前季修正 四個選項：(A) 2.12; (B) 2.50; (C) 3; (D) 4;  \n正確的選項是: (D) 4
```

# References 

You can cite this work as follows:
```bibtex
@article{Junzhe2024nclnlp,
  title={A CoT-Based SFT Training Strategy with Large Language Models for Number-Focused Headline Generation},
  booktitle = "Proceedings of the Annual Conference of the North American Chapter of the Association for Computational Linguistics",
  author={Junzhe, Zhao and Yingxi, Wang and Huizhi, Liang and Nicolay, Rusnachenko},
  year= "2024",
  month= jun,
  address = "Mexico City, Mexico",
  publisher = "Association for Computational Linguistics"
}
```
