# NBAStatsVisualization
Just an avid fan (Miami Heat) playing around with NBA data to get cool relationships

### Ideas:

* Player shot chart weighted into how deep into a game/season
* Different combos of (PTS, AST, REB, STL, BLK) vs (Point Differential and wins)
* Clusters of players based on metric (FG%, STL+BLK, etc..)  (Hierarchial to get some sense of tiers of players, Categorical for player types: shooter, defender, 2-way, 3&D, athletic, etc)
* Playoff vs Regular season comparisons of:
    a) Homecourt Advantage
    b) player stats -> Use the difference to get tiers of players who "step it up", stay the same, underperform (choke, etc)
    c) point differential -> Does it actually get harder to win in the playoffs?
* Shot attempts vs distance through a game and figure out IMPORTANT shots ("Takeover" moments or "heat-check" shots)
* Further extension to use twitter API to find tweets about players heating up
* How to figure out quality of team based on team shot chart efficiency?

### Integration Ideas:

* Use with AWS services Cloudfront, APIGateway, Lambda, DynamoDB, Cloudwatch to continuosly update
* Integrate with social media (e.g twitter API)
* Add a mobile app/website aspect to this (Angular/ReactJS)

### Sources
Utilizing API's written against nba.com found here: https://github.com/swar/nba_api
#### Resources 
Peter Beshai ----> https://peterbeshai.com/
1) https://buckets.peterbeshai.com/app/#/playerView/201935_2015
2) https://shotline.peterbeshai.com/
3) http://savvastjortjoglou.com/nba-shot-sharts.html
