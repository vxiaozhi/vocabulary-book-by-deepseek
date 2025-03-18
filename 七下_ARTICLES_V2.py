import os
import json
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s",
)

# 确定七下单词数据的路径
word_data_file = "data/七下/7下英语单词.json"
result_path = "result/all"
# word_analysis_dir = "data/all/global-words.json"
article_dir = "result/七下_articles"
image_file_path = "https://word.vxiaozhi.com/imgs/word_imgs"

with open(word_data_file, "r", encoding="utf-8") as f:
    words_data = json.load(f)

unit_list = sorted(set([word["unit"] for word in words_data]))

# words_data
# [{
#   "unit": "Unit1 Animal Friends",
#   "num": 1,
#   "word": "fox",
#   "phonetic_symbol": "[fɒks]",
#   "mean": "n.狐狸"
# }],


for target_unit in unit_list:
    print("🚀 ~ file: 七下1.py:31 ~ target_unit:", target_unit)
    target_words = [word for word in words_data if word["unit"] == target_unit]
    # print("🚀 ~ file: 七下1.py:32 ~ target_words:", target_words)
    # print(
    #     "🚀 ~ file: 七下1.py:32 ~ target_words:",
    #     [word["word"] for word in target_words],
    # )

    # 准备Markdown内容
    content = f"""# 2025人教版英语词汇释意助记(DeepSeek版) 七下 {target_unit}

> (使用 DeepSeek 提供单词的词义、词根、例句、辅助记忆、助记图像等信息。)

"""

    # https://www.vxiaozhi.com/imgs/cet4/a/abandon.jpg

    article_file_path = os.path.join(article_dir, f"{target_unit}.md")
    for cur_word in target_words:
        word = cur_word.get("word")
        print("🚀 ~ file: 七下1.py:57 ~ word:", word)
        content += f"""## {word} - {cur_word["mean"]}

### 课本释义

**序号**：{cur_word["num"]}
**音标**：{cur_word["phonetic_symbol"]}
**释义**：{cur_word["mean"]}
"""
        # 读取单词分析数据
        word_json_path = os.path.join(result_path, word[0], f"{word}.json")
        word_image_path = (f"{image_file_path}/{word[0]}/{word}.jpg").lower()
        # print("🚀 ~ file: 七下1.py:62 ~ word_json_path:", word_json_path)
        if os.path.exists(word_json_path):
            with open(word_json_path, "r", encoding="utf-8") as f:
                words_ana_data = json.load(f)
            analysis = words_ana_data.get("analysis", "")
            draw_explain = words_ana_data.get("draw_explain", "")
            # print("🚀 ~ file: 七下1.py:67 ~ draw_prompt:", analysis)
            content += f"""
{analysis}

### 助记图像

{draw_explain}

![{word}]({word_image_path})

"""

        else:
            content += """
[待完善]
"""

    # 生成Markdown文件
    # 写入文件
    with open(article_file_path, "w", encoding="utf-8") as f:
        f.write(content)
        f.write(
            """ \n\n ## 感谢以下开源项目 \n\n- [vocabulary-book-by-deepseek](https://github.com/vxiaozhi/vocabulary-book-by-deepseek) \n\n- [小智晖的AI单词库](https://word.vxiaozhi.com/)"""
        )

# for unit in unit_list:
#     # 创建单词分析的目录
#     unit_dir = os.path.join(word_analysis_dir, unit)
#     if not os.path.exists(unit_dir):
#         os.makedirs(unit_dir)

#     # 遍历文章目录，找到以 unit 为前缀的文件
#     for filename in os.listdir(article_dir):
#         if filename.startswith(unit):
