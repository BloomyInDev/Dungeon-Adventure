import random, __main__
class Mecanism:
    def changeZone(zone:int,stopzone = ""):
        print("ChangeZone now !")
        print('Zone n'+str(zone))
        zone+=1
        #### The zone is 16x16
        oriwalls = [[1,1,1,1,1,1,2,2,2,2,1,1,1,1,1,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
                    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
                    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
                    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,1,1,1,1,1,2,2,2,2,1,1,1,1,1,1]]
        newwalls = oriwalls.copy()
        if zone > 32:
            tempzone = 32
        else:
            tempzone = zone
        for i in range(tempzone):
            recreate = True
            while recreate:
                x, y = random.randint(0,len(newwalls)-1), random.randint(0,len(newwalls[0])-1)
                #print("Try",x,y)
                if newwalls[y][x] == 0:
                    if not(x in [1,6,7,8,9,13] or y in [1,6,7,8,9,13]):
                        #print(x, y)
                        newwalls[y][x] = 1
                        recreate = False
        return newwalls, zone
    def chestLoot():
        possibleitems = []
        possibleitems.extend(["pistol" for i in range(30)])
        possibleitems.extend(["health" for i in range(30)])
        possibleitems.extend(["dsword" for i in range(40)]) # All of that is for repartition equilibrate the game
        return possibleitems[random.randint(0,len(possibleitems)-1)]