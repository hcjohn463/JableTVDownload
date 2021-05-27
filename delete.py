import os


def deleteMp4(folderPath, flag):
    files = os.listdir(folderPath)
    originFile = 'o' + folderPath.split(os.path.sep)[-1] + '.mp4'
    if flag:
        for file in files:
            if file != originFile:
                os.remove(os.path.join(folderPath, file))
    else:
        os.remove(os.path.join(folderPath, originFile))


def deleteM3u8(folderPath):
    files = os.listdir(folderPath)
    for file in files:
        if file.endswith('.m3u8'):
            os.remove(os.path.join(folderPath, file))
