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

# Initial list of teams
Teams = []

# global variable for number of teams in a tournament,
# updates in main code and used in functions
global numteams 

# Initial dictionary of scores and tournament weights
Scores = dict()
Weights = dict()
Tournament = dict()

# recommended max points for tournament:
# MAJOR 16
# MINOR 8
# LOCAL GAMES DAY 4
# 1v1 GAME 2

# number of games that count towards aggregate rankings scores
NumCounted = 5

# who played in each tournament? how did they rank?
Tournament[0] = {'Location':'Brisbane','Date': '09/2015','Points': 16,
              'Teams': {'Skullduggery':1,'Mountain Men':2,'Flaily Wailies':3,'Space Pirates':4,'Newcastle Blitzkrieg':5,'MERCs':6}}

Tournament[1] = {'Location':'Newcastle','Date': '03/2016','Points': 8,
              'Teams': {'Skullwailies':1, 'Bees':1,'MERCs':3,'Newcastle Blitzkrieg':4}} 
Tournament[2] = {'Location':'Brisbane','Date': '07/2016','Points': 16,
              'Teams': {'Skullduggery':1,'Mountain Men':2,'Flaily Wailies':3,'Opposition':4,'QUT':5}} 
Tournament[3] = {'Location':'Canberra',
              'Date': '10/2016','Points': 16,
              'Teams':{'Bees':1,'Second Spars':2,'Pompfen Pals':2,'Motley Crew':4,'Owls':5,'Newcastle Blitzkrieg':6,'Space Pirates':6}} 
Tournament[4] = {'Location':'Toowoomba','Date': '04/2017', 'Points': 3,
              'Teams':{'Motley Crew':1,'Highland Dragons':2}} 

# append toowoomba game day
#IDlist= Tournaments['ID']
#IDlist = IDlist.append('Toowoomba2017')
#Datelist = Tournaments['Date']
#Datelist= Datelist.append('04/2017')
#Pointslist = Tournaments['Points']
#Pointslist = Pointslist.append(3)

for game in range(0,len(Tournament)):
    # how long ago was that tournament? What is the weighting of scores?
    try:
        tournamentdate = datetime.strptime(Tournament[game]['Date'], '%m/%Y')             
    except:
        print('Please enter all dates with numerical data in the format month/year ')    

    if today.year == tournamentdate.year:
        Tournament[game].update({'Weighting': 1})            
    elif today.year - tournamentdate.year == 1:
        if today.month <= tournamentdate.month:
            Tournament[game].update({'Weighting': 1})            
        else:
            Tournament[game].update({'Weighting': 0.5})            
    elif today.year - tournamentdate.year == 2:
        if today.month <= tournamentdate.month:
            Tournament[game].update({'Weighting': 0.5})            
        else:
            Tournament[game].update({'Weighting': 0.25})            
              
    elif today.year - tournamentdate.year == 3:
        if today.month <= tournamentdate.month:
            Tournament[game].update({'Weighting': 0.25})            
        else:
            Tournament[game].update({'Weighting': 0})            
    else:
        Tournament[game].update({'Weighting': 0})            

    # append all teams not already in team list
    Participants = list(Tournament[game]['Teams'].keys())
    newteams = set(Participants)-set(Teams)	
    Teams.extend(list(newteams))
    for t in newteams:
        Scores[str(t)] = []
        Weights[str(t)] = []

    # determine score for each participant
    numteams = len(Tournament[game]['Teams']) # global variable
    for t in Participants:
        rank = calculate_rankpoints(Tournament[game]['Points'],Tournament[game]['Teams'][str(t)])
        Scores[str(t)].append(rank)
        Weights[str(t)].append(Tournament[game]['Weighting'])

print(Scores)
print(Weights)

# weight scores and select best scores


