# FantasyFootball
I first started watching football and playing Fantasy Football during the 2020 season. I was roommates with 11 other guys in an apartment in SF and needed to play so they could have enough people. It was a $20 dollar buy-in, now up to $100, with a pay structure of 3rd getting their money back, 2nd making some profit and the rest going to 1st place. They also decided to create a punishment for last place and agreed that the 1st place winnings would help pay for any punishment.

I got last place that season...
They cut my hair to look like a monk.

That slight will not go unpunished.

So I decided to make an algorithm to win. I needed something to guide me when picking players during the draft, who to start/sit, and who to trade. The next season (2021) I got third place, but was in first until the finals. My system won me great trades such as getting Johnathan Taylor for Ezekiel Elliot week 3. While I did not win first, this showed improvement and encouraged me to keep working on it.

# 2021 Trade
During the 2021 season, I implemented an opportunity-based system for trading running backs (RBs). The idea is a common one in Fantasy Football. You should look at the amount of opportunities a player gets. While actual points and more descriptive statistics are better for describing what a player did. Opportunity statistics can tell us what could have been.

The predictive nature of these statistics intrigued me. After 2 weeks of Ezekiel Elliot's lackluster performance. He scored 5.9 week 1 and 17.7 week 2. I decided to look at other top rated RBs that were performing similarly to Elliot, but have better opportunity statistics than Elliot. This led me to find Johnathan Taylor. Taylor scored 17.6 week 1 and 6.3 week 2. Numbers very similar to Elliot. While Taylor seemed to get a similar share of his team's rushing attempts as Elliot, I noticed that Elliot's backup Tony Pollard was taking a sizable chunk of his rushing share. I decided to trade Elliot for Taylor going into week 3, this caused us to have one more game with our original RBs.

All of my league mates, except for one, were telling me that I was being robbed and that they would veto the trade if I told them to. I believe they were doing this out of the kindness of their hearts. I had come in last the year before and they were rightfully worried for me. After week 3, Ezekiel Elliot had an amazing game. 26.6 fantasy points, whereas Taylor only had 8.2. I was worried that I had been wrong; my league mates again offered to veto, but I decided to go through with the trade.

The next week Taylor barely beat Elliots 20.3 points by .1 point. After that, it wasn't even close. Week 5 Taylor got my team 31.9 points (The second highest that week). From that week on, Taylor rose to the number 1 RB for the 2021 season. Finally placing in the top 3 after coming dead last a season earlier would not have happened without Johnathan Taylor and advanced analytics.

# TODOs

accuracy metric for ECR, ADP, and VOR fantasy predictions

normal distribution of recovery time per injury

save to SQL or google sheets instead of CSV

look into argparse package

look into Faust event bus

add decision trees after adding events