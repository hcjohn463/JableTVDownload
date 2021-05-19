import ffmpeg
import time
def encodeMp4(folderPath):
    #開始時間
    start_time = time.time()
    print('開始合成影片..')

    originFile = folderPath + '/o' + folderPath.split('/')[-1] + '.mp4'
    needFile = folderPath + '/' + folderPath.split('/')[-1] + '.mp4'
    input_args = {
        "hwaccel": "nvdec",
        "vcodec": "h264_cuvid",
        "c:v": "h264_cuvid"
    }

    output_args = {
        "vcodec": "hevc_nvenc",
        "c:v": "hevc_nvenc",
        "preset": "fast",
        "crf": 0,
        "b:v": "20M",
        "acodec": "copy"
    }

    (
        ffmpeg
        .input(originFile, **input_args)
        .output(needFile, **output_args)
        .run()
    )

    end_time = time.time()
    print('花費 {0:.2f} 秒合成影片'.format(end_time - start_time))
    print('下載完成!')