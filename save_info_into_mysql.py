import pandas as pd
import mysql.connector
import random
import os

# 配置 MySQL 数据库连接
db_config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'ishare'
}


# 连接到 MySQL 数据库
def connect_to_db():
    return mysql.connector.connect(**db_config)


# 读取并处理 CSV 文件
def process_csv_files(folder_path):
    # 获取文件夹中的所有 CSV 文件
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    # 连接到数据库
    conn = connect_to_db()
    cursor = conn.cursor()

    # SQL 插入语句
    insert_query = """
    INSERT INTO feed (
        name, username, avatar, content, view_count, download_count, 
        share_count, emoji_01, emoji_02, emoji_03, emoji_04, 
        emoji_05, emoji_06, emoji_07, emoji_08, video_duration, 
        video_definition, video_needPro, video_poster, video_src,url
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
    """

    for file_name in csv_files:
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_csv(file_path)

        for index, row in df.iterrows():
            # print("index,row:", index, row)
            # 从 CSV 中获取数据

            try:
                name = row[0].strip()
                username = row[1].strip()
                avatar = row[12]
                content = str(row[4]).strip()
            except Exception as e:
                print("get row error:", e)
                continue
            # print("content:", len(content), type(content), content)

            if (content is None) or (content == 'nan'):
                content = ""
            video_poster = row[16]
            if video_poster == 'Error':
                continue
            video_src = row[15]
            url = row[13]

            # 随机生成数据
            view_count = random.randint(1, 100)
            download_count = random.randint(1, 100)
            share_count = random.randint(1, 100)

            emoji_counts = [random.randint(1, 2000) for _ in range(8)]

            video_duration = random.randint(150, 8000)
            video_definition = random.choice(["1080", "720", "4K"])
            video_needPro = True

            # print("insert_query:", insert_query)
            # 插入数据到数据库
            try:
                cursor.execute(insert_query, (
                    name, username, avatar, content, view_count, download_count,
                    share_count, *emoji_counts, video_duration, video_definition,
                    video_needPro, video_poster, video_src, url
                ))
            except Exception as e:
                print(f"Insert error: {e}")

    conn.commit()
    cursor.close()
    conn.close()

    print("Data inserted successfully for all files")


# 执行函数
process_csv_files('csv_files_done')

# CREATE TABLE feed (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(255) NOT NULL,
#     username VARCHAR(255) NOT NULL,
#     avatar VARCHAR(255),
#     content TEXT,
#     view_count INT DEFAULT 0,
#     download_count INT DEFAULT 0,
#     share_count INT DEFAULT 0,
#     emoji_01 INT DEFAULT 0,
#     emoji_02 INT DEFAULT 0,
#     emoji_03 INT DEFAULT 0,
#     emoji_04 INT DEFAULT 0,
#     emoji_05 INT DEFAULT 0,
#     emoji_06 INT DEFAULT 0,
#     emoji_07 INT DEFAULT 0,
#     emoji_08 INT DEFAULT 0,
#     video_duration INT DEFAULT 0,
#     video_definition VARCHAR(255),
#     video_needPro BOOLEAN DEFAULT FALSE,
#     video_poster VARCHAR(255),
#     video_src TEXT
# );
