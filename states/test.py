
def loadMap(name):
    with open(name, 'rb') as f:
        lines = f.readlines()
    
    print(lines)

loadMap("../assets/map/map.txt")