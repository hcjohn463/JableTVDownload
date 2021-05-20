import ffmpeg
import time
def encodeMp4(folderPath):
    #開始時間
    start_time = time.time()
    print('開始合成影片..')

    originFile = folderPath + '/o' + folderPath.split('/')[-1] + '.mp4'
    needFile = folderPath + '/' + folderPath.split('/')[-1] + '.mp4'
    
    output_args = {
        "c:v" : "libx264",
        "b:v" : "2M",
        "threads" : 5,
        "preset": "superfast",
    }

    (
        ffmpeg
        .input(originFile)
        .output(needFile, **output_args)
        .run()
    )

    end_time = time.time()
    print('花費 {0:.2f} 秒合成影片'.format(end_time - start_time))
    print('下載完成!')
