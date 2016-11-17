# My API Key: RGAPI-76f4bcb6-da64-455a-aad2-07eee7ad0e8f
# Rate Limits:
# 500 requests every 10 minutes
# 10 requests every 10 seconds

# more info: https://github.com/pseudonym117/Riot-Watcher
from riotwatcher import RiotWatcher

w = RiotWatcher("RGAPI-76f4bcb6-da64-455a-aad2-07eee7ad0e8f")

#check to see if we have API Calls Remaining 
print (w.can_make_request()) 

who_are_you = str(input("Please enter your summoner name:"))
summoner = w.get_summoner(name = who_are_you)
print (summoner)

my_ranked_stats = w.get_ranked_stats(summoner['id'])
#print(my_ranked_stats)