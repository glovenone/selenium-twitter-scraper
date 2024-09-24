# movie库中的badnews数据库里
import pymysql
import requests
import random
import json
import os

# 连接 MySQL 数据库
connection = pymysql.connect(
    host='localhost',  # 替换为你的数据库主机
    user='root',  # 替换为你的数据库用户名
    password='',  # 替换为你的数据库密码
    database='ishare',  # 替换为你的数据库名
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)


# 随机生成数字的函数
def random_count():
    return random.randint(1, 10000)


# 获取前 100 条数据
def fetch_data():
    with connection.cursor() as cursor:
        sql = "select * from feed ORDER BY rand() LIMIT 100"
        cursor.execute(sql)
        result = cursor.fetchall()
    return result


# 检查文本是否为英文
def is_english(text):
    return all(ord(c) < 128 for c in text)


# 从文件中加载缓存
def load_translation_cache(file_path="translation_cache.json"):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}


# 将缓存保存到文件
def save_translation_cache(cache, file_path="translation_cache.json"):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(cache, file, ensure_ascii=False, indent=2)


# 将单个翻译结果立即追加到缓存文件中
def append_to_translation_cache(text, translation, file_path="translation_cache.json"):
    cache = load_translation_cache(file_path)
    cache[text] = translation
    save_translation_cache(cache, file_path)


# 翻译为英文，使用文件缓存
def translate_to_english(text, cache, file_path="translation_cache.json"):
    if text in cache:
        return cache[text]

    if is_english(text):
        cache[text] = text  # 如果是英文，直接缓存并返回
        append_to_translation_cache(text, text, file_path)  # 立即保存
        return text

    # 调用翻译 API
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&dt=t&sl=zh-CN&tl=en&q={text}"
        response = requests.get(url)
        translated_text = response.json()[0][0][0]
        cache[text] = translated_text  # 缓存翻译结果
        append_to_translation_cache(text, translated_text, file_path)  # 立即保存
        return translated_text
    except (KeyError, IndexError, requests.RequestException) as e:
        print(f"Error translating '{text}': {e}")  # 打印异常信息
        cache[text] = text  # 如果翻译失败，缓存原文
        append_to_translation_cache(text, text, file_path)  # 立即保存原文
        return text


# 转换数据
def transform_data(data, cache, file_path="translation_cache.json"):
    config_page = []
    for row in data:
        # 翻译用户名和内容
        translated_username = translate_to_english(row['username'], cache, file_path)
        translated_content = translate_to_english(row['content'], cache, file_path)

        if translated_content == "":
            translated_content = random.choice(tweet_templates)

        # 如果 avatar 是默认值之一，则使用一个备用的图片
        avatar = row['avatar'] if row['avatar'] not in (
            "/images/lightbox-blank.gif", "/images/default_avatar_400x400.jpeg") else "https://img.lvv2.com/images/topic/profile_images/649924909fb414318a9f1cabe0bf6968.jpg"

        entry = {
            "name": translated_username.strip("@"),  # 使用翻译后的用户名
            "username": translated_username.strip("@"),
            "avatar": avatar,
            "content": translated_content,  # 使用翻译后的内容
            "view_count": row['view_count'],
            "download_count": row['download_count'],
            "share_count": row['share_count'],
            "emojiList": [
                {"id": 1, "emoji": "👍🏻", "count": row['emoji_01']},
                {"id": 2, "emoji": "💩", "count": row['emoji_02']},
                {"id": 3, "emoji": "❤️️", "count": row['emoji_03']},
                {"id": 4, "emoji": "🥳", "count": row['emoji_04']},
                {"id": 5, "emoji": "🐖", "count": row['emoji_05']},
                {"id": 6, "emoji": "🍾", "count": row['emoji_06']},
                {"id": 7, "emoji": "👏🏻", "count": row['emoji_07']},
                {"id": 8, "emoji": "👻", "count": row['emoji_08']},
            ],
            "videoList": [
                {
                    "definition": row['video_definition'],
                    "needPro": bool(row['video_needPro']),
                    "duration": row['video_duration'],  # 视频时长
                    "poster": row['video_poster'],
                    "src": row['video_src'],
                }
            ],
        }
        config_page.append(entry)
    return config_page


# sex相关的推文模板
tweet_templates = [
    "Sex education is important for young people to understand their bodies.",
    "The conversation about sex should be open and respectful.",
    "Sexual health is a crucial part of overall well-being.",
    "I think sex should be discussed more openly, it's a natural part of life.",
    "There are so many misconceptions about sex that need to be addressed.",
    "How can we improve sex education in schools?",
    "What are your thoughts on the importance of consent in sex?",
    "Sexuality is a personal journey and everyone experiences it differently.",
    "Talking about safe sex practices is important for everyone.",
    "There are many different opinions about sex in modern society.",
    "Sex shouldn't be a taboo topic. Let's normalize talking about it.",
    "How can we reduce the stigma around sex in public discussions?",
    "Sex and relationships are complicated but worth the effort to understand.",
    "How do you think media influences our perceptions of sex?",
    "People often have unrealistic expectations about sex from movies and TV.",
    "Sexual health checkups should be a regular part of healthcare.",
    "What role does communication play in a healthy sex life?",
    "There are so many myths about sex that need to be debunked.",
    "Sex is a normal part of human life, but it should always be consensual.",
    "It's important to educate people about the emotional aspects of sex.",
    "What are the biggest misconceptions about sex that you've encountered?",
    "Sex can be a beautiful part of life, but it needs to be approached with care.",
    "Why is there still so much stigma around talking about sex?",
    "Sexual health services should be accessible to everyone.",
    "How can we promote a healthier understanding of sex in society?",
    "Sex is often portrayed in extreme ways in media – either overly glorified or demonized.",
    "What age should kids start learning about sex in schools?",
    "Conversations about sex need to be more inclusive of different identities and orientations.",
    "It's important to have healthy boundaries when it comes to sex.",
    "Respect and consent are the foundations of any conversation about sex.",
    "Sex is part of life, but it's important to have mutual respect in every relationship.",
    "Let's talk about the importance of mutual consent when it comes to sex.",
    "There should be more resources available for people to learn about safe sex.",
    "The internet is full of misinformation about sex. How can we change that?",
    "There are still cultures where talking about sex is forbidden. How do we change that?",
    "Sexual empowerment is about understanding your own body and your boundaries.",
    "Why are people still so afraid to talk about sex openly?",
    "Sexual consent isn't just important – it's mandatory in every situation.",
    "How can we create a more respectful conversation around sex in the media?",
    "Sex is often misunderstood – how can we educate people better?",
    "There are so many different aspects of sex that people don't understand.",
    "How can we make sex education more accessible and inclusive?",
    "Respectful conversations about sex can help reduce misunderstandings and stigma.",
    "Sexual pleasure is an important part of relationships, but so is communication.",
    "The way we talk about sex has a huge impact on our understanding of relationships.",
    "Sex is natural, but it comes with responsibilities.",
    "We need to teach young people the emotional aspects of sex, not just the physical.",
    "Sex education should be a right, not a privilege.",
    "When we avoid talking about sex, we leave people in the dark about important information.",
    "The portrayal of sex in the media often skews our understanding of reality.",
    "Consent is the most important part of any sexual interaction.",
    "Sex education should cover all orientations and identities.",
    "How can we promote a healthier, more open conversation about sex?",
    "Sexual health is about more than just preventing diseases, it's about overall well-being.",
    "We need to destigmatize conversations about sex in all parts of society.",
    "Sexuality is a spectrum, and everyone experiences it differently.",
    "The way we talk about sex affects how we feel about it in our relationships.",
    "There are so many false expectations about sex created by media.",
    "Sexual health and education should be normalized, not shamed.",
    "It's important to talk openly about sex in a safe and respectful way.",
    "How do you think the internet has changed the way we talk about sex?",
    "Sexual boundaries should always be respected and understood by both parties.",
    "How can we create a more positive environment for conversations about sex?",
    "Sexual health clinics should be more accessible to all communities.",
    "The more we understand sex, the healthier our relationships can be.",
    "How can we make sure that people of all ages have access to reliable sex education?",
    "Sex is often sensationalized in media, but it's just one part of a relationship.",
    "Open discussions about sex can lead to more fulfilling and respectful relationships.",
    "We need to move beyond outdated views about sex in modern society.",
    "How do we make sure everyone has access to sexual health resources?",
    "Why is it so hard for some people to talk about sex openly?",
    "Sexual consent is an ongoing conversation, not a one-time agreement.",
    "How can we make sure people are informed about safe sex practices?",
    "What are the best ways to promote healthy attitudes towards sex?",
    "Why are there still so many taboos around sex?",
    "We should be able to talk about sex without fear of judgment.",
    "Sexuality is diverse, and it's important to respect everyone's experiences.",
    "What role does culture play in shaping our views on sex?",
    "We need more comprehensive sex education that covers all aspects of relationships.",
    "The way we learn about sex can have a lasting impact on our relationships.",
    "Sexual health should be a regular part of healthcare, not an afterthought.",
    "Everyone deserves access to accurate, non-judgmental information about sex.",
    "Sex can be fun, but it should always be consensual and respectful.",
    "Sex education should include conversations about emotional readiness, not just physical.",
    "Sexuality is a normal part of human life, but it comes with responsibilities.",
    "Why is sex such a difficult topic for people to discuss?",
    "We need more open, honest conversations about sex in society.",
    "Sexual consent should be a priority in every discussion about relationships.",
    "How can we create more inclusive spaces for conversations about sex?",
    "We need to teach young people about healthy sexual boundaries.",
    "Why is sex education still such a controversial topic in some places?",
    "Talking about sex is normal, and it should be treated as such.",
    "We need more support for people exploring their sexuality in a healthy way.",
    "The conversation around sex should include all orientations and experiences."
]


# 主函数
def main():
    # 加载翻译缓存
    translation_cache = load_translation_cache()

    # 获取数据并转换
    data = fetch_data()
    transformed_data = transform_data(data, translation_cache)

    # 将数据转换为 JSON 格式并输出
    json_data = json.dumps(transformed_data, indent=2, ensure_ascii=False)
    print(json_data)


if __name__ == "__main__":
    main()
