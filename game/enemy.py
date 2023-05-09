import pyxel, random, __main__
class Enemy:
    def spawn(walls):
        continuer = True
        while continuer:
            x = random.randint(24,128-24)
            y = random.randint(24,128-24)
            if walls[pyxel.ceil(y//8)][pyxel.ceil(x/8)] == 0 and walls[pyxel.floor(y//8)][pyxel.floor(x/8)] == 0:
                if x <= 64:
                    return {'x':x, 'y':y, 'dir':"l"}
                else:
                    return {'x':x, 'y':y, 'dir':"r"}
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
    def move(enemy,playerx,playery,walls):
        x = enemy["x"]
        y = enemy["y"]
        if playerx>x and not Enemy.isColiding(x+1,y,walls):
            x+=1
        if playerx<x and not Enemy.isColiding(x-1,y,walls):
            x-=1
        if playery>y and not Enemy.isColiding(x,y+1,walls):
            y+=1
        if playery<y and not Enemy.isColiding(x,y-1,walls):
            y-=1
        return x,y
            