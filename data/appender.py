#! /usr/bin/python3

import glob

mode=input('last 2 seasons ? y or n')
if mode == 'n':
	files=glob.glob('data*.txt')
elif mode == 'y':
	files=['data19-20.txt','data20-21.txt']

all_lines=[]
for file in files:
	print(file)
	with open(file,'r') as f:
		lines=f.readlines()
		all_lines=all_lines+lines[1:]

if mode == 'n':
	with open('all_data.txt','w') as f:
		f.write(lines[0])
		for line in all_lines:
			f.write(line)
elif mode == 'y':
	with open('season_start.txt','w') as f:
		f.write(lines[0])
		for line in all_lines:
			f.write(line)
