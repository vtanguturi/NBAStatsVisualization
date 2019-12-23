# NBAStatsVisualization
Just an avid (Miami Heat) fan playing around with NBA data in my spare time

### Ideas:

* [DONE] Different combos of (PTS, AST, REB, STL, BLK) vs (Point Differential and wins)
* [DONE] Clusters of players based on metric (FG%, STL+BLK, etc..)  (Hierarchial to get some sense of tiers of players, Categorical for player types: shooter, defender, 2-way, 3&D, athletic, etc)
* Determine and predict who will win a game
	a) [DONE] Compare teams in a game based on different recorded stat accumulation in quarter-bucketized metrics
	b) Predict outcome of the game based on difference of the stats in the comparision
* [Can't do this no way to get info] Playoff vs Regular season comparisons of:
    a) Homecourt Advantage
    b) player stats -> Use the difference to get tiers of players who "step it up", stay the same, underperform (choke, etc)
    c) point differential -> Does it actually get harder to win in the playoffs?
* Figure out quality of team (Offensive efficiency) based on team shot chart efficiency
* Player shot chart weighted into how deep into a game, and then extend it to how deep into a season
* Determine IMPORTANT shots ("Takeover" moments or "heat-check" shots)
	a) Maybe shot chart vs distance from the rim (usually players pull from deep when they are feeling it)

### Integration/Extension Ideas:

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
