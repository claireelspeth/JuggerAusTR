# JuggerAusTR
Contents:
* Code for a team ranking system
* Test data
* Example output

I have had time to work on this again recently! I want to propose something and I need people to help me test the proposed system by trying to break, game it or point out flaws I have missed.

Unfortunately, the results from the Canberra tournament broke the system I was working on previous where you earn more points by beating a team ranked more highly than your team. If you weren't there/don't remember, we had a lot of new teams as well as two teams merging on the second day due to injuries. To handle this problem, while maintaining fairness and transparency, an additive system similar to the German tournament rankings seems to be best.

1. Each tournament has the number of points it is worth announced beforehand
2. Points become worth less over time
3. Only your 5 best results count

Why is this good? Point 1 makes tournament rankings more transparent, particularly when number of teams changes on the day, while points 2 and 3 handle most of the problems with an additive points system.

Point 1 also means you know in advance which tournaments to attend if you are interested in competitive rankings, so if you can't travel frequently you can prioritise your tournaments. Major tournaments would only be a couple per year. Local game days could also contribute to team rankings but would not be worth as much. 

Point 2 keeps the results current - if a team stops playing they can't hog the top spot forever.

Point 3 is important - maybe not straight away because the number of tournaments is pretty small - but is definitely important if we allow local game days to count.
It means that you can play as many ranked games as you like, and you will never lose points by doing so, but you cannot rise to the top of the ranking ladder by spamming easy matches. It also helps to balance the distance problem we have in Australia. If you are able to drive for a couple of hours a pop and get to lots of ranked games in a year then good on you, but that doesn't mean your team should always be able to rank higher than a team that has to spend $100's on flights per person or take 1 to 2 days off work for driving to get to a single game. To maintain fairness, but also encourage teams to play multiple games per year, we cap it. The choice of 5 as the game cap is up for debate but is reasonable. It allows for 2 major tournaments each year for two years to count + 1 extra game somewhere.

The trick then become deciding how many point each tournament/game day is worth, and how the points pool gets distributed amongst participating teams. I didn't find the maths for the German rankings so I've gone with something different that gives reasonable results.

1. Instead of a points pool, tournament organiser post the maximum number of points for 1st place
2. Last place is always worth the same amount of points
3. Create a linear function (depending on max points & number of teams) to determine points for each rank
4. Teams earn points based on their final ranking at the end of the tournament

This is simple enough that people should be able to calculate by themselves where they need to place in a tournament to change their overall rank.
Some cons: Beating a team by a landslide or beating a team ranked higher than you doesn't give you more points.
Some pros: There is no incentive to brutalise less experienced teams by beating them by a landslide (unless tournaments use points earned for final rank) and the system doesn't need prior information about the ranking of each team you played in order to work.
A linear points distribution normalised with a max/min for 1st/last place is......highly debateable. Maths people, I looked at exponential and a few other functions but picked linear for simplicity and because final results across multiple tournaments felt right. If you want to argue the case for something else, we can easily test it.

Testing should be easy. I wrote some Python code and placed it on Github. You can help in two ways. 1) Download the files and test different parameters/scenarios yourself. 2) Send me mock tournament results to test that you think will break the system and produce stupid results.

Sending me new results to test:
I need one file with all games you want me to test. It should look like this:
Coober Pedy, 10/1989
Points, 9
1, The Salute of the Jugger
2, The Blood of Heroes

Testing it yourself:
https://github.com/claireelspeth/JuggerAusTR
(P.S. Please be kind with feedback on the code - I'm newish to python and still learning ways to do things more efficiently)
