# My API Key: RGAPI-76f4bcb6-da64-455a-aad2-07eee7ad0e8f
# Rate Limits:
# 500 requests every 10 minutes
# 10 requests every 10 seconds
# Regional Endpoint Platform ID for North America: NA1

# more info: https://github.com/pseudonym117/Riot-Watcher
from riotwatcher import RiotWatcher
import time
import numpy as np
import matplotlib.pyplot as plt

w = RiotWatcher("RGAPI-76f4bcb6-da64-455a-aad2-07eee7ad0e8f")

#check to see if we have API Calls Remaining 
#print (w.can_make_request()) 

who_are_you = str(input("Please enter your summoner name:"))
summoner = w.get_summoner(name = who_are_you)
print (summoner)
summoner_id = summoner['id']

my_ranked_stats = w.get_ranked_stats(summoner_id)
#print(my_ranked_stats)

champion_list = w.static_get_champion_list()
#print (champion_list)

stat_summary = w.get_stat_summary(summoner_id)
#print (stat_summary)

def champion_ids_list(): #list of champion ids
	lst = []
	for each_champ in champion_list['data']:
		lst.append(champion_list['data'][each_champ]['id'])
	return lst #each element in the list is an integer
champion_ids_list = champion_ids_list()
	
#don't use this one in the Class
def champion_dict(): #dictionary of Champion Names (keys) and Champion ids (values)
	dct = {}
	for each_champ in champion_list['data']:
		dct[champion_list['data'][each_champ]['name']] = champion_list['data'][each_champ]['id']
	return dct
champion_dict = champion_dict()
#print (champion_dict)


def most_played_champions(champ_dict): #returns a sorted list of tuples that sorts it based on games played 
	dct = {}
	for each_champ in my_ranked_stats['champions']:
		for key in champ_dict:
			if(each_champ['id']==champ_dict[key]):
				dct[key] = each_champ['stats']['totalSessionsPlayed'] 
	return sorted(dct.items(), key = lambda x : (-x[1], x[0]))
most_played_champions = most_played_champions(champion_dict)
#print (most_played_champions)

def ranked_win_percentage(champ_dict):
	dct = {}
	for each_champ in my_ranked_stats['champions']:
		for key in champ_dict:
			if(each_champ['id']==champ_dict[key]):
				dct[key] = each_champ['stats']['totalSessionsWon']/each_champ['stats']['totalSessionsPlayed']
	return sorted(dct.items(), key = lambda x : (-x[1], x[0]))

win_pct = ranked_win_percentage(champion_dict)
#print (win_pct)

def overall_ranked_win_percentage():
	x = 0
	for y in stat_summary['playerStatSummaries']:
		for key in y:
			if(y['playerStatSummaryType']=="RankedSolo5x5"):
				x = y['wins']/(y['losses']+y['wins'])
	return x

overall_ranked_win_percentage = overall_ranked_win_percentage()
#print (overall_ranked_win_percentage)

def last_played_ranked_game():
	x = 0
	for y in stat_summary['playerStatSummaries']:
		for key in y:
			if(y['playerStatSummaryType']=="RankedSolo5x5"):
				x = y['modifyDate']
	#return x/1000
	date_ranked = time.strftime('%Y-%m-%d', time.localtime(x/1000))
	return date_ranked
last_played_ranked_game = last_played_ranked_game()
#print (last_played_ranked_game)

def last_played_flex_game():
	x = 0
	for y in stat_summary['playerStatSummaries']:
		for key in y:
			if(y['playerStatSummaryType']=="RankedFlexSR"):
				x = y['modifyDate']
	#return x/1000
	date_flex = time.strftime('%Y-%m-%d', time.localtime(x/1000))
	return date_flex
last_played_flex_game = last_played_flex_game()
print (last_played_flex_game)

def last_time_logged_in():
	summoner_date = summoner['revisionDate']
	date_general = time.strftime('%Y-%m-%d', time.localtime(summoner_date/1000))
	return date_general

last_time_logged_in = last_time_logged_in()
print (last_time_logged_in)

#how to convert epoch milliseconds to readable date
#x = 1479701601000/1000
#print (time.strftime('%Y-%m-%d', time.localtime(x))) #prints out the date for epoch milliseconds adding "%H:%M:%S" gives hours minutes seconds

# x = ()
# for each_item in <list of tuples>:
#	x = each_item[1]

#IDEAS
# When's the first time that you played? vs When's the last time you played?

#  Who do you play with frequently?
# 	Maybe get some information about someone they play with frequently

#  How do your champion stats compare with global champion stats

#  Making bar charts: http://matplotlib.org/examples/api/barchart_demo.html
