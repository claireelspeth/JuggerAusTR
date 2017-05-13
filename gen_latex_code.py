import shutil
import numpy
import pandas
import datetime

# initialise variables
cardtext = "" 
char_break = 50 # number of characters allowed before we reduce font size
char_limit = 80 # number of characters allowed before we reject the text completely
num_chars = 0
cost_min = 1
cost_max = 6

stat_min = 0
stat_max = 9

name_break = 15
name_lim = 20

# log exceptions
log_file = open('gencode_logs.txt','w+')
log_file.write('Begin Log at ' + str(datetime.datetime.now()) +'\n')
log_file.close()      
Track_card_errors = ''# list errors found in input code
# Types of error:
# too much text in name/team/flavour text
# non-integer cost/stats
#cost/stats out of range
# color not available
# image does not exist

# copy preamble into new file
shutil.copyfile('preamble.txt','latex_output.txt')

# read in color options (may choose to write new colors into preamble at appropriate space?)
colors = pandas.read_csv('Card_colors.csv')
for rows in range(0,len(colors.index)):
    colors.Color[rows]=str.lower(colors.Color[rows])
    colors.Color[rows] = colors.Color[rows].strip()
# open file for appending
f = open('latex_output.txt','a')

# read in df for player cards
df= pandas.read_csv('PlayerCards.csv')
color_exists = df.TeamColour.isin(colors.Color)

df = df.replace(numpy.nan, '', regex=True) # replace missing data with empty string

for rows in range(0, len(df.index)):
    # need try/exception statements to handle input errors 
    cardtext = '\playercard{'
    try:
        if color_exists[rows]==True:
            cardtext = cardtext +df.TeamColour[rows] + '}{'
        else:
            cardtext = cardtext +'gray}{'
            f.close()
            log_file = open('gencode_logs.txt','a')
            log_file.write('Color selected for Player Card number ' + str(rows) +' does not exist. \n Please add new color to preamble')
            log_file.close()
            f = open('latexcode.txt','a')
    except:
        cardtext = cardtext +'gray}{'
        f.close()
        log_file = open('gencode_logs.txt','a')
        log_file.write('Incorrect value for color for Player Card number ' + str(rows))
        log_file.close()
        f = open('latexcode.txt','a')

    try:
        df.Name[rows] = df.Name[rows].strip() # trim whitespace
        # code to ensure only first letter is caps
        df.Name[rows].title()
        df.Team[rows] = df.Team[rows].strip() # trim whitespace
        # code to ensure only first letter is caps
        df.Team[rows].title()
        num_chars = len(df.Name[rows]) + len(df.Team[rows])

        if (num_chars <= name_break):
            cardtext = cardtext+df.Name[rows] +' ('+df.Team[rows] +')}'
        elif (num_chars > name_break and  num_chars<= name_limit): # reduce size of text if there is too much
            cardtext = cardtext+'\small{'+df.Name[rows] +' ('+df.Team[rows] +')}}'
        elif (num_chars > num_limit):    # truncate text if there is too much
            cardtext = cardtext+'\small{'+df.Name[rows][0:name_limit] +' ('+df.Team[rows][0:(name_limit-len(df.Name[rows][0:name_limit]))] +')}}'
            f.close()
            log_file = open('gencode_logs.txt','a')
            log_file.write('Name/Team too long for Player Card number ' + str(rows))
            log_file.close()
            f = open('latexcode.txt','a')

    except:
        cardtext = cardtext+'Jugger no.' +str(rows)
        f.close()
        log_file = open('gencode_logs.txt','a')
        log_file.write('Incorrect name/team value for Player Card number ' + str(rows))
        log_file.close()
        f = open('latexcode.txt','a')
        
    cardtext = '{\charisma{black}{' + str(df.Cost[rows])+ \
    '}}{\\textit{LVL}}{\\begin{tikzpicture}[fill opacity = 0](0,0)\n\\node[anchor = south west] at (0,0) {\LevelStats{gray}{' +str(df.Lv1ATK[rows]) + \
    '}{}{' + str(df.Lv1DEF[rows])
    print(cardtext)
    num_chars = len(df.Text_main[rows]) + len(df.Text_flavour[rows])
    if (num_chars <= char_break):
        textbox_text = df.Text_main[rows] + '\\newline \\textit{' + df.Text_flavour[rows] +'}'
    elif (num_chars > char_break and  num_chars<= char_limit): # reduce size of text if there is too much
        textbox_text = '\small{'+df.Text_main[rows] + '\\newline \\textit{' + df.Text_flavour[rows] +'}'
    elif (num_chars > char_limit):    # truncate text if there is too much
        textbox_text = '\small{'+df.Text_main[rows][0:char_limit] + '\\newline \\textit{' +  df.Text_main[rows][0:(char_limit-len(df.Text_main[rows][0:char_limit]))] +'}'
        f.close()
        log_file = open('gencode_logs.txt','a')
        log_file.write('Too much flavour text for Player Card with Name ' + df.Name[rows])
        log_file.close()
        f = open('latexcode.txt','a')
    print(textbox_text)
    try:
        card_cost = int(df.number[rows])
        print(card_cost)
        if (card_cost<=cost_max and card_cost>=cost_min):
            print('\cost{black}{'+str(df.number[rows]) + '}{}')
        else:           
            card_cost= min(card_cost,cost_max)
            card_cost= max(card_cost,cost_min)    
            print('\cost{black}{'+str(card_cost) + '}{}')       
    except:
        #Handle the exception
        print('\cost{black}{E}{}')
        f.close()
        log_file = open('gencode_logs.txt','a')
        log_file.write('Incorrect cost value for Player Card with Name ' + df.Name[rows])
        log_file.close()
        f = open('latexcode.txt','a')
    
# Create the following LaTeX code for each player card
 #\playercard{green}{Enforcer (South)}{\charisma{black}{1}}{\textit{LVL}}{\begin{tikzpicture}[fill opacity = 0](0,0)
#\node[anchor = south west] at (0,0) {\LevelStats{gray}{1}{}{2}{}{2}{}{3}};
#\node[anchor = south west] at (11mm,0){\LevelStats{black}{2}{}{3}{}{4}{}{4}};
#\node[anchor = south west] at (22mm,0){\LevelStats{gray}{3}{}{4}{}{4}{}{6}};
#\node[anchor = south west] at (33mm,0){\LevelStats{black}{4}{}{6}{}{6}{}{8}};
#\end{tikzpicture}}{Receive an additional {\inlinecost{black}{2}} at the beginning of each turn\\\ \\\textit{Hi!}}{}{}{C:/Users/Cake/Pictures/2015-08/cakeDerp.jpg};   
    
# append closing statment
f.write('\end{document}')

# close file
f.close()

# what try/catch clauses do I need? eg. non single digit integer entries for stats would be a problem.         print("you may need to trim whitespace or use tolower")

# how should I handle a paragraph of text that might have too much content and need to have the fontsize changed?
# and what about if I want to have a paragraph of normal text and italics text? Guess I would need two columns

# what data analysis can I perform? Cost distribution. Frequency of skills. etc
