#!/usr/bin/env python
# @Author  : pengyun

from pweb.server.pweb import WSGIApplication, Render, ctx
from pweb.server.units import jsonify
import ants
import utils
import state
import threading
import importlib
from time import sleep
from ucb import *
# from json import dumps as jsonify

app = WSGIApplication()

app.config["secret_key"] = 'secret'
render = Render('templates').render_template


VERSION = 1.2
ASSETS_DIR = "static/assets/"
INSECT_DIR = "insects/"
STRATEGY_SECONDS = 3
INSECT_FILES = {
    'Worker': ASSETS_DIR + INSECT_DIR + "ant_harvester.gif",
    'Thrower': ASSETS_DIR + INSECT_DIR + "ant_thrower.gif",
    'Long': ASSETS_DIR + INSECT_DIR + "ant_longthrower.gif",
    'Short': ASSETS_DIR + INSECT_DIR + "ant_shortthrower.gif",
    'Harvester': ASSETS_DIR + INSECT_DIR + "ant_harvester.gif",
    'Fire': ASSETS_DIR + INSECT_DIR + "ant_fire.gif",
    'Bodyguard': ASSETS_DIR + INSECT_DIR + "ant_bodyguard.gif",
    'Hungry': ASSETS_DIR + INSECT_DIR + "ant_hungry.gif",
    'Slow': ASSETS_DIR + INSECT_DIR + "ant_slow.gif",
    'Stun': ASSETS_DIR + INSECT_DIR + "ant_stun.gif",
    'Ninja': ASSETS_DIR + INSECT_DIR + "ant_ninja.gif",
    'Wall': ASSETS_DIR + INSECT_DIR + "ant_wall.gif",
    'Scuba': ASSETS_DIR + INSECT_DIR + "ant_scuba.gif",
    'Queen': ASSETS_DIR + INSECT_DIR + "ant_queen.gif",
    'Tank': ASSETS_DIR + INSECT_DIR + "ant_tank.gif",
    'Bee': ASSETS_DIR + INSECT_DIR + "bee.gif",
    'Remover': ASSETS_DIR + INSECT_DIR + "remove.png",
}


class GUI:
    """Browser based GUI that communicates with Python game engine"""

    def __init__(self):
        self.active = True
        self.cleanState()

    def cleanState(self):
        self.initialized = False
        self.state = state.State()
        self.gameOver = False
        self.colony = None
        self.currentBeeId = 0
        self.currentInsectId = 0
        self.insects = []
        self.bees = []
        self.deadbees = []
        self.deadinsects = []
        self.insectToId = {}
        self.beeToId = {}
        self.beeLocations = {}

    def makeHooks(self):
        ants.Insect.reduce_armor = utils.class_method_wrapper(ants.Insect.reduce_armor, post=dead_insects)
        ants.AntColony.remove_ant = utils.class_method_wrapper(ants.AntColony.remove_ant, post=removed_ant)

    def newGameThread(self):
        print("Trying to start new game")
        self.cleanState()  # resets GUI state
        importlib.reload(ants)  # resets ants, e.g. with newly implemented Ants
        self.makeHooks()

        self.winner = ants.start_with_strategy(gui.args, gui.strategy)
        self.gameOver = True
        self.saveState("winner", self.winner)
        self.saveState("gameOver", self.gameOver)
        # self.killGUI()


    def killGUI(self):
        self.active = False

    def startGame(self, data=None):
        threading.Thread(target=self.newGameThread).start()
        print("Game started")

    def exit(self, data=None):
        self.active = False

    def initialize_colony_graphics(self, colony):
        self.colony = colony
        self.ant_type_selected = -1
        self.saveState("strategyTime", STRATEGY_SECONDS)
        self.saveState("food", self.colony.food)
        self.ant_types = self.get_ant_types()
        self._init_places(colony)
        self.saveState("places", self.places)
        # Finally log that we are initialized
        self.initialized = True

    def get_ant_types(self, noSave=False):
        ant_types = [];
        for name, ant_type in self.colony.ant_types.items():
            ant_types.append({"name": name, "cost": ant_type.food_cost, "img": self.get_insect_img_file(name)})

        # Sort by cost
        ant_types.sort(key=lambda item: item["cost"])

        if not noSave:
            self.saveState("ant_types", ant_types)
        return ant_types

    def get_insect_img_file(self, name):
        return INSECT_FILES[name]

    def getState(self, data=None):
        """Get our message from JSON"""
        return self.state.getState()

    def saveState(self, key, val):
        """Saves our game object to JSON file"""
        self.state.updateState(key, val)

    def strategy(self, colony):
        """The strategy function is called by ants.AntColony each turn"""
        # Have we initialized our graphics yet?
        if not self.initialized:
            # No, so do that now
            self.initialize_colony_graphics(colony)
        elapsed = 0  # Physical time elapsed this turn
        self.saveState("time", int(elapsed))
        while elapsed < STRATEGY_SECONDS:
            self.saveState("time", colony.time)
            self._update_control_panel(colony)
            sleep(0.25)
            elapsed += 0.25

    def get_place_row(self, name):
        return name.split("_")[1]

    def get_place_column(self, name):
        return name.split("_")[2]

    def _init_places(self, colony):
        """Calculate all of our place data"""
        self.places = {};
        self.images = {'AntQueen': dict()}
        rows = 0
        cols = 0
        for name, place in colony.places.items():
            if place.name == 'Hive':
                continue
            pCol = self.get_place_column(name)
            pRow = self.get_place_row(name)
            if place.exit.name == 'AntQueen':
                rows += 1
            if not pRow in self.places:
                self.places[pRow] = {}
            self.places[pRow][pCol] = {"name": name, "type": "tunnel", "water": 0, "insects": {}}
            if "water" in name:
                self.places[pRow][pCol]["water"] = 1
            self.images[name] = dict()
        # Add the Hive
        self.places[colony.hive.name] = {"name": name, "type": "hive", "water": 0, "insects": {}}
        self.places[colony.hive.name]["insects"] = []
        for bee in colony.hive.bees:
            self.places[colony.hive.name]["insects"].append({"id": self.currentBeeId, "type": "bee"})
            self.beeToId[bee] = self.currentBeeId
            self.currentBeeId += 1
        self.saveState("rows", rows)
        self.saveState("places", self.places);

    def update_food(self):
        self.saveState("food", self.colony.food)

    def _update_control_panel(self, colony):
        """Reflect the game state in the play area."""
        self.update_food()
        old_insects = self.insects[:]
        old_bees = self.bees[:]
        self.bees, self.insects = [], []
        for name, place in colony.places.items():
            if place.name == 'Hive':
                continue
            pCol = self.get_place_column(name)
            pRow = self.get_place_row(name)
            if place.ant is not None:
                if self.insectToId[place.ant] not in self.insects:
                    # Add this ant to our internal list of insects
                    self.insects.append(self.insectToId[place.ant])
                # Ok there is an ant that needs to be drawn here
                self.places[pRow][pCol]["insects"] = {
                    "id": self.insectToId[place.ant],
                    "type": place.ant.name,
                    "img": self.get_insect_img_file(place.ant.name)
                }
                # Check if it's a container ant
                if hasattr(place.ant, "container"):
                    self.places[pRow][pCol]["insects"]["container"] = place.ant.container
                    if place.ant.container and place.ant.ant:
                        self.places[pRow][pCol]["insects"]["contains"] = {
                            "type": place.ant.ant.name,
                            "img": self.get_insect_img_file(place.ant.ant.name)
                        }
            else:
                self.places[pRow][pCol]["insects"] = {}
            # Loop through our bees
            for bee in place.bees:
                self.beeLocations[self.beeToId[bee]] = name
                if self.beeToId[bee] not in self.bees:
                    self.bees.append(self.beeToId[bee])
        # Save our new bee locations to our game state
        self.saveState("beeLocations", self.beeLocations)

    def deployAnt(self, data):
        # Check to see if the ant is a remover. If so we need to remove the ant in pname
        pname, ant = data["pname"], data["ant"]
        if ant == "Remover":
            existing_ant = self.colony.places[pname].ant
            if existing_ant is not None:
                print("colony.remove_ant('{0}')".format(pname))
                self.colony.remove_ant(pname)
            return
        insect = None
        try:
            print("colony.deploy_ant('{0}', '{1}')".format(pname, ant))
            insect = self.colony.deploy_ant(pname, ant);
        except Exception as e:
            print(e)
            return {"error": str(e)}
        if not insect:
            return {"error": "Unable to deploy ant"}
        id = self.currentInsectId
        self.insects.append(id)
        self.insectToId[insect] = id
        self.currentInsectId += 1
        self._update_control_panel(self.colony);
        return {"success": 1, "id": id}


@app.route('/')
def index():
    return render('gui.html')


@app.route('/ajax/fetch/state', methods=['GET', 'POST'])
def states():
    return jsonify(gui.getState())


@app.route('/ajax/start/game', methods=['GET', 'POST'])
def start():
    gui.startGame()
    return jsonify(gui.startGame())


@app.route('/ajax/exit', methods=['GET', 'POST'])
def exit():
    gui.exit()
    return "Exit"


@app.route('/ajax/deploy/ant', methods=['GET', 'POST'])
def ant():
    delopy = {
        'pname': ctx.request.form['pname'],
        'ant': ctx.request.form['ant'],
    }
    return jsonify(gui.deployAnt(delopy))


def dead_insects(self, rv, *args):
    if self.armor <= 0 and self:
        print('{0} ran out of armor and expired'.format(self))
        if self in gui.insectToId:
            gui.deadinsects.append(gui.insectToId[self])
            gui.saveState("deadinsects", gui.deadinsects)
        elif self in gui.beeToId:
            gui.deadbees.append(gui.beeToId[self])
            gui.saveState("deadbees", gui.deadbees)


def removed_ant(self, rv, *args):
    r = gui.get_place_row(args[0])
    c = gui.get_place_column(args[0])
    if c in gui.places[r]:
        if "id" in gui.places[r][c]["insects"]:
            gui.deadinsects.append(gui.places[r][c]["insects"]["id"])
            gui.saveState("deadinsects", gui.deadinsects)


@main
def run(*args):
    global gui
    gui = GUI()
    gui.args = args

    def start_http():
        while gui.active:
            app.run(debug=True)
        print("Web server terminated")

    start_http()