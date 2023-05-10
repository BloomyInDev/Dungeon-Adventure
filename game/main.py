import pyxel, time
from player import *
from enemy import *
from scenery import *
from mecanism import *
normalfps = 30
config={'screen':[128,137],'fps':60}
equipements = {
    "sword": {'delay':28,'atk':1 ,'wait':10},
    "dsword":{'delay':32,'atk':1 ,'wait':12},
    "pistol":{'delay':8 ,'atk':1 ,'wait':8 ,'specialvar':{'ammo':24}}
}
pyxel.init(config['screen'][0], config['screen'][1], title="Dungeon Game", fps=config['fps'])
pyxel.load("resources.pyxres")
pyxel.mouse(True)
animationtick = 0
tick = 0
lastestchangeitem = 0
player = {"x":60,"y":60,"equipement":{"list":["sword"],"inhand":0,"used":False,"delay":0,'specialvar':{'ammo':20,"listbullet":[]}},"dir":"u","score":0,"life":4}
enemies = {"wait":False,"list":[]}

scenary = {"walls":0,"tp":0,"chest":{"state":0,'gift':None,'timegiven':None},"endgame":False}
zone = 1
pyxel.playm(0,loop=True)
def changeTheZone():
    global walls,zone,enemies
    print(zone)
    if scenary["chest"]["state"] == 2:
        scenary["chest"]["state"] = 0
    walls, zone = Mecanism.changeZone(zone)
    enemies["list"] = []
    for i in range(2,zone):
        enemies["list"].append(Enemy.spawn(walls))
    #print(enemies)
    pyxel.play(3,3)
# =========================================================
# == UPDATE
# =========================================================
def update():
    """Update everything in the game (always at fps)"""
    global player,animationtick,tick
    # update player vars
    if player["life"]>0:
        if tick == config['fps']: tick = 0
        else: tick += 1
        animationtick = (tick//config["fps"])*normalfps
        #print(scenary['chest'])
        if zone%5==0 and scenary["chest"]["state"] != 2:
            scenary["chest"] = Scenery.spawnchest()
            #print(Player.colidingChest(player["x"],player["y"],True))
        elif scenary["chest"]["state"]==0: scenary["chest"] = {"state":0}
        if tick%(config["fps"]//normalfps) == 0: 
            player["x"], player["y"], player["equipement"]["delay"], player["dir"], scenary["chest"] = Player.move(player["x"], player["y"], player["equipement"]["delay"], player["dir"], walls, scenary["chest"])
            if enemies["wait"] == True:
                for enemy in enemies["list"]:
                    #print(enemy)
                    enemy["x"],enemy["y"] = Enemy.move(enemy,player["x"],player["y"],walls)
            enemies["wait"] = not enemies["wait"]
        scenary["walls"], scenary["tp"] = Scenery.animation(animationtick,scenary)
        if player["equipement"]["delay"] >= equipements[player["equipement"]["list"][player["equipement"]["inhand"]]]["wait"] or player["equipement"]["list"][player["equipement"]["inhand"]] == "pistol":
            player["equipement"]["used"] = True
            i=0
            while i<len(enemies["list"]):
                match player["equipement"]["list"][player["equipement"]["inhand"]]:
                    case "sword":
                        hit = Player.sword.hitEnemy(player["x"],player["y"],player["dir"],enemies["list"][i]['x'],enemies["list"][i]['y'])
                        #print('Touché',hit,'player',player["x"],player["y"],player["dir"],'enemy',enemies[i]["x"],enemies[i]["y"])
                        if hit:
                            enemies["list"].pop(i)
                            player["score"]+=1
                        else:
                            i+=1
                    case "dsword":
                        hit = Player.dsword.hitEnemy(player["x"],player["y"],player["dir"],enemies["list"][i]['x'],enemies["list"][i]['y'])
                        #print('Touché',hit,'player',player["x"],player["y"],player["dir"],'enemy',enemies[i]["x"],enemies[i]["y"])
                        if hit:
                            enemies["list"].pop(i)
                            player["score"]+=1
                        else:
                            i+=1
                    case _:
                        i+=1
        else: player["equipement"]["used"] = False
        x=0
        if player["equipement"]["list"][player["equipement"]["inhand"]] == "pistol":
            if (pyxel.frame_count//60)%5==1 and tick == 0:
                player["equipement"]["specialvar"]["ammo"]+=1
                #print('Ammo now at',player["equipement"]["specialvar"]["ammo"])
            i=0
            while i<len(player["equipement"]["specialvar"]["listbullet"]):
                bullet = player["equipement"]["specialvar"]["listbullet"][i]
                if bullet['x']<8 or bullet['x']>121 or bullet['y']<8 or bullet['y']>121:
                    player["equipement"]["specialvar"]["listbullet"].pop(i)
                else:
                    match bullet["dir"]:
                        case "u":
                            bullet['y']-=1
                        case "d":
                            bullet['y']+=1
                        case "r":
                            bullet['x']+=1
                        case "l":
                            bullet['x']-=1
                    i+=1
        i = 0
        while i<len(enemies["list"]):
            #print(len(player["equipement"]['specialvar']['listbullet']))
            if player["equipement"]["list"][player["equipement"]["inhand"]] == "pistol":
                while x<len(player["equipement"]['specialvar']['listbullet']):
                    #print(player["equipement"]['specialvar']['listbullet'][x]['x'],player["equipement"]['specialvar']['listbullet'][x]['y'])
                    #print(enemies["list"][i]['x'],enemies["list"][i]['y'])
                    if Player.pistol.hitEnemy(player["equipement"]['specialvar']['listbullet'][x]['x'],player["equipement"]['specialvar']['listbullet'][x]['y'],enemies["list"][i]['x'],enemies["list"][i]['y']):
                        player["equipement"]['specialvar']['listbullet'].pop(x)
                        enemies["list"].pop(i)
                        player["score"]+=1
                        player["equipement"]["specialvar"]["ammo"]+=1
                        print("Enemy killed, score at",player["score"],"and Enemy nb at",len(enemies["list"]))
                    else: x+=1
            try:
                if Player.colidingEnemy(player["x"],player["y"],enemies["list"][i]["x"],enemies["list"][i]["y"]):
                    enemies["list"].pop(i)
                    player["life"]-=1
                    pyxel.play(3,5)
                    i-=1
                    
            except IndexError:
                pass
            i+=1
    else:
        if not scenary["endgame"]:
            scenary["endgame"]=True
            pyxel.stop(0)
            pyxel.play(0,4)
            time.sleep(1)
# =========================================================
# == DRAW
# =========================================================
def draw():
    """Draw everything (skipped if not enought time is given)"""

    # Clear
    
    pyxel.cls(0)
    
    
    ### UI
    pyxel.rect(0,128,128,9,1)
    pyxel.text(64-(2*len(str(zone))),16,str(zone-1),1)
    # Life
    pyxel.blt(0,129,0,0,35,16,7,0)
    if 0<=player["life"]<=4: pyxel.blt(0,129,0,0,42,4*player["life"],7,0)
    else: pyxel.blt(0,129,0,0,42,16,7,0)
    pyxel.text(3,130,str(player["life"]),2)
    # Ammo/Use of equipement
    pyxel.blt(15,129,0,0,35,16,7,0)
    # Delay before the reuse
    pyxel.blt(30,129,0,0,35,16,7,0)
    pyxel.blt(30,129,0,0,56,1+(15-(player["equipement"]["delay"]//2)),7,0)
    if player["equipement"]["list"][player["equipement"]["inhand"]]!="pistol":
        if not player["equipement"]["used"]:
            pyxel.blt(15,129,0,0,49,16,7,0)
    else:
        # Ammo countdown
        if player["equipement"]["specialvar"]["ammo"]<21:
            pyxel.blt(15,129,0,0,49,(player["equipement"]["specialvar"]["ammo"]//1.5),7,0)
        else:
            pyxel.blt(15,129,0,0,49,16,7,0)
        pyxel.text(18,130,str(player["equipement"]["specialvar"]["ammo"]),5)
    pyxel.text(97-(6*len(str(player["score"]))),130,str('Score : '+str(player["score"])),7)
    # Objects in inv
    xcords = 48
    objpos = {}
    for objects in player["equipement"]["list"]:
        match objects:
            case "sword":
                objpos["sword"]=xcords
                pyxel.blt(xcords,129,1,0,16,6,6,0)
            case "dsword":
                objpos["dsword"]=xcords
                pyxel.blt(xcords,129,1,16,16,6,6,0)
            case "pistol":
                objpos["pistol"]=xcords
                pyxel.blt(xcords,129,1,8,16,6,6,0)
        xcords+=9
    pyxel.rect(objpos[player["equipement"]["list"][player["equipement"]["inhand"]]],136,7,1,7)
    
    ### Walls
    match scenary["chest"]["state"]:
        case 1:
            pyxel.blt(scenary["chest"]["x"],scenary["chest"]["y"],0,0,27,8,8,0)
        case 2:
            pyxel.blt(scenary["chest"]["x"],scenary["chest"]["y"],0,8,27,8,8,0)
            if pyxel.frame_count<=scenary["chest"]["timegiven"]+config["fps"]*5:
                pyxel.text(52,52,scenary["chest"]["gift"],1)
    for y in range(len(walls)):
        for x in range(len(walls[y])):
            if walls[y][x] == 1:
                if scenary["chest"]!=False:
                    for x1 in [7,8]:
                        for y1 in [7,8]:
                            if walls[y1][x1]==1:
                                pass
                            else:
                                pyxel.blt(x*8, y*8, 0, scenary["walls"]*8, 11, 8, 8, 0)  
                else:
                    pyxel.blt(x*8, y*8, 0, scenary["walls"]*8, 11, 8, 8, 0)
            if walls[y][x] == 2:
                match scenary["tp"]:
                    case -1:
                        pyxel.blt(x*8, y*8, 0, 0, 19, 8, 8, 0)
                    case _:
                        pyxel.blt(x*8, y*8, 0, (scenary["tp"]+1)*8, 19, 8, 8, 0)
    ### Enemies
    for enemy in enemies["list"]:
        if enemy!=None:
            match enemy["dir"]:
                case "l":
                    pyxel.blt(enemy["x"],enemy["y"], 0, 24, 0, 6, 10, 0)
                case "r":
                    pyxel.blt(enemy["x"],enemy["y"], 0, 36, 0, 6, 10, 0)
    ### Player
    match player["dir"]:
        case "d":
            pyxel.blt(player["x"], player["y"], 0, 0, 0, 6, 10, 0)
        case "l":
            pyxel.blt(player["x"], player["y"], 0, 6, 0, 6, 10, 0)
        case "u":
            pyxel.blt(player["x"], player["y"], 0, 12, 0, 6, 10, 0)
        case "r":
            pyxel.blt(player["x"], player["y"], 0, 18, 0, 6, 10, 0)
    ### Player's equipement
    if player["equipement"]["used"]:
        match player["equipement"]["list"][player["equipement"]["inhand"]]:
            case "sword":
                match player["dir"]:
                    case "l":
                        pyxel.blt(player["x"]-5,player["y"]+6,1,0,0,5,2,0)
                    case "r":
                        pyxel.blt(player["x"]+6,player["y"]+6,1,0,3,5,2,0)
                    case "u":
                        pyxel.blt(player["x"]+2,player["y"]-3,1,3,6,2,3,0)
                    case "d":
                        pyxel.blt(player["x"]+2,player["y"]+8,1,0,6,2,5,0)
            case "dsword":
                match player["dir"]:
                    case "l":
                        pyxel.blt(player["x"]-5,player["y"]+6,1,0,0,5,2,0)
                        pyxel.blt(player["x"]+5,player["y"]+6,1,0,3,5,2,0) 
                    case "r":
                        pyxel.blt(player["x"]-4,player["y"]+6,1,0,0,5,2,0)
                        pyxel.blt(player["x"]+6,player["y"]+6,1,0,3,5,2,0)                     
                    case "u" | "d":
                        pyxel.blt(player["x"]+2,player["y"]-3,1,3,6,2,3,0)
                        pyxel.blt(player["x"]+2,player["y"]+8,1,0,6,2,5,0)
            case "pistol":
                match player["dir"]:
                    case "l":
                        pyxel.blt(player["x"]-5,player["y"]+4,1,18,0,6,5,0)
                    case "r":
                        pyxel.blt(player["x"]+5,player["y"]+4,1,24,0,6,5,0)
                    case "u":
                        pyxel.blt(player["x"]+2,player["y"]-4,1,21,5,2,4,0)
                    case "d":
                        pyxel.blt(player["x"]+2,player["y"]+7,1,18,5,3,5,0)
    elif player["equipement"]["list"][player["equipement"]["inhand"]] == "pistol":
        match player["dir"]:
            case "l":
                pyxel.blt(player["x"]-5,player["y"]+4,1,6,0,6,5,0)
            case "r":
                pyxel.blt(player["x"]+5,player["y"]+4,1,12,0,6,5,0)
            case "u":
                pyxel.blt(player["x"]+2,player["y"]-4,1,9,5,2,4,0)
            case "d":
                pyxel.blt(player["x"]+2,player["y"]+7,1,6,5,3,5,0)
    # Pistol Bullet
    if player["equipement"]["list"][player["equipement"]["inhand"]] == "pistol":
        for bullet in player["equipement"]["specialvar"]["listbullet"]:
            pyxel.pset(bullet['x'],bullet['y'],13)
    
    if scenary["endgame"]:
        pyxel.rect(16,32,96,33,1)
        pyxel.text(18,34,"Game Over !",7)
        pyxel.text(18,40,str("Your score is :"+str(player["score"])),7)

    
walls, zone = Mecanism.changeZone(zone)
pyxel.run(update, draw)