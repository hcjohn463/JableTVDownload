import os
import time
from tqdm import tqdm


def mergeMp4(folderPath, tsList):
    """產生 FFmpeg concat 用的清單檔案，不再進行二進位串接以節省時間與 IO"""
    start_time = time.time()
    # video_name = folderPath.split(os.path.sep)[-1]
    concat_list_path = os.path.join(folderPath, 'concat_list.txt')

    print('正在準備合成清單..')
    total = len(tsList)
    with open(concat_list_path, 'w', encoding='utf-8') as f:
        for i in range(total):
            file = tsList[i].split('/')[-1][0:-3] + '.mp4'
            full_path = os.path.join(folderPath, file)
            if os.path.exists(full_path):
                # FFmpeg concat file 格式: file 'path/to/file'
                # 使用相對路徑或絕對路徑皆可，這裡用檔名即可，因為會在 folderPath 執行 ffmpeg
                f.write(f"file '{file}'\n")
            else:
                print(f'警告: 缺少片段 {file}')

    elapsed = time.time() - start_time
    print('花費 {0:.2f} 秒 準備合成清單'.format(elapsed))

