from openai import OpenAI
import os,requests,json
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from tools import url2domain
from tools import doEmbedding
load_dotenv()

## 在serper.dev申请
XAPIKEY = os.environ.get("XAPI")
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
### 譬如：小白喜欢红牡丹，那么问题来了，小红喜欢什么？
def reWriteQuestion(question):
    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "理解问题后，退一步思考去掉无关偏见和误导信息，仅关注问题本身。将问题转化成2个可以用于搜索引擎搜索的关键词,使用空格隔开,以便我可以用于google进行搜索.只需要说关键词，不需要说其他内容"},
        {"role": "user", "content": question}
    ]
    )

    write_to_file("intention.txt",question.strip() + " -> " + completion.choices[0].message.content + "\n")
    print(completion.choices[0].message.content)
    return(completion.choices[0].message.content)

## 2. 重写问题
### 譬如：小白喜欢红牡丹，那么问题来了，小红喜欢什么？

def reWriteQuestionInEnglish(question):
    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "理解问题后，退一步思考去掉无关偏见和误导信息，仅关注问题本身。将问题转化成2个可以用于搜索引擎搜索的英语关键词,使用空格隔开,以便我可以用于google进行搜索.只需要说关键词，不需要说其他内容"},
        {"role": "user", "content": question}
    ]
    )

    write_to_file("intention.txt",question.strip() + " -> " + completion.choices[0].message.content + "\n")
    print(completion.choices[0].message.content)
    return(completion.choices[0].message.content)

## 理解问题,重新描述问题.
def underStandQuestion(question):
    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "理解以下问题，退一步思考去掉无关偏见和误导信息，仅关注名词主语本身。使用另外3种不同的名词及描述方式重新表达同一个问题，只表达新的描述方式，不要说其他无关内容"},
        {"role": "user", "content": question}
    ]
    )

    write_to_file("understand.txt",question.strip() + " -> " + completion.choices[0].message.content + "\n\n\n")
    print(completion.choices[0].message.content)
    return(completion.choices[0].message.content)

## 理解问题,重新描述问题.
def underStandQuestioninEnglish(question):
    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "理解以下问题，退一步思考去掉无关偏见和误导信息，仅关注名词主语本身。使用另外1种英文表达方式重新表达同一个问题，只表达新的描述方式，不要说其他无关内容。"},
        {"role": "user", "content": question}
    ]
    )

    write_to_file("understand.txt",question.strip() + " -> " + completion.choices[0].message.content + "\n\n\n")
    print(completion.choices[0].message.content)
    return(completion.choices[0].message.content)

## 3. 获取搜索引擎单页面结果(略)
def html_to_markdown(url):
    try:
        response = requests.get(url)
        response.encoding = response.apparent_encoding  # 自动检测编码
        response.raise_for_status()  # 确保请求成功
        soup = BeautifulSoup(response.text, 'html.parser')

        markdown_content = ""

        # 抽取并转换标题
        if soup.title:
            markdown_content += f"# {soup.title.string}\n\n"

        # 抽取并转换段落
        for p in soup.find_all('p'):
            markdown_content += f"{p.get_text()}\n\n"
        
        write_to_file("filecontent.txt","================="+url+"=========================\n")
        write_to_file("filecontent.txt",markdown_content)

        return markdown_content
    except requests.RequestException as e:
        return f"Error: {e}"

## 4. 检索搜索引擎，并获得全文内容.
def searchWeb(keyword,question):
    url = "https://google.serper.dev/search"
    payload = json.dumps(
        [
        {
            "q": keyword,
            "num": 10
        }

        ]
    )
    headers = {
    'X-API-KEY': XAPIKEY,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    num = 0
    
    md = json.loads(response.text)
    for gg in (md):
        for item in gg['organic']:
            print(item['link'])
            ## 下面是记录日志到URL.txt
            write_to_file("URL.txt",item['link'])
            ## 拉黑的域名，不用看.
            if blackListHost(item['link']):
                print("blacklistURL:" + item['link'])
                continue
            
            completeContent = html_to_markdown(item['link']).replace("\n","").replace("  ","")
            if len(completeContent) > 0:
                segments = doEmbedding.findsimillar(completeContent,question)
                if  segments != "[没找到匹配内容]":
                    aa.append(segments)
                    num = num + 1
                else:
                    write_to_file("toBlackListHOST.txt",item['link'])
                if num >= 3:
                    break


## 4. 检索搜索引擎，并获得全文内容.
def searchWebInEnglish(keyword,question):
    url = "https://google.serper.dev/search"
    payload = json.dumps(
        [
        {
            "q": keyword,
            "num": 20
        }

        ]
    )
    headers = {
    'X-API-KEY': XAPIKEY,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    num = 0
    
    md = json.loads(response.text)
    for gg in (md):
        for item in gg['organic']:
            print(item['link'])
            ## 下面是记录日志到URL.txt
            write_to_file("URL.txt",item['link'])

            ## 拉黑的域名，不用看.
            if blackListHost(item['link']):
                print("blacklistURL:" + item['link'])
                continue

            completeContent = html_to_markdown(item['link']).replace("\n","").replace("  "," ")
            if len(completeContent) > 0:
                segments = doEmbedding.findsimillar(completeContent,question)
                if  segments != "[没找到匹配内容]":
                    aa.append(segments)
                    num = num + 1
                else:
                    write_to_file("toBlackListHOST.txt",item['link'])
                if num >= 3:
                    break

def domainInWhitelist(url):
    whitelist = ["",
                 "",
                 "",
                 ]
    host = url2domain.extract_domain(url)
    


## 常用的记录内容到文件.
def write_to_file(filename,content):
    ## 'URL.txt'
    with open(filename, 'a+', encoding='utf-8') as file:
        file.write(content+"\n")

def hasAsked(question):
    try:
        with open("intention.txt", 'r', encoding='utf-8') as file:
            for line in file:
                if question.strip() in line:
                    return True
        return False
    except FileNotFoundError:
        print(f"文件 {question} 未找到。")
        return False

## 检索答案合成
def AnswerGen(aa,question,originquestion):
    while len(aa) < 3:
        aa.append("no")
    
    realQuestion = """
使用提供的由三重引号引起来的文章，并用简单的中文，完整地回答问题。如果在文章中找不到答案，请写“我找不到答案”。

\"\"\"{}\"\"\"
\"\"\"{}\"\"\"
\"\"\"{}\"\"\"

问题：{}
========
格式如下:
问题: [内容]
答案: [内容]
""".format(aa[0],aa[1],aa[2],question)
    
    print(realQuestion)

    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "作为一个严谨的AI助手，你总是会使用简单的表达方式，完整并且相关地描述问题的答案."},
        {"role": "user", "content": realQuestion}
    ]
    )

    write_to_file("QNA.txt","================")
    write_to_file("QNA.txt","原问题:"+originquestion)
    write_to_file("QNA.txt",completion.choices[0].message.content.replace("\"\"\"",""))
    # write_to_file("QNA.txt","问题:"+originquestion)
    # write_to_file("QNA.txt","答案:"+completion.choices[0].message.content.replace("\"\"\"",""))
    print("原问题:"+originquestion)
    print(completion.choices[0].message.content.replace("\"\"\"",""))

def blackListHost(url):
   host = url2domain.extract_domain(url)
   if host in ["helpguide.org",
               "mindtools.com",
               "www.helpguide.org",
               "zju.edu.cn",
               "cyol.com",
               "mafengwo.cn",
               "ctrip.com",
               "toshopping.com.cn",
               "swjtu.edu.cn",
               "163.com",
               ]:
       return True
   else:
       return False
    


## 如果想要批处理，可以用这个函数(用来优化基础能力.)
def batchMain():
    toAsk = [
        # "什么是爱情",
        # "什么是强化学习",
        # "曹雪芹是谁，有什么著作？",
        # "摧毁一个孩子有多简单？",
        "要怎样努力，才能成为很厉害的人？",
        "怎么才能停止自己脑子里的胡思乱想？",
        "如何不痛苦地早起？",
        "你觉得自己牛在哪儿？为什么会这样觉得？",
        "如何成为一个优秀的男朋友？",
        "排名在前 1% 的高中生是靠天赋还是靠努力？",
        "怎么提高表达能力？",
        "如何提高自己的为人处世能力？",
        "大学看哪些书比较适合？",
        "人在迷茫时该干什么？",
        "如何成长为一个高情商的人？",
        "怎样看待美国仇华情绪？",
        "有哪些典型的「学生思维」？",
        "女朋友的哪些缺点最让男性受不了？",
    ]
    for question in toAsk:
        if hasAsked(question):
            continue
        else:
            underStandQuestion(question)
            # keyword = reWriteQuestion(question)
            # searchWeb(keyword,question)
            # AnswerGen(aa,question)
            # askMoreQuestion(question)


## 从question.txt中批量读取问题.
def batchMainFromFile():
    with open("question.txt", 'r', encoding='utf-8') as file:
        for question in file:
            if hasAsked(question):
                continue
            else:
                print(question)
                keyword = reWriteQuestionInEnglish(question)
                searchWeb(keyword,question)

def main(question):
    # question = input("输入你要查询的问题:")
    print("下面重写关键词======")
    keyword = reWriteQuestion(question)
    print("下面进行web搜索得到答案======")
    searchWeb(keyword,question)
    print("下面生成合成内容======")
    AnswerGen(aa,question,question)
    # print("下面生成3个新问题======")
    # askMoreQuestion(question)

def mainInEnglish(question):
    # question = input("输入你要查询的问题:")
    print("下面重写关键词======")
    englishQuestion = underStandQuestioninEnglish(question)
    keyword = reWriteQuestionInEnglish(englishQuestion)
    print("下面进行web搜索得到答案======")
    searchWebInEnglish(keyword,englishQuestion)
    print("下面生成合成内容======")
    AnswerGen(aa,englishQuestion,question)
    # print("下面生成3个新问题======")
    # askMoreQuestion(question)

# 评测PROMPT：
## 相关性：
# 请评估下面的答案部分是否与问题相关？如果回答了，请回复“是的”，如果无关，请回复“没有”。
# 问题：依恋一个人是一种什么样子的状态？
# 答案：依恋一个人是一种个体与其形成牢固情感纽带的倾向，能为个体提供安全和安慰的状态。

## 完整性：
# 请评估下面的答案部分是否完整回答问题？如果回答完整，请回复“是的”，如果不完整，请回复“没有”。
# 问题: 如何培养高情商？
# 答案: 发展情商是一个持续的过程。这个旅程因人而异。然而，根据安德鲁斯的说法，以下行动可能会让你更加自我意识。

## 自我反思并改进:
# 请反思下面的答案部分是否完整回答问题？如果完整，请返回原文。如果没有，请使用简单的描述表达方式补全缺失内容，直接提供补充完整的问题和答案。
# 输出格式如下:
# 问题: [内容]
# 答案: [内容]
# ---------------------------
# 问题: 如何培养高情商？
# 答案: 培养情商是一个持续的过程，每个人的旅程都不同。然而，根据安德鲁斯的说法，以下行动可能会让你更加自我认识：情商、自我认知、自我管理、动机、同理心、社交技能。情商简而言之，是个人如何识别和管理自己的情绪，以及如何应对他人情绪的能力。

## 直接回复问题(有哪些典型问题需要先查询？)
# 使用最简单而深刻的表达方式回答下面问题
# ------
# 喜欢和爱情的区别是什么？

def test():
    aa.append(". However, these concepts differ, and to decipher the feeling you have, you need to know the difference between like and love.Keep reading to understand like vs. love properly. Irrespective of your feelings for someone")
    aa.append(". The difference between liking and loving someone goes beyond simple language and explores the complex worlds of intimacy, connection, and human emotions. In order to identify these differences, one must make their way through the maze of emotions and encounters that characterize these unique loves。有人说小白喜欢小红，我认为这是无稽之谈。")
    aa.append("喜欢和爱情的区别在于深度和承诺。喜欢是一种愉悦和欣赏，通常是短暂和表面的；而爱情则是一种深刻的情感，包含了责任、牺牲和长久的承诺。喜欢可以是对某个人的某些特质感兴趣，而爱情则是全心全意地接受和支持对方。")
    AnswerGen(aa,"小红喜欢小白吗？","小红喜欢小白吗？")


aa = []
# mainInEnglish("喜欢和爱情的区别是什么？")
# main("喜欢和爱情的区别是什么？")
main("喜欢和爱情的区别是什么？")



#### 难回答问题:
## 问题：杭州有什么小众且好玩的景点？
## 问题：最近有什么好电影值得推荐？
## 问题：今天有什么最新科技新闻？
## 问题：什么是强化学习？
## 问题：什么是喜欢？


# test()

# url = "http://hz.bendibao.com/tour/202097/92977.shtm"
# print(html_to_markdown(url))