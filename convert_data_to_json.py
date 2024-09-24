#movie库中的badnews数据库里
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
    database='movie',  # 替换为你的数据库名
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)


# 随机生成数字的函数
def random_count():
    return random.randint(1, 10000)


# 获取前 100 条数据
def fetch_data():
    with connection.cursor() as cursor:
        sql = "SELECT tid, thumbnail, user_name, title, content_url, tag, video_poster, video_source_url FROM badnews WHERE video_poster != '' AND user_name != '李老师不是你老师' ORDER BY rand() LIMIT 100"
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
        translated_username = translate_to_english(row['user_name'], cache, file_path)
        translated_content = translate_to_english(row['title'], cache, file_path)
        if row['thumbnail'] not in ("/images/lightbox-blank.gif", "/images/default_avatar_400x400.jpeg"):
            thumbnail = row['thumbnail']
        else:
            thumbnail = "https://img.lvv2.com/images/topic/profile_images/649924909fb414318a9f1cabe0bf6968.jpg"
        entry = {
            "name": translated_username,
            "username": translated_username,
            "avatar": thumbnail,
            "content": translated_content,
            "view_count": str(random_count()),
            "download_count": str(random_count()),
            "share_count": str(random_count()),
            "emojiList": [
                {"id": 1, "emoji": "👍🏻", "count": random_count()},
                {"id": 2, "emoji": "💩", "count": random_count()},
                {"id": 3, "emoji": "❤️️", "count": random_count()},
                {"id": 4, "emoji": "🥳", "count": random_count()},
                {"id": 5, "emoji": "🐖", "count": random_count()},
                {"id": 6, "emoji": "🍾", "count": random_count()},
                {"id": 7, "emoji": "👏🏻", "count": random_count()},
                {"id": 8, "emoji": "👻", "count": random_count()},
            ],
            "videoList": [
                {
                    "definition": random.choice(["4K", "1080", "720"]),
                    "needPro": random.choice([True, False]),
                    "duration": random.randint(600, 10000),  # 生成秒数
                    "poster": row['video_poster'],
                    "src": row['video_source_url'],
                }
            ],
        }
        config_page.append(entry)
    return config_page


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
