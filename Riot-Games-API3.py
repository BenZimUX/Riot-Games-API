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

who_are_you = str(input("Please enter your summoner name:"))
summoner = w.get_summoner(name = who_are_you)
print (summoner)
summoner_id = summoner['id']
champion_list = w.static_get_champion_list()

class Cleaned_Champion_Data():
	def __init__(self, champion_list = {}):
		self.champion_list = champion_list

	def champion_ids_list(): #list of champion ids
		lst = []
		for each_champ in champion_list['data']:
			lst.append(champion_list['data'][each_champ]['id'])
		return lst #each element in the list is an integer
	# champion_ids_list = champion_ids_list()
			
	#don't use this one in the Class
	def champion_dict(): #dictionary of Champion Names (keys) and Champion ids (values)
		dct = {}
		for each_champ in champion_list['data']:
			dct[champion_list['data'][each_champ]['name']] = champion_list['data'][each_champ]['id']
		return dct
	# champion_dict = champion_dict()***********
	
# Do I have to initialize the class here and call the functions in order to pass them into my class Riot_Data?
class Riot_Data(Static_Data):
	def __init__(self, my_ranked_stats = {}, stat_summary = {}):
		Static_Data.__init__(self, champion_list = {})
		self.my_ranked_stats = my_ranked_stats
		self.stat_summary = stat_summary

	
	def most_played_champions(self, champ_dict*****): #returns a sorted list of tuples that sorts it based on games played 
		dct = {}
		for each_champ in self.my_ranked_stats['champions']:
			for key in champ_dict:
				if(each_champ['id']==champ_dict[key]):
					dct[key] = each_champ['stats']['totalSessionsPlayed'] 
		return sorted(dct.items(), key = lambda x : (-x[1], x[0]))

	
	def ranked_win_percentage(self, champ_dict*****):
		dct = {}
		for each_champ in self.my_ranked_stats['champions']:
			for key in champ_dict:
				if(each_champ['id']==champ_dict[key]):
					dct[key] = each_champ['stats']['totalSessionsWon']/each_champ['stats']['totalSessionsPlayed']
		return sorted(dct.items(), key = lambda x : (-x[1], x[0]))


	def overall_ranked_win_percentage(self):
		x = 0
		for y in self.stat_summary['playerStatSummaries']:
			for key in y:
				if(y['playerStatSummaryType']=="RankedSolo5x5"):
					x = y['wins']/(y['losses']+y['wins'])
		return x


	def last_played_ranked_game(self):
		x = 0
		for y in self.stat_summary['playerStatSummaries']:
			for key in y:
				if(y['playerStatSummaryType']=="RankedSolo5x5"):
					x = y['modifyDate']
		#return x/1000
		date_ranked = time.strftime('%Y-%m-%d', time.localtime(x/1000))
		return date_ranked


	def last_played_flex_game(self):
		x = 0
		for y in self.stat_summary['playerStatSummaries']:
			for key in y:
				if(y['playerStatSummaryType']=="RankedFlexSR"):
					x = y['modifyDate']
		#return x/1000
		date_flex = time.strftime('%Y-%m-%d', time.localtime(x/1000))
		return date_flex


	def last_time_logged_in(self):
		summoner_date = summoner['revisionDate']
		date_general = time.strftime('%Y-%m-%d', time.localtime(summoner_date/1000))
		return date_general


data = Riot_Data(w.get_ranked_stats(summoner_id), w.get_stat_summary(summoner_id))
print(data.most_played_champions(champion_dict****))
print(data.ranked_win_percentage(champion_dict****))
print(data.overall_ranked_win_percentage())
print(data.last_played_ranked_game())
print(data.last_played_flex_game())
print(data.last_time_logged_in())

#having trouble with champion_dict and inheriting from the class (I can't seem to make it work)

#  Making bar charts: http://matplotlib.org/examples/api/barchart_demo.html
