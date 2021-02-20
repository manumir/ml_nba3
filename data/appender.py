#! /usr/bin/python3

import glob

mode=input('last 2 seasons ? y or n')
if mode == 'n':
	files=glob.glob('./seasons/data*.txt.gz')
	files=sorted(files)
elif mode == 'y':
	files=['./seasons/data19-20.txt','./seasons/data20-21.txt']

all_lines=[]
for file in files:
	print(file)
	with open(file,'r') as f:
		lines=f.readlines()
		all_lines=all_lines+lines[1:]

if mode == 'n':
	with open(input('name of file to output to '),'w') as f:
		f.write(lines[0])
		for line in all_lines:
			f.write(line)
elif mode == 'y':
	with open('season_start.csv','w') as f:
		f.write(lines[0])
		for line in all_lines:
			f.write(line)
