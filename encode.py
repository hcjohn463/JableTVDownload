import os
import time
def encodeMp4(folderPath):
    #開始時間
    start_time = time.time()
    print('開始合成影片..')

    number = folderPath.split('/')[-1]
    before = number + '/o' + number + '.mp4'
    after = number + '/' + number + '.mp4'
    command = 'ffmpeg -i ' + before + ' -c:v libx264 -b:v 2M -threads 5 -preset superfast ' + after
    os.system(command)

    end_time = time.time()
    print('花費 {0:.2f} 秒合成影片'.format(end_time - start_time))
    print('下載完成!')
