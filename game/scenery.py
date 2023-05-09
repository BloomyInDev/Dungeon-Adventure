animdir = 1
class Scenery:
    def changedir(scenary):
        global animdir
        if animdir == -1 and scenary["tp"] <= 0: animdir = 1
        elif animdir == 1 and scenary["tp"] >= 2: animdir = -1
    def animation(tick,scenary):
        if tick == 30:
            if scenary["walls"] == 1: walls_scenary = 0
            else: walls_scenary = 1
            Scenery.changedir(scenary)
            tp_scenary = scenary["tp"]+animdir
            return walls_scenary, tp_scenary
        elif tick == 15:
            walls_scenary = scenary["walls"]
            tp_scenary = scenary["tp"]+animdir
            return walls_scenary, tp_scenary
        else:
            walls_scenary = scenary["walls"]
            tp_scenary = scenary["tp"]
            return walls_scenary, tp_scenary
    def spawnchest():
        return {"x":60,"y":60,"state":1}