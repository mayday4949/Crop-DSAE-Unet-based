import openai
import os

# 设置OpenAI API密钥
openai.api_key = "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"

# GPT-3生成文本的函数
def generate_text(prompt):
    # 调用OpenAI API生成文本
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=10,
        stop=None,
        temperature=0.5,
    )

    # 提取生成的文本并返回
    texts = [choice.text.strip() for choice in response.choices]
    return texts

# 获取用户输入
prompt = input("请输入一段文本，我们将生成10个相似的文本：\n")

# 生成相似的文本
texts = generate_text(prompt)

# 打印生成的文本
print("以下是10个相似的文本：")
for i, text in enumerate(texts):
    print(f"{i+1}. {text}")