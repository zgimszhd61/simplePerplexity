from openai import OpenAI
import os,requests,json
from bs4 import BeautifulSoup

## 在platform.openai.com申请
os.environ["OPENAI_API_KEY"] = "sk-"

## 在serper.dev申请
XAPIKEY = "xxx"
## 1. 问题的举一反三
def askMoreQuestion(question):
    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "根据原始问题提出3个相关且苏格拉底式的进一步问题，注意问题不要重复，有价值的，可以跟进，并写出的每个问题不超过 20 个字。"},
        {"role": "user", "content": question}
    ]
    )

    print(completion.choices[0].message.content)

## 2. 重写问题
def reWriteQuestion(question):
    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "退一步思考，理解问题后，将问题转化成2个可以用于搜索引擎搜索的关键词,使用空格隔开,以便我可以用于google进行搜索.只需要说关键词，不需要说其他内容"},
        {"role": "user", "content": question}
    ]
    )

    print(completion.choices[0].message.content)
    return(completion.choices[0].message.content)

## 3. 获取搜索引擎单页面结果(略)
def html_to_markdown(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 确保请求成功
        soup = BeautifulSoup(response.text, 'html.parser')

        markdown_content = ""

        # 抽取并转换标题
        if soup.title:
            markdown_content += f"# {soup.title.string}\n\n"

        # 抽取并转换段落
        for p in soup.find_all('p'):
            markdown_content += f"{p.get_text()}\n\n"

        return markdown_content
    except requests.RequestException as e:
        return f"Error: {e}"

## 4. 检索搜索引擎，并获得全文内容.
def searchWeb(keyword):
    url = "https://google.serper.dev/search"
    payload = json.dumps(
        [
        {
            "q": keyword,
            "num": 4
        }

        ]
    )
    headers = {
    'X-API-KEY': XAPIKEY,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    
    md = json.loads(response.text)
    for gg in (md):
        for item in gg['organic']:
            print(item['link'])
            completeContent = html_to_markdown(item['link'])
            if len(completeContent) > 0:
                aa.append(completeContent)
            else:
                aa.append("nothing")

## 检索答案合成
def AnswerGen(aa,question):
    realQuestion = """
使用提供的由三重引号引起来的文章来回答问题。 如果在文章中找不到答案，请写“我找不到答案”。

\"\"\"{}\"\"\"
\"\"\"{}\"\"\"
\"\"\"{}\"\"\"

问题：{}
""".format(aa[0],aa[1],aa[2],question)
    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "you are a helpful assistant"},
        {"role": "user", "content": realQuestion}
    ]
    )

    print(completion.choices[0].message.content)

aa = []

def main():
    question = input()
    print("下面重写关键词======")
    keyword = reWriteQuestion(question)
    print("下面进行web搜索得到答案======")
    searchWeb(keyword)
    print("下面生成合成内容======")
    AnswerGen(aa,question)
    print("下面生成3个新问题======")
    askMoreQuestion(question)

main()
