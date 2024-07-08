import re
# !pip install openai
import os
import openai
from dotenv import load_dotenv
import uuid
import numpy as np
load_dotenv()

def cosine_similarity(vector1, vector2):
    """
    计算两个向量之间的余弦相似度
    """
    dot_product = np.dot(vector1, vector2)
    norm_vector1 = np.linalg.norm(vector1)
    norm_vector2 = np.linalg.norm(vector2)
    return dot_product / (norm_vector1 * norm_vector2)


def find_most_similar_text(embeddings, query_embedding):
    """找到与查询嵌入最相似的文本"""
    similarities = [cosine_similarity(query_embedding, emb) for emb in embeddings]
    most_similar_index = np.argmax(similarities)
    return most_similar_index, similarities[most_similar_index]




def findsimillar(mmtext,question):
# mmtext = "#禁书《金瓶梅》的真正作者是谁？_王世贞由内容质量、互动评论、分享传播等多维度分值决定，勋章级别越高()，代表其在平台内的综合表现越好。《金瓶梅》是一部惊世奇书，也是“明代四大奇书”之一，还被清代小说点评家张竹坡誉为“第一奇书”。它借《水浒传》中“武松杀嫂”一节引出以西门庆为主角的一段市井生活，借宋代的人物暴露明代社会的腐败。一般认为书名是以西门庆三个重要女人名字中的各一个字拼凑成的。“金”指潘金莲，“瓶”指李瓶儿，“梅”指庞春梅。这本书思想内容丰富、艺术手法娴熟，但是它问世时，作者并没有署上自己的真实姓名，所以学者们对它的作者问题始终抱有很大的兴趣，以至《金瓶梅》的作者到底是谁，迄今仍然无定论。《金瓶梅》的作者署名“兰陵笑笑生”，但其真名实姓考证至今并无定论，作者是何方人氏也说法不一。因为作者声称写的是山东地面的人和事，署名中又有“兰陵”字眼，加之作品用语基本上是北方话，所以多认为是山东人。有的研究者认为作者是李开先。李开先是山东人，嘉靖进士，40岁罢官回家，他的身世、生平和对词曲等市井文学的极深的爱好和修养与前人对《金瓶梅》的说法不谋而合；作品本身也证明它同李开先关系密切；李开先的作品《宝剑记》也是用《水浒》的故事，把《金瓶梅》和李开先的《宝剑记》作比较，就会发现不少相同之处。所以《金瓶梅》和《三国演义》、《水浒传》、《西游记》一样，都是在民间艺人中长期流传之后，经作家个人写定的，而这个写定者就是李开先。还有人认为作者是另一个山东人贾三近，他是嘉靖、万历年间大文学家，因为《金瓶梅》一书从头到尾贯穿了大量的峄县人仅用的方言俚语，峄古称兰陵，从贾三近的生平事迹，以及宦游处所、人生经历、嗜好、著作目录等方面看，他是最接近“兰陵笑笑生”的一个人。最流行的看法则认为，嘉靖年间的大文学家王世贞是《金瓶梅》的作者。王世贞，字元美，号凤洲，又号燕州山人，是南京刑部尚书，也是明代著名的文学家、史学家。王世贞才学富赡，文名满天下，与李攀龙、谢榛等合称为“后七子”。在前后七子中最博学多才。李攀龙去世后，他独领文坛20年。《明史》称他“才最高、地望最显，声华意气，笼盖海内”。他为官清正，不附权贵。东林党杨继盛被严嵩陷害下狱，他经常送汤药，又代杨妻草疏。杨被害后，他为杨殓葬；父亲被严嵩陷害，他作长诗《袁江流钤山冈》和《太保歌》等，揭露严嵩父子的罪恶。他精于吏治，乐于提拔有才识之人，衣食寒士，不与权奸同流合污，受时人推重。据说他作《金瓶梅》是想为父报仇，王世贞的父亲因献《清明上河图》的赝品，被人识破，因而得罪权臣严嵩和严世藩父子，最后被残害致死。王世贞为报父仇，特作小说《金瓶梅》献给严世藩投其所好。书的内容隐射严嵩父子，揭露他们的种种丑行，而书上又涂有毒药，当严世藩读完此书后就中毒而死了。但是著名学者吴晗率先对这个观点提出质疑，他查阅了大量的正史、野史、笔记，以翔实的史料作为依据，推翻了前人据以立论的主要依据——《清明上河图》与王世贞家族的关系，得出历史上的王世贞之父并不是因为献假图被害，严世藩也不是因为中毒而身亡的结论，否定了《金瓶梅》为王世贞所作的传统看法。吴晗还从书中大量运用的“山东方言”这一点来看，认为王世贞虽然在山东做过三年官，但是要像本地人一样用方言写出这样的巨著是不可能的。他还明确指出，《金瓶梅》应为万历十年至三十年的作品，作者绝不可能是王世贞。有不少研究者也撰文支持吴晗的观点。此是清初人依据《金瓶梅词话》第六十三回所绘的图画。画面中央艺人正在表现海盐腔，右下方的伴奏乐队有提琴、三弦、笙、笛、云锣等乐器，两旁是饮酒看戏的宾客，左上方是掀帘看戏的女眷。20世纪80年代，国内开始有语言学家发表文章对作者的山东籍贯表示怀疑，理由是作品中有不少用语是当今山东方言所没有的，反而在吴方言区经常用到，于是大胆设想作者有可能是吴方言区人。30年代时，英国汉学家阿瑟·韦利就曾提出《金瓶梅》作者是徐渭这一说法，在60多年后的今天却被绍兴文理学院讲师潘承玉新近出版的《金瓶梅新证》给证实了。潘承玉的《金瓶梅新证》首先从时代背景推断《金瓶梅》成书时代为明嘉靖末延续至万历十七年稍后，而这正与徐渭的生活时代相吻合。从地理原型、风俗、方言等诸角度多层面来看，小说与绍兴文化也有很深刻的联系，根据《金瓶梅》是一部“借宋喻明”、“借蔡讽严（嵩）”之作的定论，指出当时正是绍兴形成了全国第一个反严潮流，披露了徐渭与陶望龄以及沈炼为代表的一大批“反严乡贤”鲜为人知的史实，从沈炼正是被严嵩迫害致死，断言徐渭是因感于乡风，感于沈炼的冤死愤慨而作《金瓶梅》。另外，徐渭在晚年曾暗示过他花40年心血而完成了一部长篇小说。而《金瓶梅》的措词用语、文风都与徐渭十分吻合。另外，从作者写作《金瓶梅》的特殊心态，也跟徐渭的遭际一脉相承。中国古典文学名著《金瓶梅》问世四百多年来，作者究竟是谁？创作背景怎样？笑笑生究竟是何人，还是一个未解的谜，这一连串疑问仍像重重迷雾笼罩，等待后人的解答。返回搜狐，查看更多责任编辑："
    texts = []
    segs = re.split("(。|？|，|\,|\.)", mmtext)
    buffer = ""
    for line in segs:
        if len(buffer) > 200:
            texts.append(buffer)
            buffer = line
        else:
            buffer = buffer + line
    if len(buffer) > 3:
        texts.append(buffer)

    for item in texts:
        print("=============")
        print(item)


    # 获取嵌入
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )

    # 打印响应
    # print(response)

    # 提取嵌入向量
    mlist = response.data
    embeddings = []
    for item in mlist:
        embeddings = embeddings + [item.embedding]
        # print(item.embedding)

    # 查询文本
    query_text = question
    query_response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=[query_text]
    )

    query_embedding = query_response.data[0].embedding

    # 计算余弦相似度并找到最相似的文本
    most_similar_index, similarity_score = find_most_similar_text(embeddings, query_embedding)

    if similarity_score < 0.6:
        print("[没找到匹配内容]")
        return("[没找到匹配内容]")
    else:
        print(f"Most similar text: {texts[most_similar_index]}")
        print(f"Similarity score: {similarity_score}")
        return(texts[most_similar_index])

## 用法说明.
def main():
    mmtext = "王樨，字桂庵，是大名府的一个富家子弟。有一次，他去南方游历，船停在江边。他看到邻船上有个姑娘在绣鞋子，长得非常漂亮。王桂庵偷偷看了她很久，然后故意大声吟诗，让姑娘听见。姑娘似乎明白他的意思，抬头看了他一眼，又继续绣鞋子。王桂庵心动不已，扔了一锭银子过去，银子掉在姑娘的衣襟上。姑娘捡起银子扔到岸边。王桂庵捡回银子，又扔了一枚金钏过去，金钏掉在姑娘脚下，但她不理会。过了一会儿，船家的父亲回来，王桂庵很担心，姑娘用脚把金钏盖住。船开走后，王桂庵很沮丧，后悔没有马上托媒人定下婚事。他打听姑娘的身份，但没人知道。他回到自己的船上，追赶姑娘的船，但找不到。事情办完后，他回北方，沿江寻找姑娘，还是没有消息。"
    question = "金瓶梅的作者是谁"
    findsimillar(mmtext,question)

# main()