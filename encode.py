import os
import subprocess
from tqdm import tqdm


def get_segment_count(folder_path):
    """取得 concat_list.txt 中的片段總數以顯示進度"""
    try:
        with open(os.path.join(folder_path, 'concat_list.txt'), 'r', encoding='utf-8') as f:
            return sum(1 for line in f if line.startswith('file'))
    except Exception:
        return None


def ffmpegEncode(folder_path, file_name, action=1):
    """
    結合合成與快速無損轉檔
    - 使用 concat demuxer 避免兩次讀寫
    - 不重新壓縮畫面，畫質完全不變
    - 修正音訊封包格式（ADTS → ASC）
    - 加上 faststart
    """
    if action == 0:
        return

    os.chdir(folder_path)
    concat_list = 'concat_list.txt'
    dst = f'{file_name}.mp4'

    if not os.path.exists(concat_list):
        print(f'❌ 找不到合成清單 {concat_list}')
        return

    # 取得片段總數（用於進度條）
    total_segments = get_segment_count(folder_path)

    # 這裡我們觀察 FFmpeg 的進度輸出
    # 因為是 concat copy，通常很快，我們追蹤 frame 或者是 time
    # 但因為總幀數難算，我們顯示處理進度
    cmd = ['ffmpeg', '-y',
           '-f', 'concat',
           '-safe', '0',
           '-i', concat_list,
           '-c', 'copy',
           '-bsf:a', 'aac_adtstoasc',
           '-movflags', '+faststart',
           '-progress', 'pipe:1',
           '-nostats',
           '-loglevel', 'info',   # 改為 info 以便抓取 "Opening" 訊息
           dst]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True,
                                bufsize=1, encoding='utf-8')

    desc = '🚀 快速合成與轉檔'
    with tqdm(total=total_segments, unit='片段', desc=desc,
              bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]',
              dynamic_ncols=True, colour='yellow') as pbar:

        processed_segments = 0
        last_frame_count = 0
        for line in process.stdout:
            # 這裡列出幾種可能的格式以增加相容性
            # 1. [concat @ 0x...] Opening 'xxxxx.mp4' for reading
            # 2. Opening 'xxxxx.mp4' for reading
            if 'Opening' in line and 'for reading' in line:
                processed_segments += 1
                if processed_segments <= total_segments:
                    pbar.update(1)
            
            # 作為備案：如果一直沒有 Opening 訊息（某些環境會過濾），
            # 我們可以透過 frame 的變動來讓進度條「動起來」表示沒死掉，
            # 雖然這裡 total 是片段數，所以我們只在描述增加訊息。
            if 'frame=' in line:
                try:
                    parts = line.split('=')
                    if len(parts) > 1:
                        frame_val = parts[1].split()[0]
                        if frame_val.isdigit():
                            pbar.set_postfix_str(f"已處理 {frame_val} 幀")
                except:
                    pass

            if line.startswith('progress=end'):
                if processed_segments < total_segments:
                    pbar.update(total_segments - processed_segments)

    process.wait()

    if process.returncode == 0:
        if os.path.exists(concat_list):
            os.remove(concat_list)
        print('✅ 合成與轉檔成功!')
    else:
        print('❌ 合成與轉檔失敗!')
