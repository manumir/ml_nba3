from bs4 import BeautifulSoup as bs4
from functions import name2acro2
import requests
import re
import sys

# usage
# python3 scraper3.py 10-11 
# scrapes 10-11 season

season=sys.argv[1]
if int(season[-2:]) > 0:
	last_year_of_season='20'+season[-2:]
else:
	last_year_of_season='19'+season[-2:]

with open('./data/data'+season+'.txt','w') as file:
	file.write('date,team,player,MP,FG,FGA,FG%,3P,3PA,3P%,FT,FTA,FT%,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,PTS,+/-\n')

	x = requests.get('https://www.basketball-reference.com/leagues/NBA_'+last_year_of_season+'_games.html')
	soup=bs4(x.text,'html.parser')
	months=soup.body.find('div',class_="filter").find_all('a')
	for month in months:
		month_link=month.get('href')

		x = requests.get('https://www.basketball-reference.com/'+month_link)

		soup=bs4(x.text,'html.parser')
		links=soup.find_all('a',attrs={'href' : re.compile ('/boxscores/[0-9]')})
		for link in links:
			link=link.get('href')
			
			# get game data
			x = requests.get('https://www.basketball-reference.com'+link)
			print(link)

			soup=bs4(x.text,'html.parser')

			# get date
			date=soup.body.find('div',id='content').h1.text
			date=date[date.find(',')+2:].replace(',','')

			ids=[]
			tables=soup.body.find_all('div',class_='overthrow table_container')
			for table_id in tables:
				if re.search('-game-basic',table_id.get('id')):
					ids.append(table_id.get('id'))

			for id in ids:
				match=re.search(3*'[A-Z]',id)
				if match:
					team=id[match.start():match.end()]

				# get whole game table
				table=soup.body.find('div',attrs={"id":id,"class":"overthrow table_container"})
				table=table.table

				stats=[]
				lines=table.find_all('tr')
				for line in lines:
					name=line.find('th').text
					stats_line=line.find_all('td')
					if len(stats_line) > 0:
						line=''
						for stat in stats_line:
							line=line+','+stat.text
						if name != 'Team Totals':
							line=date+','+team+','+name+line+'\n'
						elif name == 'Team Totals':
							line=date+','+team+','+name+line[:-1]+'\n'
						if name != 'Starters' or name != 'Reserves':
							stats.append(line)

				for line in stats:
					file.write(line)


