# -*- coding: utf-8 -*-

import random
import json
import shutil
import pandas as pd


from flask import Flask, request, jsonify
import os
from refacto_de_randomstory import *
from flask_cors import CORS

# create the Flask app
app = Flask(__name__)
CORS(app)

@app.route('/post_json', methods=['POST'])
def process_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json_data = request.json
        with open('dataJson.json','w') as f:
            json.dump(json_data, f)
            print("ok")
        return json_data
    else:
        return 'Content-Type not supported!'


@app.route('/query-example')

def query_example():
    import os
    os.path.abspath(os.getcwd())

    """# Gestion accès Json"""

    jsonFile = "dataJson.json"

    with open(jsonFile, 'r') as f:
        data = json.load(f)

    """# Party Faker pour les données aléatoires"""

    import random
    from faker import Faker
    fake = Faker('fr_FR')

    villes = []
    for i in range(1000):
        villes.append(fake.city())


    def contenuPersonnage(personnage):
        content =  data[personnage]
        nom = content["nom"]
        race = content["race"]
        top_3_attributs = sorted(content["attributs"], key=data["personnage1"]["attributs"].get, reverse=True)[:3]
        top_3_capacite = sorted(content["capacites"], key=data["personnage1"]["capacites"].get, reverse=True)[:3]
        # print(nom, top_3_attributs, top_3_capacite)
        return nom, top_3_attributs, top_3_capacite, race

    # get if personnage1 etc sont dans data
    listPossibilities = []
    TableauIfpersonnage = []
    def getExistPersonnage(dataJson):
        for nbr in range(1, 7):
            listPossibilities.append("personnage"+str(nbr))
            if(listPossibilities[nbr-1] in dataJson):
                TableauIfpersonnage.append(listPossibilities[nbr-1])
        return (len(TableauIfpersonnage))

    nbr_personnageInJson = getExistPersonnage(data)


    """# Tout mettre dans fonction"""

    def capaciteesPersonnage():
        capac = []
        for x in range(nbr_personnageInJson):
            personnages = "personnage"+ str(x+1)
            sort_attributs = sorted(data[personnages]["capacites"].items(), key=lambda x: x[1], reverse=True)
            result = []
            allPersonnageAttribut = []
            for i in sort_attributs:
                result.append(i[0])
            capac.append(result[:3])
            # print(result[:3])
        return capac

    def attributsPersonnage():
        attrib = []
        for x in range(nbr_personnageInJson):
            personnages = "personnage"+ str(x+1)
            sort_attributs = sorted(data[personnages]["attributs"].items(), key=lambda x: x[1], reverse=True)
            result = []
            allPersonnageAttribut = []
            for i in sort_attributs:
                result.append(i[0])
            attrib.append(result[:3])
            # print(result[:3])
        return attrib

    listPossibilities = []
    TableauIfpersonnage = []
    def getExistPersonnage(dataJson):
        for nbr in range(1, 7):
            listPossibilities.append("personnage"+str(nbr))
            # print(listPossibilities[nbr-1])
            if(listPossibilities[nbr-1] in dataJson):
                TableauIfpersonnage.append(listPossibilities[nbr-1])
        # print((TableauIfpersonnage))
        return (len(TableauIfpersonnage))

    # print(getExistPersonnage(data))
    nbr_personnageInJson = getExistPersonnage(data)
    # print(nbr_personnageInJson)

    chooseCapaciteeSentence = ["tandis que ses compétences sont plus orientées : ", "au lieu de ça sont génie pointe du côtée de : ", "alors que ses capacitées se situe vers : ", "cependant son art l'axe sur :"]
    chooseAttributsSentence = ["possède les attributs suivant : ", "a les qualité suivantes : ", "est pourvu de plusieurs aptitude : ", "détient de multiples facultées  : ", "bénéficie de moult dons : "]


    def PersonnageAndAttributsAndCapacityToStory():
        allAttributs_AllPersonnage = attributsPersonnage()
        allCapacity_AllPersonnage = capaciteesPersonnage()
        listPersonnage = []
        for x in range(nbr_personnageInJson):
            personnages = "personnage"+ str(x+1)
            if(x<nbr_personnageInJson-1):
                listPersonnage.extend([
                      contenuPersonnage(personnages)[0],
                      random.choice(chooseAttributsSentence),
                      allAttributs_AllPersonnage[x][0], ", ",
                      allAttributs_AllPersonnage[x][1], "et",
                      allAttributs_AllPersonnage[x][2], "; ",
                      random.choice(chooseCapaciteeSentence),
                      allCapacity_AllPersonnage[x][0], ", ",
                      allCapacity_AllPersonnage[x][1], "et",
                      allCapacity_AllPersonnage[x][2], ".",
                      ])
            if(x==nbr_personnageInJson-1):
                    listPersonnage.extend([
                              "\n",
                              contenuPersonnage(personnages)[0],
                              random.choice(chooseAttributsSentence),
                              allAttributs_AllPersonnage[x][0],", ",
                              allAttributs_AllPersonnage[x][1], "et",
                              allAttributs_AllPersonnage[x][2],"; ",
                              random.choice(chooseCapaciteeSentence),
                              allCapacity_AllPersonnage[x][0], ", ",
                              allCapacity_AllPersonnage[x][1], "et",
                              allCapacity_AllPersonnage[x][2], ".",
                              ])
        return listPersonnage

    # Get only name
    def addPersonnageToStory():
        listPersonnage = []
        for x in range(nbr_personnageInJson):
            personnages = "personnage"+ str(x+1)
            if(x<nbr_personnageInJson-1):
               listPersonnage.extend([
                      contenuPersonnage(personnages)[0],
                      "et",
                      ])
            if(x==nbr_personnageInJson-1):
                listPersonnage.extend([
                              contenuPersonnage(personnages)[0],
                              ])
        return listPersonnage

    addPersonnageToStory()

    def getRacePersonnage():
        raceList = []
        for x in range(nbr_personnageInJson):
            personnages = "personnage"+ str(x+1)
            if(x<nbr_personnageInJson-1):
                raceList.extend([
                      contenuPersonnage(personnages)[3],
                      "-",
                      ])
            if(x==nbr_personnageInJson-1):
                raceList.extend([
                              contenuPersonnage(personnages)[3],
                              ])
        return raceList

    getRacePersonnage()

    race = [
        "\n Ce n'est que le début de guerre entre les races ",
        "\n Ceci n'est qu'ébauche à l'hostilité entre ",
        "\n Tout cela donne naissance à une bataille entre ",
        "\n L'entrée en émeute ne fait que commencer entre les races ",
        "\n Tout cela donne origine à un combat ",
        ]

    import os
    from datetime import datetime
    import shutil

    def createStory(intro, storyBeginning, numberOfPlayers, Name, verb, listAttributsCapacityByperssonnage, raceName):
        id = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S").replace(":", "_").replace("/", "-"))
  
        city = random.choice(villes)
        text = intro + city + ". \n" + storyBeginning + numberOfPlayers + " personnages " + ' '.join(Name) + verb +  "\n" + ' '.join(listAttributsCapacityByperssonnage) + random.choice(race) +  ' '.join(raceName)

        return text  

    intro = [
         "Il était une fois, dans la ville de ", 
         "En ce temps-là en ", 
         "Il y a de cela, fort longtemps dans la cité de ",
         "Il y a bien longtemps au centre de ",
         "Dans une galaxie lointaine, très lointaine. Une petite ville au nom de ",
         "C’était il y a plus de cent ans au niveau d'une petite bourgade ",
         "Dans l’heureux temps des chevaliers, au sein du chateau de "
         ]

    storyBeginning = ["""\n Des meurtres sont commis chaque nuit
par certains habitants du village, devenus
Lycanthropes à cause d’un phénomène
mystérieux (peut-être l’effet de serre ?)…
Les Villageois doivent se ressaisir
pour éradiquer ce nouveau fléau venu
du fond des âges, avant que le hameau ne perde ses derniers habitants.\n C'est pour cela que nos """,
"""C'est l'histoire de royaumes inconnus, en guerre depuis des siècles. Les héros,au nombre de """,
"""Lorsqu'étaient grands les cieux, et noire la nuit, obscurcie par l'éclat des villes jamais endormies.
A la seule lueur de la danse des lucioles, des étoiles là-haut et de nos flammes folles.
Et que l'air s'emplissait du souffle des futaies, et des larmes et des voix du bois qui brûlait. Seuls les """, 
"""Nous chassions en ce temps tels les loups que nous sommes. Et chantions dans la nuit, car nous aurions pu être hommes. Vos """,
"""Le petit fils de Roges RABIT, avait orgaisé une soiréee feuille morte dans sa citadelle natale: le Blood Diamond.
Il y avait alors 7 petits gnomes qui travaillaient ensemble afin de construire une fresque. C'est à cet endroit même que la rencontre entre nos """, 
"""L'an de grâce 1420 a vu l'avenir des humains assombri par l'arrivée de créatures monstrueuses, répugnantes. 
Ces bêtes venus des enfers ne sortaient de leur que la nuit pour piller et tuer, sans raison, au hasard. 
Quelles chances peuvent avoir les humains contre une telle force. Les """,
]

    verb = [" virent la créature. \n", 
        " entrerent dans la cité. \n",
        " ensorcelèrent plusieurs villageois. \n",
        " maudirent le chef du village. \n",
        " apparurent comme par miracle. \n",
        " envoutèrent la population juste par leurs présence. \n"
        ]

    text = createStory(
        random.choice(intro),
        random.choice(storyBeginning),
        str(nbr_personnageInJson), 
        addPersonnageToStory(),
        random.choice(verb),
        PersonnageAndAttributsAndCapacityToStory(),
        getRacePersonnage(),
        )
    return text
if __name__ == '__main__':
                           # run app in debug mode on port 5000
    app.run(debug=True, host="127.0.0.1", port=5000)
    #10.5.0.20
