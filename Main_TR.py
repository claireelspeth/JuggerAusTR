# define a function to turn tournament rank into points    
def calculate_rankpoints(maxpoints, rank):
  # linear distribution of ranking points such that
  # team ranked first gets max_points and
  # team ranked last gets 1 point
    slope = (maxpoints-1)/(1-numteams)
    intercept = 1 - numteams*slope
    rankpoints = slope*rank+ intercept
   
    return rankpoints


# begin main code

from datetime import datetime
today = datetime.now()
# use today's date
checkyear = today.year
checkmonth = today.month
# if you want to explore the team ladder at a past or future date you can
# by uncommenting the code here
#checkyear = 2016
#checkmonth = 12

# Initial list of teams
Teams = []

# global variable for number of teams in a tournament,
# updates in main code and used in functions
global numteams 

# Initial dictionary of scores and tournament weights and ranks
Scores = dict()
Weights = dict()
Tournament = dict()
RankingLadder = dict()
# What about allowing pre-filled scores data?
# That would need to be linked to dates and weights recalculated
# Easier for me to write code to reculate everything from tournament results

# number of games that count towards aggregate rankings scores
NumCounted = 5

# Tournament details? who played in each tournament? how did they rank?
Tournament[0] = {'Location':'Brisbane','Date': '09/2015','Points': 16,
              'Teams': {'Skullduggery':1,'Mountain Men':2,'Flaily Wailies':3,'Space Pirates':4,'Newcastle Blitzkrieg':5,'MERCs':6}}

Tournament[1] = {'Location':'Newcastle','Date': '03/2016','Points': 8,
              'Teams': {'Skullwailies':1, 'Bees':1,'MERCs':3,'Newcastle Blitzkrieg':4}} 
Tournament[2] = {'Location':'Brisbane','Date': '07/2016','Points': 16,
              'Teams': {'Skullduggery':1,'Mountain Men':2,'Flaily Wailies':3,'Opposition':4,'QUT':5}} 
Tournament[3] = {'Location':'Canberra',
              'Date': '10/2016','Points': 16,
              'Teams':{'Bees':1,'Second Spars':2,'Pompfen Pals':2,'Motley Crew':4,'Owls':5,'Newcastle Blitzkrieg':6,'Space Pirates':6}} 
Tournament[4] = {'Location':'Toowoomba','Date': '04/2017', 'Points': 2,
              'Teams':{'Motley Crew':1,'Highland Dragons':2}} 
# can I read this data in as a text or JSON file?


#d = {}
#with open("file.txt") as f:
 #   for line in f:
  #     (key, val) = line.split()
   #    d[int(key)] = val
f = open('Tournaments.txt','r')
content = f.readlines()
f.close()
for l in open('Tournaments.txt').readlines():
    if not l.startswith("#"): # remove preamble text
        print(l) # print tournament data


for game in range(0,len(Tournament)):
    # how long ago was that tournament? What is the weighting of scores?
    try:
        tournamentdate = datetime.strptime(Tournament[game]['Date'], '%m/%Y')             
    except:
        print('Please enter all dates with numerical data in the format month/year ')    

    if checkyear == tournamentdate.year:
        if checkmonth <= tournamentdate.month:
            # tournament hasn't happened yet!
            Tournament[game].update({'Weighting': 0})       
        else:
            Tournament[game].update({'Weighting': 1})            
    elif checkyear - tournamentdate.year == 1:
        if checkmonth <= tournamentdate.month:
            Tournament[game].update({'Weighting': 1})            
        else:
            Tournament[game].update({'Weighting': 0.5})            
    elif checkyear - tournamentdate.year == 2:
        if checkmonth <= tournamentdate.month:
            Tournament[game].update({'Weighting': 0.5})            
        else:
            Tournament[game].update({'Weighting': 0.25})            
              
    elif checkyear - tournamentdate.year == 3:
        if checkmonth <= tournamentdate.month:
            Tournament[game].update({'Weighting': 0.25})            
        else:
            Tournament[game].update({'Weighting': 0})            
    else:
        Tournament[game].update({'Weighting': 0})            

    # append all teams not already in team list
    Participants = list(Tournament[game]['Teams'].keys())
    
    # clean data to reduce human data entry errors
    for t in range(0,len(Participants)): 
        Participants[t].strip() # trim white space
       # Participants[t].title() # homogenise caps/lowercase, comment out if unwanted
        
    newteams = set(Participants)-set(Teams)	
    Teams.extend(list(newteams))
    for t in newteams:
        Scores[str(t)] = []
        Weights[str(t)] = []
        RankingLadder[str(t)] = []

    # determine score for each participant
    numteams = len(Tournament[game]['Teams']) # global variable
    # what if teams don't want to be ranked and
    # the person entering data didn't provide all data?
    if max(Tournament[0]['Teams'].values()) > numteams:
        numteams = max(Tournament[0]['Teams'].values())
    for t in Participants:
        rank = calculate_rankpoints(Tournament[game]['Points'],Tournament[game]['Teams'][str(t)])
        Scores[str(t)].append(rank)
        Weights[str(t)].append(Tournament[game]['Weighting'])

# aggregate weighted scores and select best
for t in Teams:
    for game in range(0,len(Scores[str(t)])): # such that team participated?
        weightedscore = Scores[str(t)][game] * Weights[str(t)][game]
        RankingLadder[str(t)].extend([weightedscore])
    aggscore = sorted(RankingLadder[str(t)],reverse=True)
    aggscore= sum(aggscore[0:NumCounted])
    RankingLadder[str(t)]=aggscore

rankvals = list(RankingLadder.values())
RankingList = [x for (y,x) in sorted(zip(rankvals,Teams),reverse=True)]
rankvals = sorted(rankvals,reverse=True)
# desired output RankingLadder = {rank: {Team, Score}}
# rank can't be a key when we can have multiple teams at the same rank
RankingLadder = dict()
r = 1
for t in range(0,len(Teams)):
    RankingLadder[RankingList[t]] = [r,rankvals[t]]
    try:
        if rankvals[t+1] < rankvals[t]:
            r=r+1
    except:
        print('')

print(RankingLadder)

# export stuff to files?
