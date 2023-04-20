import os
import subprocess
def ffmpeg_encode(folder_path, file_name):
    action = input('要轉檔嗎?(y/n)')
    if(action.lower() == "y"):
        os.chdir(folder_path)
        try:
            action = input('要使用Nvidia硬體加速嗎?(y/n)')
            if(action.lower() == "y"):
                subprocess.call(['ffmpeg', '-i', f'{file_name}.mp4','-c:v', 'h264_nvenc', '-b:v', '10000K',
                                '-threads', '5', f'f_{file_name}.mp4'])
            else:
                subprocess.call(['ffmpeg', '-i', f'{file_name}.mp4', '-c:v', 'libx264', '-b:v', '3M',
                            '-threads', '5', '-preset', 'superfast', f'f_{file_name}.mp4'])
            os.remove(os.path.join(folder_path, f'{file_name}.mp4'))
            os.rename(os.path.join(folder_path, f'f_{file_name}.mp4'), os.path.join(folder_path, f'{file_name}.mp4'))
            print("轉檔成功!")

        except:
            print("轉檔失敗!")
    else:
        return
