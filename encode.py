import os
def encodeMp4(folderPath):
	number = folderPath.split('/')[-1]
	before = number + '/o' + number + '.mp4'
	after = number + '/' + number + '.mp4'
	command = 'ffmpeg -i ' + before + ' -c:v libx264 -b:v 2M -threads 5 -preset superfast ' + after
	os.system(command)
