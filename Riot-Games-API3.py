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
#print (summoner)
summoner_id = summoner['id']
champion_list = w.static_get_champion_list()

class Cleaned_Champion_Data():
	def __init__(self, champion_list = {}):
		self.champion_list = champion_list

	def champion_ids_list(self): #list of champion ids
		lst = []
		for each_champ in self.champion_list['data']:
			lst.append(self.champion_list['data'][each_champ]['id'])
		return lst #each element in the list is an integer
			

	def champion_dict(self): #dictionary of Champion Names (keys) and Champion ids (values)
		dct = {}
		for each_champ in self.champion_list['data']:
			dct[self.champion_list['data'][each_champ]['name']] = self.champion_list['data'][each_champ]['id']
		return dct
	

class Riot_Data(Cleaned_Champion_Data):
	def __init__(self, my_ranked_stats = {}, stat_summary = {}):
		Cleaned_Champion_Data.__init__(self, champion_list)
		self.my_ranked_stats = my_ranked_stats
		self.stat_summary = stat_summary

	
	def most_played_champions(self, champ_dict): #returns a sorted list of tuples that sorts it based on games played 
		dct = {}
		for each_champ in self.my_ranked_stats['champions']:
			for key in champ_dict:
				if(each_champ['id']==champ_dict[key]):
					dct[key] = each_champ['stats']['totalSessionsPlayed'] 
		return sorted(dct.items(), key = lambda x : (-x[1], x[0]))

	
	def ranked_win_percentage(self, champ_dict):
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
					if y['losses']+y['wins'] != 0:
						x = y['wins']/(y['losses']+y['wins'])
					else:
						print ("Unable to Calculate")
		return x


	def last_played_ranked_game(self):
		x = 0
		for y in self.stat_summary['playerStatSummaries']:
			for key in y:
				if(y['playerStatSummaryType']=="RankedSolo5x5"):
					x = y['modifyDate']
		date_ranked = time.strftime('%Y-%m-%d', time.localtime(x/1000))
		return date_ranked


	def last_played_flex_game(self):
		x = 0
		for y in self.stat_summary['playerStatSummaries']:
			for key in y:
				if(y['playerStatSummaryType']=="RankedFlexSR"):
					x = y['modifyDate']
		date_flex = time.strftime('%Y-%m-%d', time.localtime(x/1000))
		return date_flex


	def last_time_logged_in(self):
		summoner_date = summoner['revisionDate']
		date_general = time.strftime('%Y-%m-%d', time.localtime(summoner_date/1000))
		return date_general

data = Riot_Data(w.get_ranked_stats(summoner_id), w.get_stat_summary(summoner_id))

most_played_champions = (data.most_played_champions(data.champion_dict()))

most_played_champions_list = []
for x in most_played_champions:
	most_played_champions_list.append(x[1])

most_played_champions_list2 = []
for x in most_played_champions:
	most_played_champions_list2.append(x[0])

ranked_win_percentage = (data.ranked_win_percentage(data.champion_dict()))

ranked_win_percentage_list = []
for x in ranked_win_percentage:
	ranked_win_percentage_list.append(x[1])


ranked_win_percentage_list2 = []
for x in ranked_win_percentage:
	ranked_win_percentage_list2.append(x[0])


def graphing_most_played_champs():
	N = len(most_played_champions_list)
	mostplayed = most_played_champions_list
	
	ind = np.arange(N)  
	width = 0.35     

	fig, ax = plt.subplots()
	rects1 = ax.bar(ind, mostplayed, width, color='b')
	for rect in rects1:
	        height = rect.get_height()
	        ax.text(rect.get_x() + rect.get_width()/2., height,
	                '%d' % int(height),
	                ha='center', va='bottom')
	ax.set_ylabel('Number of Games Played') 
	ax.set_title('Most Played Ranked Champions')
	ax.set_xticks(ind + width)
	ax.set_xticklabels(most_played_champions_list2, rotation = 90) 
	plt.show()

def graphing_win_percentage():
	N = len(ranked_win_percentage_list)
	winpct = (ranked_win_percentage_list)
	
	ind = np.arange(N) 
	width = 0.4      

	fig, ax = plt.subplots()
	rects1 = ax.bar(ind, winpct, width, color='b')
	for rect in rects1:
	        height = rect.get_height()
	        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
	                '%d' % int(height),
	                ha='center', va='bottom')
	ax.set_ylabel('Win Percentage') 
	ax.set_title('Ranked Win Percentage by Champion')
	ax.set_xticks(ind + width)
	ax.set_xticklabels(ranked_win_percentage_list2, rotation = 90) 
	plt.show()

graphing_most_played_champs()
graphing_win_percentage()
print("Your Overall Ranked Win Percentage is:", data.overall_ranked_win_percentage())
print("Your Last Played Ranked Game was on:", data.last_played_ranked_game())
print("Your Last Played Ranked Flex Game was on:", data.last_played_flex_game())
print("The Last Time You Logged In Was:", data.last_time_logged_in())