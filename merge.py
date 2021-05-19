import time
import os
def mergeMp4(folderPath,tsList):
	for i in range(len(tsList)):
		file = tsList[i].split('/')[-1][0:-3] + '.mp4'
		if os.path.exists(folderPath + '/' + file):
			with open(folderPath + '/' + file, 'rb') as f1:
				with open(folderPath + '/o' + folderPath.split('/')[-1] + '.mp4', 'ab') as f2:
					f2.write(f1.read())
		else:
			print(file + " 失敗 ")
