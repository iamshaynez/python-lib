
import os
import re
from dotenv import load_dotenv
from openai import OpenAI
import json
import pandas as pd
from ConfigCenter import R2Config
# In your terminal please set your environment variables by running the following lines of code.
# export 'CONSUMER_KEY'='<your_consumer_key>'
# export 'CONSUMER_SECRET'='<your_consumer_secret>'
load_dotenv()

config = R2Config()
twitter_json = config.read_json(f'twitter_poetry.json')
consumer_key = twitter_json['CONSUMER_KEY']
consumer_secret = twitter_json["CONSUMER_SECRET"]
access_token = twitter_json["ACCESS_TOKEN"]
access_token_secret = twitter_json["ACCESS_TOKEN_SECRET"]


openai_json = config.read_json(f'openai_{os.environ["OPENAI_ACCOUNT"]}.json')
openai_api_key = openai_json['OPENAI_API_KEY']
openai_base_url = openai_json['OPENAI_BASE_URL']

def split_paragraphs(filename):
    # 读取文件内容
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 使用正则表达式查找特定的模式
    # 这个模式匹配形如[]{#index_split_000.html#p15} A 的行
    pattern = r"\[\]\{#[^}]*\}.*"
    
    # 使用找到的模式拆分文件内容
    # 我们拆分的标准是找到的模式和之前的任何一个非空字符之间
    paragraphs = re.split(pattern, content)
    
    # 移除结果数组中可能存在的空字符串
    paragraphs = [para for para in paragraphs if para.strip()]
    
    return paragraphs

def json_list_to_excel(json_list, output_filename):
    # 将 JSON 列表转换为 DataFrame
    df = pd.DataFrame(json_list)
    
    # 将 DataFrame 保存到 Excel 文件
    # 使用 'openpyxl' 引擎来处理 xlsx 文件
    df.to_excel(output_filename, index=False, engine='openpyxl')

def process_paragraph(paragraph):
    text = ""
    image_prompt = ""
    from openai import OpenAI
    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key=openai_api_key, base_url=openai_base_url
    )
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_format={ "type": "json_object" }, temperature=1.0,
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": f"""1. Read the content below regarding one specific god/goddess
        ---
        ```markdown
        {paragraph}
        ```
        ---
        2. Describe the key information of the god/goddess
        3. Print in below json format.

        \`\`\`json
        "nameOfGod": " ",
        "region":" ",
        "dutyInCharge":" ",
        "religion":" ",
        "generalDescription": " "
        \`\`\`"""}
        ]
    )
    #print(response)
    #print(response.choices[0].message.content)
    data = json.loads(response.choices[0].message.content)
    print(f"Name: {data.get('nameOfGod', None)}" )
    return data

def process_paragraphs(paragraphs):
    # 处理每个段落，并收集处理后的结果
    processed_paragraphs = [process_paragraph(para) for para in paragraphs]
    return processed_paragraphs


if __name__ == "__main__":
    #main(ifBing = True)
    print('Starting processing...')
    file_name = "gods.md"
    paragraphs = split_paragraphs(file_name)
    #print(type(paragraphs))
    print(f'paragraphs lens: {len(paragraphs)}')
    print('----')

    json_data = process_paragraph(paragraphs[300])
    print(json_data)
    json_list = process_paragraphs(paragraphs)
    #print(json_para)
    json_list_to_excel(json_list, 'output.xlsx')