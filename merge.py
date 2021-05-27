import os


def mergeMp4(folderPath, tsList):
    for i in range(len(tsList)):
        file = tsList[i].split('/')[-1][0:-3] + '.mp4'
        full_path = os.path.join(folderPath, file)
        video_name = folderPath.split(os.path.sep)[-1]
        if os.path.exists(full_path):
            with open(full_path, 'rb') as f1:
                with open(os.path.join(folderPath, 'o' + video_name + '.mp4'), 'ab') as f2:
                    f2.write(f1.read())
        else:
            print(file + " 失敗 ")
