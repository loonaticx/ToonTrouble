import json
import os

settingsDefault = '''{
    "settings":
    {
        "want-ambient-occlusion": false,
        "want-bloom-enabled": false,
        "want-fog-enabled": true,
        "want-xray-mode": false,
        "want-invert-mode": false,
        "player-dna": 3
    }
}
'''

def generateSettings():
    if not os.path.exists('config/'):
        os.mkdir('config/')

    if not os.path.isfile('config/settings.json'):
        with open('config/settings.json', 'w') as data:
            data.write(settingsDefault)
            data.close()

def loadSettings():
    with open('config/settings.json') as data:
        return json.load(data)

#print (settings["settings"][0]['want-gay-ass-filters'])
#rint (settings["settings"][0]['want-ambient-occlusion'])
#print (settings["settings"][1]['value'])

#print(settings["settings"])



colorsJsonDefaultValues = '''{
    "colors":
    [
        {
            "name": "African Violet",
            "value": [0.70, 0.52, 0.75, 1.0]
        },
        {
            "name": "Lime Green",
            "value": [0.50, 1.0, 0.00, 1.0]
        }
    ]
}
'''



def generateColors():
    if not os.path.exists('config/'):
        os.mkdir('config/')

    if not os.path.isfile('config/colors.json'):
        with open('config/colors.json', 'w') as data:
            data.write(colorsJsonDefaultValues)
            data.close()

    with open('config/colors.json') as data:
        colors = json.load(data)

#generateColors()




