import os
import subprocess


def ffmpeg_encode(folder_path, file_name):
    os.chdir(folder_path)
    try:
        subprocess.call(['ffmpeg', '-i', f'{file_name}.mp4', '-c:v', 'libx264', '-b:v', '3M',
                        '-threads', '5', '-preset', 'superfast', f'f_{file_name}.mp4'])
        os.remove(os.path.join(folder_path, f'{file_name}.mp4'))
        print(f"Encoded {file_name}")
    except:
        print(f"Fail to encode {file_name}")
