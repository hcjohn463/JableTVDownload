from tqdm import tqdm
import time
import os
def mergeMp4(folderPath,tsList):

	#開始時間
	start_time = time.time()
	print('開始合成影片..')

	for i in range(len(tsList)):
		file = tsList[i].split('/')[-1][0:-3] + '.mp4'
		if os.path.exists(folderPath + '/' + file):
			with open(folderPath + '/' + file, 'rb') as f1:
				with open(folderPath + '/' + folderPath.split('/')[-1] + ".mp4", 'ab') as f2:
					f2.write(f1.read())
		else:
			print(file + " 失敗 ")

	end_time = time.time()
	print(f"花費 {end_time - start_time} 秒合成影片")