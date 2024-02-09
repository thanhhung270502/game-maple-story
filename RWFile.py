import os
import json

class HandleFile():
    def saveFile(dir, fileName, data):
        with open(os.path.join(dir, fileName), 'w') as file:
            json.dump(data, file)

    def loadFile(dir, fileName):
        try:
            with open(os.path.join(dir, fileName), 'r') as file:
                score = json.load(file)
        except FileNotFoundError:
            return 0
        return score 