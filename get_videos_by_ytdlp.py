import os
import pandas as pd
from yt_dlp import YoutubeDL

# 文件夹路径
folder_path = './csv_files/'  # 替换为你存放 CSV 文件的文件夹路径

# yt-dlp 配置，添加 cookies 参数和获取视频下载地址与缩略图
ydl_opts = {
    'quiet': True,  # 不显示日志信息
    'skip_download': True,  # 不下载视频
    'cookiesfrombrowser': ('firefox', '/Users/glove/Library/Application Support/Firefox/Profiles/6xb16db6.default-release/'),
    'geturl': True,  # 获取视频URL
    'getthumbnail': True,  # 获取视频缩略图
}

break_loop1 = False
# 遍历文件夹中的所有 CSV 文件
for filename in os.listdir(folder_path):
    if break_loop1:
        break
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)

        # 读取 CSV 文件
        df = pd.read_csv(file_path)

        # 确保文件有第10列
        if len(df.columns) < 15:
            print(f"{filename} doesn't have enough columns.")
            continue

        # 遍历每一行，获取第14列的视频链接,15是id，16是视频地址，17是图片地址
        for index, row in df.iterrows():
            video_url = row[13]  # 第14列内容 (index 从0开始，所以是13)

            # 检查第16列是否存在且内容是否等于 'Error'
            if len(row) >= 16 and row[15] != 'Error':
                continue  # 如果有内容但不是 'Error'，则跳过当前行

            if pd.notna(video_url):  # 检查视频链接是否为空
                try:
                    with YoutubeDL(ydl_opts) as ydl:
                        # 提取视频信息
                        info_dict = ydl.extract_info(video_url, download=False)

                        # 获取视频下载链接和缩略图 URL
                        video_download_url_list = info_dict.get('requested_formats', 'N/A')
                        video_download_url = ''
                        if video_download_url_list:
                            video_download_url = video_download_url_list[0]['url']
                        thumbnail_url = info_dict.get('thumbnail', 'N/A')
                        print('url:', video_url)
                        print('result:', video_download_url)

                        # 将视频下载地址和缩略图 URL 写入第11列和第12列
                        df.at[index, 'video_download_url'] = video_download_url
                        df.at[index, 'thumbnail_url'] = thumbnail_url
                except Exception as e:
                    print(f"Error processing video {video_url}: {e}")
                    if 'Rate-limit exceeded' in str(e):  # 未生效，e中获取不到对应内容
                        print(f"Rate limit exceeded, break out;")
                        break_loop1 = True
                        continue

                    df.at[index, 'video_download_url'] = 'Error'
                    df.at[index, 'thumbnail_url'] = 'Error'

        # 保存修改后的 CSV 文件
        df.to_csv(file_path, index=False)
        print(f"Updated: {filename}")
