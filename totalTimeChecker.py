from sc2reader.factories import SC2Factory
import os, csv

replayPath = unicode(os.getcwd()) + "/glabVIII"
dirListing = os.listdir(replayPath)
sc2 = SC2Factory()

def timeAdjuster(secondsSum):
    """Adjusts 1.4 minutes to 1.0 minutes, return minutes"""

    a, b, c = 1.4, secondsSum, 1.0
    x = (b*c)/a
    return x/60.0

# Rename files to avoid issues with non-ASCII characters
for num, filename in enumerate(dirListing):
    if not filename.startswith("temp") and filename.endswith(".SC2Replay"):
        os.rename(os.path.join(replayPath, filename), os.path.join(replayPath, 'temp' + str(num) + '.SC2Replay'))

# Refresh directory contents
dirListing = os.listdir(replayPath)

timeDict = {}
for filename in dirListing:
    if not filename.startswith("glab") and filename.endswith(".SC2Replay"): # Loop over re-named files only
        replay = sc2.load_replay(os.path.join(replayPath, filename), load_level=4)

        userName = str(replay.teams[0])[str(replay.teams[0]).rfind('g'):str(replay.teams[0]).rfind('(')]
        gameDate = str(replay.end_time)
        gameLength = str(replay.game_length)

        for num, ev in enumerate(replay.events):
            if ev.name == 'PlayerLeaveEvent':
                leaveIndex = num-1
                break
            else:
                leaveIndex = 'None'

        if leaveIndex == 'None':
            print "No PlayerLeaveEvent!"
            exit()

        gameLengthEst = replay.events[leaveIndex].second

        if gameLength.count('.') == 1:
            gameLength = (int(gameLength[:gameLength.find('.')])*60)+(int(gameLength[gameLength.find('.')+1:]))
        elif gameLength.count('.') == 2:
            gameLength = ((int(gameLength[:gameLength.find('.')])*3600)+
                          (int(gameLength[gameLength.find('.')+1:gameLength.rfind('.')])*60)+
                          (int(gameLength[gameLength.rfind('.')+1:])))

        if userName in timeDict and gameDate not in timeDict[userName][1]:
            timeDict[userName][0].append(gameLength)
            timeDict[userName][1].append(gameLengthEst)
            timeDict[userName][2].append(gameDate)
        else:
            timeDict[userName] = [[gameLength], [gameLengthEst], [gameDate]]

for key in timeDict:
    adjGameLength = timeAdjuster(sum(timeDict[key][0]))
    adjGameLengthEst = timeAdjuster(sum(timeDict[key][1]))

    print str(key)+' gameLength: '+str(adjGameLength/60.0)+'     gameLengthEstimate: '+str(adjGameLengthEst/60.0)
