# define a function to turn tournament rank into points    
def calculate_rankpoints(maxpoints, rank):
  # linear distribution of ranking points such that
  # team ranked first gets max_points and
  # team ranked last gets 1 point
    slope = (maxpoints-1)/(1-numteams)
    intercept = 1 - numteams*slope
    rankpoints = slope*rank+ intercept
   
    return rankpoints

# define a function to determine time decay weighing of tournament
def check_date(checkyear, checkmonth, tournament_year, tournament_month):
    if checkyear == tournament_year:
        if checkmonth <= tournament_month:
            # tournament hasn't happened yet!
            Weighting =0       
        else:
            Weighting = 1          
    elif checkyear - tournament_year == 1:
        if checkmonth <= tournament_month:
            Weighting = 1             
        else:
            Weighting = 0.5            
    elif checkyear - tournament_year == 2:
        if checkmonth <= tournament_month:
            Weighting = 0.5             
        else:
            Weighting = 0.25
    elif checkyear - tournament_year == 3:
        if checkmonth <= tournament_month:
            Weighting = 0.25            
        else:
            Weighting =0            
    else:
        Weighting =0
    return Weighting   

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


# number of games that count towards aggregate rankings scores
NumCounted = 5

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

# Read in tournament details
numgames= 0
for l in open('Tournaments.txt').readlines():
    if (not l.startswith('#') and not l.startswith('\n')): # remove preamble text and new lines
        l.strip()
        l=l.split(',')
        try:
            # compile teams data
            r= int(l[0]) # rank as integer
            t= (l[1].strip()) # team with whitespace removed
           # add new teams to full team list
            Teams = set(list(Teams)+[t])
            try:
                Participants.update({t: r})
                Tournament[numgames-1].update({'Teams':Participants}) # add new entries
            except:
                print('I skipped an entry as I could not read it')
        except:
            # create new tournament listing
            if l[0].strip().capitalize()=='Points':                
                Tournament[numgames].update({'Points': int(l[1])})
                numgames = numgames+1
                Participants = {}
            else:               
                Tournament[numgames]={}
                Tournament[numgames].update({'Location': l[0]}) 
                try:
                    d=datetime.strptime(l[1].strip(), '%m/%Y')
                    w = check_date(checkyear, checkmonth, d.year, d.month)
                    Tournament[numgames].update({'Weighting': w})
                except:
                    print('Date is not in correct format, ignoring this data')                   
                    Tournament[numgames].update({'Weighting': 0})
        
for t in Teams:
    Scores[str(t)] = []
    Weights[str(t)] = []
    RankingLadder[str(t)] = []
    
for game in range(0,len(Tournament)):
    Participants = list(Tournament[game]['Teams'].keys())
    numteams = len(Participants) # global variable
    
    # what if teams don't want to be ranked and
    # the person entering data didn't provide all data?
    if max((Tournament[game]['Teams'].values())) > numteams:
        numteams = max(Tournament[game]['Teams'].values())

    # determine score for each participant
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
