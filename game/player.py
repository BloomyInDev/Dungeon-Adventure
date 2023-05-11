import pyxel, __main__
from mecanism import *
from scenery import *
deadzone = 15000
delaybetweenchanges = 10
class Player:
    class sword:
        def hitEnemy(playerx,playery,playerdir,enemyx,enemyy):
            match playerdir:
                case "d":
                    if playery<enemyy<playery+12 and playerx<enemyx+3<playerx+6:
                        return True
                case "l":
                    if playerx-5<enemyx+6<playerx and playery<enemyy+4<playery+9:
                        return True
                case "u":
                    if playery>enemyy+9>playery-3 and playerx<enemyx+3<playerx+6:
                        return True
                case "r":
                    if playerx+6<enemyx<playerx+11 and playery<enemyy+4<playery+9:
                        return True
            return False
    class dsword:
        def hitEnemy(playerx,playery,playerdir,enemyx,enemyy):
            match playerdir:
                case "d" | "u":
                    if playery-4<enemyy<playery+13 and playerx<enemyx+3<playerx+6:
                        return True
                case "l" | "r":
                    if (playerx-6<enemyx<playerx+11 or playerx-6<enemyx+6<playerx+11) and playery<enemyy+4<playery+9:
                        return True
            return False
    class pistol:
        def hitEnemy(bulletx,bullety,enemyx,enemyy):
            #print(enemyx<=bulletx<=enemyx+5, enemyy<=bullety<=enemyy+9)
            if enemyx<=bulletx<=enemyx+5 and enemyy<=bullety<=enemyy+9:
                return True
            return False
        def shootBullet(bullets,dir,playerx,playery):
            match dir:
                case 'u':
                    bullets.append({'x':playerx+3,'y':playery-4,'dir':dir})
                case 'd':
                    bullets.append({'x':playerx+3,'y':playery+10,'dir':dir})
                case 'r':
                    bullets.append({'x':playerx+10,'y':playery+5,'dir':dir})
                case 'l':
                    bullets.append({'x':playerx-5,'y':playery+5,'dir':dir})
    def isColiding(x,y,walls):
        try:
            if walls[(y+2)//8][x//8]==1:
                return True
            elif walls[(y+2)//8][(x+5)//8]==1:
                return True
            elif walls[(y+9)//8][x//8]==1:
                return True
            elif walls[(y+9)//8][(x+5)//8]==1:
                return True
        except IndexError:
            if walls[y//8][-1]==1: return True
            if walls[-1][x//8]==1: return True
            elif walls[-1][(x+5)//8]==1: return True
            else: return False
        return False
    def colidingChest(x,y,chest):
        if chest==1:
            if 60 <= x <= 68 and 60 <= y <= 68:
                return True
        return False
    def colidingEnemy(x,y,ex,ey):
        if x<=ex<=x+6 or x<=ex+6<=x+6:
            if y<=ey+10<=y+9 or y<=ey<=y+9:
                return True
        return False
    def isInTeleportZone(x,y):
        #print("TeleportZone",x,y)
        if x<=4: return True, 118, y
        elif x>=120: return True, 8, y
        elif y<=4: return True, x, 118
        elif y>=118: return True, x, 6
        else: return False, None, None      
    def lootChest(chestonscene):
        gift = Mecanism.chestLoot()
        chestscene = {'x':chestonscene['x'],'y':chestonscene['y'],'state':2,'gift':gift,'timegiven':pyxel.frame_count}
        match gift:
            case "pistol":
                if not("pistol" in __main__.player["equipement"]["list"]):
                    __main__.player["equipement"]["list"].append("pistol")
                    __main__.player["equipement"]["inhand"]=len(__main__.player["equipement"]["list"])-1
                else:
                    __main__.player["equipement"]["specialvar"]["ammo"]+=1
            case "dsword":
                if not("dsword" in __main__.player["equipement"]["list"]):
                    __main__.player["equipement"]["list"].append("dsword")
                    __main__.player["equipement"]["inhand"]=len(__main__.player["equipement"]["list"])-1
                else:
                    Player.lootChest(chestscene)
            case "health":
                __main__.player["life"]+=1

        return chestscene
    def move(x, y, equipementbefore, dir, walls, chestscene):
        x, y = x, y
        #Player's movement
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) or pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTX)>deadzone:
            if (x < 128) and not Player.isColiding(x+1,y, walls):
                x = x + 1
                dir = "r"
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT) or pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTX)<-deadzone:
            if (x > 0) and not Player.isColiding(x-1,y, walls):
                x = x - 1
                dir = "l"
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN) or pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTY)>deadzone:
            if (y < 128) and not Player.isColiding(x,y+1, walls):
                y = y + 1
                dir = "d"
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP) or pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTY)<-deadzone:
            if (y > 0) and not Player.isColiding(x,y-1, walls):
                y = y - 1
                dir = "u"
        # Player's teleporter
        if Player.isInTeleportZone(x,y)[0]:
            __main__.changeTheZone()
            _,x,y = Player.isInTeleportZone(x,y)
        # Player's equipement change
        if pyxel.btnv(pyxel.MOUSE_WHEEL_Y):
            #print(pyxel.mouse_wheel)
            if pyxel.mouse_wheel>0:
                if len(__main__.player["equipement"]["list"])-1==__main__.player["equipement"]["inhand"]:
                    __main__.player["equipement"]["inhand"]=0
                else:
                    __main__.player["equipement"]["inhand"]+=1
            else:
                if __main__.player["equipement"]["inhand"]==0:
                    __main__.player["equipement"]["inhand"]=len(__main__.player["equipement"]["list"])-1
                else:
                    __main__.player["equipement"]["inhand"]-=1
            #print(__main__.player["equipement"]["list"][__main__.player["equipement"]["inhand"]])
        if (pyxel.btn(pyxel.GAMEPAD1_BUTTON_LEFTSHOULDER) or pyxel.btn(pyxel.KEY_E) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_X)) and pyxel.frame_count-__main__.lastestchangeitem>delaybetweenchanges:
            __main__.lastestchangeitem = pyxel.frame_count
            if __main__.player["equipement"]["inhand"]==0:
                __main__.player["equipement"]["inhand"]=len(__main__.player["equipement"]["list"])-1
            else:
                __main__.player["equipement"]["inhand"]-=1
            #print(__main__.player["equipement"]["list"][__main__.player["equipement"]["inhand"]])
        if (pyxel.btn(pyxel.GAMEPAD1_BUTTON_RIGHTSHOULDER) or pyxel.btn(pyxel.KEY_R) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_Y)) and pyxel.frame_count-__main__.lastestchangeitem>delaybetweenchanges:
            __main__.lastestchangeitem = pyxel.frame_count
            if len(__main__.player["equipement"]["list"])-1==__main__.player["equipement"]["inhand"]:
                __main__.player["equipement"]["inhand"]=0
            else:
                __main__.player["equipement"]["inhand"]+=1
            #print(__main__.player["equipement"]["list"][__main__.player["equipement"]["inhand"]])
        # Player's sword
        if (pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnv(pyxel.GAMEPAD1_AXIS_TRIGGERRIGHT)>deadzone) and Player.colidingChest(x,y,chestscene['state']):
            chestscene = Player.lootChest(chestscene)
            equipement = 0
        elif (pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnv(pyxel.GAMEPAD1_AXIS_TRIGGERRIGHT)>deadzone) and equipementbefore == 0:
            equipement = __main__.equipements[__main__.player["equipement"]["list"][__main__.player["equipement"]["inhand"]]]['delay']
            if __main__.player["equipement"]["list"][__main__.player["equipement"]["inhand"]]=="pistol":
                if __main__.player["equipement"]["specialvar"]["ammo"]>0:
                    Player.pistol.shootBullet(__main__.player["equipement"]["specialvar"]["listbullet"],dir,x,y)
                    __main__.player["equipement"]["specialvar"]["ammo"]-=1
                    pyxel.play(3,2)
            else:
                pass
        elif equipementbefore !=0 : equipement = equipementbefore-1
        else: equipement = 0

        return x, y, equipement, dir, chestscene
