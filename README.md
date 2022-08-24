# FantasyFootball
I first started watching football and playing Fantasy Football during the 2020 season. I was roommates with 11 other guys in an apartment in SF and needed to play so they could have enough people. It was a $20 dollar buy-in, now up to $100, with a pay structure of 3rd getting their money back, 2nd making some profit and the rest going to 1st place. They also decided to create a punishment for last place and agreed that the 1st place winnings would help pay for any punishment.

I got last place that season...
They cut my hair to look like a monk.

That slight will not go unpunished.

So I decided to make an algorithm to win. I needed something to guide me when picking players during the draft, who to start/sit, and who to trade. The next season (2021) I got third place, but was in first until the finals. My system won me great trades such as getting Johnathan Taylor for Ezekiel Elliot week 3. While I did not win first, this showed improvement and encouraged me to keep working on it.

# Strategy
Last year, I implemented an opportunity-based system for trading running backs (RBs). The idea is a common one in Fantasy Football. You should look at the amount of opportunities a player gets. While actual points and more descriptive statistics are better for describing what a player did. Opportunity statistics can tell us what could have been.

The predictive nature of these statistics intrigued me. After 2 weeks of Ezekiel Elliot's lackluster performance. He scored 5.9 week 1 and 17.7 week 2. I decided to look at other top rated RBs that were performing as bad as Elliot, but who had more opportunities than Elliot. This led me to find Johnathan Taylor. Taylor scored 17.6 week 1 and 6.3 week 2. (data). The trade deal was made going into week 3, so we would each have one more game with our original RBs.

All of my league mates, except for one, were telling me that I was being robbed and that they would veto the trade if I told them to. I believe they were doing this out of the kindness of their hearts. I had come in last the year before and they were rightfully worried for me. After week 3, Ezekiel Elliot had an amazing game. 26.6 fantasy points, whereas Taylor only had 8.2. I was worried that I had been wrong; my league mates again offered to veto, but I decided to go through with the trade.

 (Post trade).

# TODOs

Bug found in CollectPlayerData. Need to fix or help nflfastpy api work

accuracy metric for ECR, ADP, and VOR fantasy predictions

normal distribution of recovery time per injury

save to SQL or google sheets instead of CSV

look into argparse package

look into Faust event bus

add decision trees after adding events