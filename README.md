# clashroyale-stats
statsroyale scrapper to get stats

Exploratory Data Analysis of my Clash Royale account data:

https://www.kaggle.com/jonathanbouchet/jose-vicente-s-data-on-clash-royal

https://www.kaggle.com/pepe93/eda-of-my-clash-royale-battles/notebook



### NOTE: 
I've realised that CR-api project includes battles info so it's very likely this project will use CR-api in the future.


<br>

Go to https://statsroyale.com and follow the instructions. You need to generate your matches history.

Now you need to modify the file USER_ID.py and put between the 's your Clash Royale ID.

Then, install the dependencies on requirements.txt by running the following line. Please note you need Python 3.5.:

pip install -r requirements.txt

Now, run the following line:

scrapy crawl crSpider

That will generate a csv file with the info of your matches. Every time you want to save new matches you need to visit https://statsroyale.com/profile/<YOUR-CLASH-ROYALE-ID> and press the button "Refresh battles". That website only shows the last 25 matches.

As you can see, there is a script named clash-royale-for-da.py. This script generates a csv file from the original with card variables with only their levels (in case a member of the match didn't have that card in his deck, the level of that card will be 0). 

Note: Refactoring for this project is on my personal to-do list. I'm aware the code is "quick and dirty" and please have that in mind. There are other projects in my GitHub profile that look better, trust me ;)
