def myacc(preds2,test):
  preds=[]
  for i in range(len(preds2)):
    if preds2[i] < 0.5:
      preds.append(0)
    else:
      preds.append(1)

  test=list(test)
  count=0
  for i in range(len(test)):
    if preds[i]==test[i]:
      count=count+1

  return count/len(test)

def name2acro2(arg):
	if arg in ['Memphis Grizzlies','Memp. Grizzlies']:
		arg1 = 'MEM'
	elif arg in ['Dallas Mavericks','Dall. Mavericks']:
		arg1 = 'DAL'
	elif arg == 'Indiana Pacers':
		arg1 = 'IND'
	elif arg == 'Brooklyn Nets':
		arg1 = 'BKN'
	elif arg == 'Atlanta Hawks':
		arg1 = 'ATL'
	elif arg in ['Portland Trail Blazers','Trail Blazers']:
		arg1 = 'POR'
	elif arg in ['Minnesota Timberwolves','Minnesota Timb.']:
		arg1 = 'MIN'
	elif arg == 'Utah Jazz':
		arg1 = 'UTA'
	elif arg == 'Chicago Bulls':
		arg1 = 'CHI'
	elif arg in ['Sacramento Kings','Sac. Kings']:
		arg1 = 'SAC'
	elif arg == 'Toronto Raptors':
		arg1 = 'TOR'
	elif arg in ['Washington Wizards','Washin. Wizards']:
		arg1 = 'WAS'
	elif arg == 'Orlando Magic':
		arg1 = 'ORL'
	elif arg == 'Denver Nuggets':
		arg1 = 'DEN'
	elif arg in ['Golden State Warriors','GS Warriors']:
		arg1 = 'GSW'
	elif arg == 'Phoenix Suns':
		arg1 = 'PHX'
	elif arg in ['Charlotte Hornets','Charlotte Bobcats','Charl. Hornets']:
		arg1 = 'CHA'
	elif arg == 'New Orleans Hornets':
		arg1 = 'NOH'
	elif arg == 'New Jersey Nets':
		arg1 = 'NJN'
	elif arg == 'Seattle SuperSonics':
		arg1 = 'SEA'
	elif arg in ['Cleveland Cavaliers','Clev. Cavaliers']:
		arg1 = 'CLE'
	elif arg == 'Milwaukee Bucks':
		arg1 = 'MIL'
	elif arg in ['Los Angeles Clippers','LA Clippers']:
		arg1 = 'LAC'
	elif arg == 'Houston Rockets':
		arg1 = 'HOU'
	elif arg in ['New York Knicks','NY Knicks']:
		arg1 = 'NYK'
	elif arg == 'Detroit Pistons':
		arg1 = 'DET'
	elif arg in ['New Orleans Pelicans','NO Pelicans']:
		arg1 = 'NOP'
	elif arg in ['Philadelphia 76ers','Philadel. 76ers']:
		arg1 = 'PHI'
	elif arg == 'Miami Heat':
		arg1 = 'MIA'
	elif arg == 'Boston Celtics':
		arg1 = 'BOS'
	elif arg in ['Oklahoma City Thunder','OKC Thunder']:
		arg1 = 'OKC'
	elif arg in ['San Antonio Spurs','SA Spurs']:
		arg1 = 'SAS'
	elif arg in ['Los Angeles Lakers','LA Lakers']:
		arg1 = 'LAL'
	else:
		print('cannot define '+arg)
		return arg
	return arg1

