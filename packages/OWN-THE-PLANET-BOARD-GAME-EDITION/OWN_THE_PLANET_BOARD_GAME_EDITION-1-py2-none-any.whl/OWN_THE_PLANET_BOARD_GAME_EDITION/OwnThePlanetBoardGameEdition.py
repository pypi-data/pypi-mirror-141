"""
This file contains code for the game "Own The Planet - Board Game Edition".
Author: DigitalCreativeApkDev
"""

# Game version: 1


# Importing necessary libraries
import sys
import uuid
import pickle
import copy
import random
import os
from functools import reduce

import mpmath
from mpmath import mp, mpf

mp.pretty = True


# Creating static functions to be used throughout the game.


def is_number(string: str) -> bool:
    try:
        mpf(string)
        return True
    except ValueError:
        return False


def triangular(n: int) -> int:
    return int(n * (n - 1) / 2)


def mpf_sum_of_list(a_list: list) -> mpf:
    return mpf(str(sum(mpf(str(elem)) for elem in a_list if is_number(str(elem)))))


def mpf_product_of_list(a_list: list) -> mpf:
    return mpf(reduce(lambda x, y: mpf(x) * mpf(y) if is_number(x) and
                                                      is_number(y) else mpf(x) if is_number(x) and not is_number(
        y) else mpf(y) if is_number(y) and not is_number(x) else 1, a_list, 1))


def load_game_data(file_name):
    # type: (str) -> Game
    return pickle.load(open(file_name, "rb"))


def save_game_data(game_data, file_name):
    # type: (Game, str) -> None
    pickle.dump(game_data, open(file_name, "wb"))


def clear():
    # type: () -> None
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows System
    else:
        os.system('clear')  # For Linux System


# Creating necessary classes for the game.


class Dice:
    """
    This class contains attributes of the dice in the game.
    """

    def __init__(self):
        # type: () -> None
        self.value: int = random.randint(1, 20)

    def __str__(self):
        # type: () -> str
        return "Value: " + str(self.value) + "\n"

    def clone(self):
        # type: () -> Dice
        return copy.deepcopy(self)


class Board:
    """
    This class contains attributes of the board in this game.
    """

    def __init__(self, tiles):
        # type: (list) -> None
        self.__tiles: list = tiles

    def __str__(self):
        # type: () -> str
        res: str = "Current board representation:\n\n"
        for tile in self.__tiles:
            res += str(tile) + "\n"

        return res

    def get_tiles(self):
        # type: () -> list
        return self.__tiles

    def clone(self):
        # type: () -> Board
        return copy.deepcopy(self)


class Tile:
    """
    This class contains attributes of a tile on the board.
    """

    TILE_NUMBER: int = 0

    def __init__(self, name, description):
        # type: (str, str) -> None
        Tile.TILE_NUMBER += 1
        self.name: str = name
        self.description: str = description

    def __str__(self):
        # type: () -> str
        res: str = ""  # initial value
        res += "Name: " + str(self.name) + "\n"
        res += "Description: " + str(self.description) + "\n"
        return res

    def clone(self):
        # type: () -> Tile
        return copy.deepcopy(self)


class StartTile(Tile):
    """
    This class contains attributes of the start tile where the player can gain awards by passing or landing on it.
    """

    def __init__(self):
        # type: () -> None
        Tile.__init__(self, "START TILE", "A tile where the player can gain awards by passing or landing on it.")


class EmptySpace(Tile):
    """
    This class contains attributes of an empty space where nothing happens if the player lands on it.
    """

    def __init__(self):
        # type: () -> None
        Tile.__init__(self, "EMPTY SPACE", "A tile where nothing happens if the player lands on it.")


class Place(Tile):
    """
    This class contains attributes of a place the player can purchase and upgrade when landing on it.
    """

    def __init__(self, name, description, gold_cost, gold_per_turn, exp_per_turn):
        # type: (str, str, mpf, mpf, mpf) -> None
        Tile.__init__(self, name, description)
        self.level: int = 1
        self.gold_cost: mpf = gold_cost
        self.gold_per_turn: mpf = gold_per_turn
        self.exp_per_turn: mpf = exp_per_turn
        self.owner: Player or None = None  # initial value

    def __str__(self):
        # type: () -> str
        res: str = Tile.__str__(self)  # initial value
        res += "Level: " + str(self.level) + "\n"
        res += "Gold Cost: " + str(self.gold_cost) + "\n"
        res += "Gold Per Turn: " + str(self.gold_per_turn) + "\n"
        res += "EXP Per Turn: " + str(self.exp_per_turn) + "\n"
        res += "Owner: "
        if self.owner is None:
            res += "None\n"
        else:
            res += str(self.owner.name) + "\n"
        return res

    def level_up(self):
        # type: () -> None
        self.level += 1
        self.gold_cost *= mpf("10") ** triangular(self.level)
        self.gold_per_turn *= mpf("10") ** (triangular(self.level) - 1)
        self.exp_per_turn *= mpf("10") ** (triangular(self.level) - 1)


class RandomRewardTile(Tile):
    """
    This class contains attributes of a tile where the player can gain random rewards.
    """

    def __init__(self):
        # type: () -> None
        Tile.__init__(self, "RANDOM REWARD TILE", "A tile granting random rewards to the player landing on it.")


class QuizTile(Tile):
    """
    This class contains attributes of a quiz tile where the player can answer quiz questions to gain rewards.
    """

    def __init__(self):
        # type: () -> None
        Tile.__init__(self, "QUIZ TILE", "A tile where the player can gain rewards by answering quiz "
                                         "questions correctly.")


class UpgradeShop(Tile):
    """
    This class contains attributes of an upgrade shop where the player can buy upgrades.
    """

    def __init__(self, upgrades_sold):
        # type: (list) -> None
        Tile.__init__(self, "UPGRADE SHOP", "A tile where the player can buy upgrades.")
        self.__upgrades_sold: list = upgrades_sold

    def get_upgrades_sold(self):
        # type: () -> list
        return self.__upgrades_sold

    def __str__(self):
        # type: () -> str
        res: str = str(self.name) + "\n"
        res += "Below is a list of upgrades sold:\n"
        for upgrade in self.__upgrades_sold:
            res += str(upgrade) + "\n"

        return res


class QuizQuestion:
    """
    This class contains attributes of a quiz question the player can answer in quiz zones.
    """

    QUESTION_NUMBER: int = 0

    def __init__(self, question, choices, correct_answer, correct_answer_gold_reward, correct_answer_exp_reward):
        # type: (str, list, str, mpf, mpf) -> None
        QuizQuestion.QUESTION_NUMBER += 1
        self.question: str = question
        self.choices: list = choices
        self.correct_answer: str = correct_answer
        self.correct_answer_gold_reward: mpf = correct_answer_gold_reward
        self.correct_answer_exp_reward: mpf = correct_answer_exp_reward

    def __str__(self):
        # type: () -> str
        res: str = ""  # initial value
        res += str(self.QUESTION_NUMBER) + ". " + str(self.question) + "\n"
        for choice in self.choices:
            res += str(choice) + "\n"

        res += "Correct Answer Gold Reward: " + str(self.correct_answer_gold_reward) + "\n"
        res += "Correct Answer EXP Reward: " + str(self.correct_answer_exp_reward) + "\n"
        return res

    def clone(self):
        # type: () -> QuizQuestion
        return copy.deepcopy(self)


class RandomReward:
    """
    This class contains attributes of an obtainable random reward at random reward tiles.
    """

    def __init__(self):
        # type: () -> None
        self.reward_gold: mpf = mpf("1e" + str(random.randint(1000, 100000)))
        self.reward_exp: mpf = mpf("1e" + str(random.randint(1000, 100000)))

    def __str__(self):
        # type: () -> str
        res: str = ""  # initial value
        res += "Reward Gold: " + str(self.reward_gold) + "\n"
        res += "Reward EXP: " + str(self.reward_exp) + "\n"
        return res

    def clone(self):
        # type: () -> RandomReward
        return copy.deepcopy(self)


class Upgrade:
    """
    This class contains attributes of an upgrade the player can purchase to improve the amount
    of gold and EXP earned per turn.
    """

    def __init__(self, name, description, gold_cost, gold_gain_multiplier, exp_gain_multiplier):
        # type: (str, str, mpf, mpf, mpf) -> None
        self.name: str = name
        self.description: str = description
        self.gold_cost: mpf = gold_cost
        self.gold_gain_multiplier: mpf = gold_gain_multiplier
        self.exp_gain_multiplier: mpf = exp_gain_multiplier

    def __str__(self):
        # type: () -> str
        res: str = ""  # initial value
        res += "Name: " + str(self.name) + "\n"
        res += "Description: " + str(self.description) + "\n"
        res += "Gold Cost: " + str(self.gold_cost) + "\n"
        res += "Gold Gain Multiplier: " + str(self.gold_gain_multiplier) + "\n"
        res += "EXP Gain Multiplier: " + str(self.exp_gain_multiplier) + "\n"
        return res

    def clone(self):
        # type: () -> Upgrade
        return copy.deepcopy(self)


class Player:
    """
    This class contains attributes of the player in this game.
    """

    def __init__(self, name):
        # type: (str) -> None
        self.player_id: str = str(uuid.uuid1())
        self.name: str = name
        self.level: int = 1
        self.location: int = 0  # initial value
        self.gold: mpf = mpf("1e6")
        self.exp: mpf = mpf("0")
        self.required_exp: mpf = mpf("1e6")
        self.__owned_list: list = []  # initial value
        self.__upgrade_list: list = []  # initial value

    def __str__(self):
        # type: () -> str
        res: str = ""  # initial value
        res += "Player ID: " + str(self.player_id) + "\n"
        res += "Name: " + str(self.name) + "\n"
        res += "Level: " + str(self.level) + "\n"
        res += "Location: " + str(self.location) + "\n"
        res += "Gold: " + str(self.gold) + "\n"
        res += "EXP: " + str(self.exp) + "\n"
        res += "Required EXP: " + str(self.required_exp) + "\n"
        res += "Below is a list of places owned by the player:\n"
        for place in self.__owned_list:
            res += str(place) + "\n"

        res += "Below is a list of upgrades owned by the player:\n"
        for upgrade in self.__upgrade_list:
            res += str(upgrade) + "\n"

        return res

    def level_up(self):
        # type: () -> None
        while self.exp >= self.required_exp:
            self.level += 1
            self.required_exp *= mpf("10") ** triangular(self.level)

    def roll_dice(self, game):
        # type: (Game) -> None
        self.location += Dice().value
        if self.location >= len(game.board.get_tiles()):
            self.gold += game.start_bonus
            self.location -= len(game.board.get_tiles())

    def get_gold_per_turn(self):
        # type: () -> mpf
        return mpf_sum_of_list([place.gold_per_turn for place in self.__owned_list]) * \
               mpf_product_of_list([upgrade.gold_gain_multiplier for upgrade in self.__upgrade_list])

    def get_exp_per_turn(self):
        # type: () -> mpf
        return mpf_sum_of_list([place.exp_per_turn for place in self.__owned_list]) * \
               mpf_product_of_list([upgrade.exp_gain_multiplier for upgrade in self.__upgrade_list])

    def get_owned_list(self):
        # type: () -> list
        return self.__owned_list

    def buy_place(self, place):
        # type: (Place) -> bool
        if self.gold >= place.gold_cost:
            self.gold -= place.gold_cost
            self.__owned_list.append(place)
            place.owner = self
            return True
        return False

    def upgrade_place(self, place):
        # type: (Place) -> bool
        if place in self.__owned_list:
            if self.gold >= place.gold_cost:
                self.gold -= place.gold_cost
                place.level_up()
                return True
            return False
        return False

    def acquire_place(self, place, owner):
        # type: (Place, Player) -> bool
        if place in owner.get_owned_list() and place not in self.get_owned_list():
            if self.gold >= place.gold_cost:
                self.gold -= place.gold_cost
                owner.gold += place.gold_cost
                place.level_up()
                self.__owned_list.append(place)
                owner.__owned_list.append(place)
                place.owner = self
                return True
            return False
        return False

    def get_upgrade_list(self):
        # type: () -> list
        return self.__upgrade_list

    def buy_upgrade(self, upgrade):
        # type: (Upgrade) -> bool
        if self.gold >= upgrade.gold_cost:
            self.gold -= upgrade.gold_cost
            self.__upgrade_list.append(upgrade)
            return True
        return False

    def get_random_reward(self, random_reward):
        # type: (RandomReward) -> None
        self.gold += random_reward.reward_gold
        self.exp += random_reward.reward_exp
        self.level_up()

    def answer_quiz_question(self, quiz_question, input_answer):
        # type: (QuizQuestion, str) -> bool
        if input_answer == quiz_question.correct_answer:
            self.gold += quiz_question.correct_answer_gold_reward
            self.exp += quiz_question.correct_answer_exp_reward
            self.level_up()
            return True
        return False

    def gain_turn_reward(self):
        # type: () -> None
        self.gold += self.get_gold_per_turn()
        self.exp += self.get_exp_per_turn()
        self.level_up()

    def clone(self):
        # type: () -> Player
        return copy.deepcopy(self)


class CPU(Player):
    """
    This class contains attributes of a CPU controlled player as the player's opponent.
    """

    def __init__(self):
        # type: () -> None
        Player.__init__(self, "CPU")


class Game:
    """
    This class contains attributes of saved game data.
    """

    def __init__(self, player, cpu, board, quiz_questions):
        # type: (Player, CPU, Board, list) -> None
        self.turn: int = 0
        self.start_bonus: mpf = mpf("2e5")
        self.player: Player = player
        self.cpu: CPU = cpu
        self.board: Board = board
        self.__quiz_questions: list = quiz_questions

    def __str__(self):
        # type: () -> str
        res: str = ""  # initial value
        res += "Start Bonus: " + str(self.start_bonus) + "\n"
        res += "Player's stats in the game: " + str(self.player) + "\n"
        res += "CPU's stats in the game: " + str(self.cpu) + "\n"
        return res

    def get_quiz_questions(self):
        # type: () -> list
        return self.__quiz_questions

    def clone(self):
        # type: () -> Game
        return copy.deepcopy(self)


# Creating main function used to run the game.


def main() -> int:
    """
    This main function is used to run the game.
    :return: an integer
    """

    print("Welcome to 'Own The Planet - Board Game Edition' by 'DigitalCreativeApkDev'.")
    print("This game is an offline board game where the player and CPU compete to be the richest in the planet.")

    # Initialising function level variables to be used in the game.
    # 1. List of upgrades sold in the upgrade shop
    upgrades_sold: list = [
        Upgrade("GOLD UPGRADE #1", "Gold upgrade level 1.", mpf("1e10"), mpf("5"), mpf("1")),
        Upgrade("GOLD UPGRADE #2", "Gold upgrade level 2.", mpf("1e20"), mpf("10"), mpf("1")),
        Upgrade("GOLD UPGRADE #3", "Gold upgrade level 3.", mpf("1e40"), mpf("20"), mpf("1")),
        Upgrade("GOLD UPGRADE #4", "Gold upgrade level 4.", mpf("1e80"), mpf("40"), mpf("1")),
        Upgrade("GOLD UPGRADE #5", "Gold upgrade level 5.", mpf("1e160"), mpf("80"), mpf("1")),
        Upgrade("GOLD UPGRADE #6", "Gold upgrade level 6.", mpf("1e320"), mpf("160"), mpf("1")),
        Upgrade("GOLD UPGRADE #7", "Gold upgrade level 7.", mpf("1e640"), mpf("320"), mpf("1")),
        Upgrade("GOLD UPGRADE #8", "Gold upgrade level 8.", mpf("1e1280"), mpf("640"), mpf("1")),
        Upgrade("GOLD UPGRADE #9", "Gold upgrade level 9.", mpf("1e2560"), mpf("1280"), mpf("1")),
        Upgrade("GOLD UPGRADE #10", "Gold upgrade level 10.", mpf("1e5120"), mpf("2560"), mpf("1")),
        Upgrade("EXP UPGRADE #1", "EXP upgrade level 1.", mpf("1e10"), mpf("1"), mpf("5")),
        Upgrade("EXP UPGRADE #2", "EXP upgrade level 2.", mpf("1e20"), mpf("1"), mpf("10")),
        Upgrade("EXP UPGRADE #3", "EXP upgrade level 3.", mpf("1e40"), mpf("1"), mpf("20")),
        Upgrade("EXP UPGRADE #4", "EXP upgrade level 4.", mpf("1e80"), mpf("1"), mpf("40")),
        Upgrade("EXP UPGRADE #5", "EXP upgrade level 5.", mpf("1e160"), mpf("1"), mpf("80")),
        Upgrade("EXP UPGRADE #6", "EXP upgrade level 6.", mpf("1e320"), mpf("1"), mpf("160")),
        Upgrade("EXP UPGRADE #7", "EXP upgrade level 7.", mpf("1e640"), mpf("1"), mpf("320")),
        Upgrade("EXP UPGRADE #8", "EXP upgrade level 8.", mpf("1e1280"), mpf("1"), mpf("640")),
        Upgrade("EXP UPGRADE #9", "EXP upgrade level 9.", mpf("1e2560"), mpf("1"), mpf("1280")),
        Upgrade("EXP UPGRADE #10", "EXP upgrade level 10.", mpf("1e5120"), mpf("1"), mpf("2560"))
    ]

    # 2. The board
    board: Board = Board([
        StartTile(),
        Place("The Pygmy Wilderness", "A jungle.", mpf("1e5"), mpf("1e4"), mpf("1e3")),
        EmptySpace(),
        EmptySpace(),
        Place("Kihahancha Paradise", "A jungle.", mpf("1e10"), mpf("1e8"), mpf("1e6")),
        EmptySpace(),
        EmptySpace(),
        UpgradeShop(upgrades_sold),
        EmptySpace(),
        EmptySpace(),
        Place("The Almond Seafront", "A beach.", mpf("1e16"), mpf("1e13"), mpf("1e10")),
        EmptySpace(),
        EmptySpace(),
        EmptySpace(),
        QuizTile(),
        EmptySpace(),
        UpgradeShop(upgrades_sold),
        EmptySpace(),
        Place("Cineneh Enclave", "An island.", mpf("1e23"), mpf("1e19"), mpf("1e15")),
        EmptySpace(),
        EmptySpace(),
        RandomRewardTile(),
        EmptySpace(),
        Place("Emerheller Shallows", "A lake.", mpf("1e31"), mpf("1e26"), mpf("1e21")),
        EmptySpace(),
        EmptySpace(),
        UpgradeShop(upgrades_sold),
        EmptySpace(),
        EmptySpace(),
        Place("Chelver Waters", "A lake.", mpf("1e40"), mpf("1e34"), mpf("1e28")),
        EmptySpace(),
        QuizTile(),
        EmptySpace(),
        Place("Wreckage Bay", "A pirate cove.", mpf("1e50"), mpf("1e43"), mpf("1e36")),
        EmptySpace(),
        EmptySpace(),
        EmptySpace(),
        Place("Kraken Cay", "A pirate cove.", mpf("1e61"), mpf("1e53"), mpf("1e45")),
        EmptySpace(),
        EmptySpace(),
        RandomRewardTile(),
        Place("The Secret Haunt", "A dungeon.", mpf("1e73"), mpf("1e64"), mpf("1e55")),
        UpgradeShop(upgrades_sold),
        EmptySpace(),
        EmptySpace(),
        Place("The Nether Pits", "A dungeon.", mpf("1e86"), mpf("1e76"), mpf("1e66")),
        EmptySpace(),
        EmptySpace(),
        EmptySpace(),
        QuizTile(),
        EmptySpace(),
        EmptySpace(),
        Place("Gourdley Citadel", "A castle.", mpf("1e100"), mpf("1e89"), mpf("1e78")),
        EmptySpace(),
        EmptySpace(),
        RandomRewardTile(),
        EmptySpace(),
        UpgradeShop(upgrades_sold),
        EmptySpace(),
        EmptySpace(),
        EmptySpace(),
        Place("Kiamgema Wilderness", "A jungle.", mpf("1e115"), mpf("1e103"), mpf("1e91")),
        EmptySpace(),
        QuizTile(),
        EmptySpace(),
        Place("Baraboni Paradise", "A jungle.", mpf("1e131"), mpf("1e118"), mpf("1e105")),
        EmptySpace(),
        EmptySpace(),
        EmptySpace(),
        RandomRewardTile(),
        EmptySpace(),
        Place("Gladbour Highlands", "A mountain.", mpf("1e148"), mpf("1e134"), mpf("1e120")),
        EmptySpace(),
        UpgradeShop(upgrades_sold),
        EmptySpace(),
        Place("Blacklita Mountain", "A mountain.", mpf("1e166"), mpf("1e151"), mpf("1e136")),
        EmptySpace(),
        EmptySpace(),
        QuizTile(),
        EmptySpace(),
        EmptySpace(),
        Place("Infinite Bank", "A beach.", mpf("1e185"), mpf("1e169"), mpf("1e153")),
        RandomRewardTile(),
        EmptySpace(),
        EmptySpace(),
        Place("Nanstino Margin", "A beach.", mpf("1e205"), mpf("1e188"), mpf("1e171")),
        EmptySpace(),
        EmptySpace(),
        EmptySpace(),
        EmptySpace(),
        UpgradeShop(upgrades_sold),
        EmptySpace(),
        EmptySpace(),
        Place("Barringsor Holm", "An island.", mpf("1e226"), mpf("1e208"), mpf("1e190")),
        EmptySpace(),
        EmptySpace(),
        QuizTile(),
        EmptySpace(),
        EmptySpace(),
        Place("Sudcona Key", "An island.", mpf("1e248"), mpf("1e229"), mpf("1e210")),
        EmptySpace(),
        EmptySpace(),
        RandomRewardTile(),
        EmptySpace(),
        Place("Canhead Shallows", "A lake.", mpf("1e271"), mpf("1e251"), mpf("1e231")),
        EmptySpace(),
        EmptySpace(),
        EmptySpace(),
        EmptySpace(),
        Place("Shrewsry Domain", "A lake.", mpf("1e295"), mpf("1e274"), mpf("1e253")),
        EmptySpace(),
        EmptySpace(),
        QuizTile(),
        EmptySpace(),
        Place("Vauxcarres Timberland", "A forest.", mpf("1e320"), mpf("1e298"), mpf("1e276")),
        EmptySpace(),
        UpgradeShop(upgrades_sold),
        EmptySpace(),
        EmptySpace(),
        Place("Timber Enclave", "A pirate cove.", mpf("1e346"), mpf("1e323"), mpf("1e300")),
        EmptySpace(),
        EmptySpace(),
        EmptySpace(),
        EmptySpace(),
        Place("Cove of Salty Sands", "A pirate cove.", mpf("1e373"), mpf("1e349"), mpf("1e325")),
        EmptySpace(),
        EmptySpace(),
        QuizTile(),
        EmptySpace(),
        EmptySpace(),
        Place("Raging Prairie", "A desert.", mpf("1e401"), mpf("1e376"), mpf("1e351")),
        EmptySpace(),
        RandomRewardTile(),
        EmptySpace(),
        EmptySpace(),
        Place("Moaning Wastes", "A desert.", mpf("1e430"), mpf("1e404"), mpf("1e378")),
        EmptySpace(),
        EmptySpace(),
        QuizTile(),
        EmptySpace(),
        EmptySpace(),
        Place("Cladborough Stronghold", "A castle.", mpf("1e460"), mpf("1e433"), mpf("1e406")),
        EmptySpace(),
        UpgradeShop(upgrades_sold),
        EmptySpace(),
        EmptySpace(),
        EmptySpace(),
        Place("Grimcarres Bay", "A beach.", mpf("1e491"), mpf("1e463"), mpf("1e435")),
        EmptySpace(),
        EmptySpace(),
        EmptySpace(),
        EmptySpace(),
        Place("Brookcarres Sands", "A beach.", mpf("1e523"), mpf("1e494"), mpf("1e465")),
        EmptySpace(),
        QuizTile(),
        EmptySpace(),
        Place("Neunora Sands", "A beach.", mpf("1e556"), mpf("1e526"), mpf("1e496")),
        EmptySpace(),
        UpgradeShop(upgrades_sold),
        EmptySpace(),
        EmptySpace(),
        RandomRewardTile(),
        EmptySpace(),
        Place("Mahanmei", "A jungle.", mpf("1e590"), mpf("1e559"), mpf("1e528")),
        EmptySpace(),
        EmptySpace(),
        EmptySpace(),
        Place("The Mighty Paradise", "A jungle.", mpf("1e625"), mpf("1e593"), mpf("1e561")),
        EmptySpace(),
        RandomRewardTile(),
        EmptySpace(),
        Place("Hideout of Grog", "A pirate cove.", mpf("1e661"), mpf("1e628"), mpf("1e595")),
        EmptySpace(),
        UpgradeShop(upgrades_sold),
        EmptySpace(),
        EmptySpace(),
        EmptySpace(),
        QuizTile(),
        EmptySpace(),
        EmptySpace(),
        Place("Dead Kraken Lagoon", "A pirate cove.", mpf("1e698"), mpf("1e664"), mpf("1e630")),
        EmptySpace(),
        EmptySpace(),
        RandomRewardTile(),
        EmptySpace(),
        EmptySpace(),
        Place("Shelgue Key", "An island.", mpf("1e736"), mpf("1e701"), mpf("1e666")),
        EmptySpace(),
        EmptySpace(),
        QuizTile(),
        EmptySpace(),
        Place("The Molten Skerry", "An island.", mpf("1e775"), mpf("1e739"), mpf("1e703")),
        EmptySpace(),
        EmptySpace(),
        EmptySpace(),
        Place("Carderby Stronghold", "A castle.", mpf("1e815"), mpf("1e778"), mpf("1e741")),
        EmptySpace(),
        EmptySpace(),
        RandomRewardTile(),
        EmptySpace(),
        EmptySpace(),
        Place("The Wrinkled Domain", "A sea.", mpf("1e856"), mpf("1e818"), mpf("1e780")),
        EmptySpace(),
        UpgradeShop(upgrades_sold),
        EmptySpace(),
        EmptySpace(),
        Place("Chesterrial Waters", "A sea.", mpf("1e898"), mpf("1e859"), mpf("1e820")),
        EmptySpace(),
        EmptySpace(),
        QuizTile(),
        EmptySpace(),
        Place("The Frothy Abyss", "A sea.", mpf("1e941"), mpf("1e901"), mpf("1e861")),
        EmptySpace(),
        EmptySpace(),
        UpgradeShop(upgrades_sold),
        EmptySpace(),
        EmptySpace(),
        EmptySpace(),
        Place("Calm Loch", "A lake.", mpf("1e985"), mpf("1e944"), mpf("1e903")),
        EmptySpace(),
        EmptySpace(),
        EmptySpace(),
        EmptySpace(),
        Place("Nipatane Expanse", "A lake.", mpf("1e1030"), mpf("1e988"), mpf("1e946")),
        EmptySpace(),
        EmptySpace(),
        RandomRewardTile(),
        EmptySpace(),
        EmptySpace(),
        EmptySpace(),
        Place("New Gardens Wharf", "A harbor.", mpf("1e1076"), mpf("1e1033"), mpf("1e990")),
        EmptySpace(),
        EmptySpace(),
        UpgradeShop(upgrades_sold),
        EmptySpace(),
        EmptySpace(),
        QuizTile(),
        EmptySpace(),
        EmptySpace(),
        Place("Nokojour Landing", "A harbor.", mpf("1e1123"), mpf("1e1079"), mpf("1e1035"))
    ])

    # 3. New game representation
    new_game: Game

    # 4. Quiz questions
    quiz_questions: list = [
        QuizQuestion("What is the length of an Olympic Swimming Pool (in metres)?", [
            "A. 100 metres",
            "B. 50 metres",
            "C. 25 metres",
            "D. 75 metres"
        ], "B", mpf("1e100"), mpf("1e100")),
        QuizQuestion("What is the name of the largest ocean on earth?", [
            "A. Atlantic",
            "B. Antarctic",
            "C. Pacific",
            "D. Indian"
        ], "C", mpf("1e200"), mpf("1e200")),
        QuizQuestion("Which of the following places is a lake in this game?", [
            "A. New Gardens Wharf",
            "B. Carderby Stronghold",
            "C. The Frothy Abyss",
            "D. Calm Loch"
        ], "D", mpf("1e400"), mpf("1e400")),
        QuizQuestion("What type of place is Shelgue Key categorised as in this game?", [
            "A. An island",
            "B. A beach",
            "C. A pirate cove"
            "D. A sea"
        ], "A", mpf('1e800'), mpf("1e800")),
        QuizQuestion("Which team won the 2020-21 Premier League?", [
            "A. Manchester United",
            "B. Liverpool",
            "C. Chelsea",
            "D. Manchester City"
        ], "D", mpf("1e1600"), mpf("1e1600")),
        QuizQuestion("What type of place is Raging Prairie categorised as in this game?", [
            "A. A beach",
            "B. A desert",
            "C. An island",
            "D. A sea"
        ], "B", mpf("1e3200"), mpf("1e3200")),
        QuizQuestion("How many pirate coves are in this game?", [
            "A. 5",
            "B. 6",
            "C. 7",
            "D. 8"
        ], "B", mpf("1e6400"), mpf("1e6400")),
        QuizQuestion("How many islands are in this game?", [
            "A. 3",
            "B. 4",
            "C. 5",
            "D. 6"
        ], "C", mpf("1e12800"), mpf("1e12800")),
        QuizQuestion("How many jungles are in this game?", [
            "A. 3",
            "B. 4",
            "C. 5",
            "D. 6"
        ], "D", mpf("1e25600"), mpf("1e25600")),
        QuizQuestion("How many lakes are in this game?", [
            "A. 6",
            "B. 7",
            "C. 8",
            "D. 9"
        ], "A", mpf("1e51200"), mpf("1e51200"))
    ]

    # 5. Name of file containing saved game data
    file_name: str = "SAVED OWN THE PLANET - BOARD GAME EDITION DATA"

    try:
        new_game = load_game_data(file_name)

        # Clearing up the command line window
        clear()

        print("Current game progress:\n", str(new_game))
    except FileNotFoundError:
        # Clearing up the command line window
        clear()

        name: str = input("Please enter your name: ")
        player_data: Player = Player(name)
        new_game = Game(player_data, CPU(), board, quiz_questions)

    print("Enter 'Y' for yes.")
    print("Enter anything else for no.")
    continue_playing: str = input("Do you want to continue playing 'Own The Planet - Board Game Edition'? ")
    while continue_playing == "Y":
        # Clearing up the command line window
        clear()

        # Incrementing the value of new_game.turn
        new_game.turn += 1

        print("Your stats:\n\n" + str(new_game.player))
        print("CPU's stats:\n\n" + str(new_game.cpu))

        # Checking whether it is player's or CPU's turn
        if new_game.turn % 2 == 1:
            new_game.player.gain_turn_reward()
            print("It is your turn to roll the dice!")
            print("Enter 'ROLL' to roll the dice.")
            print("Enter anything else to save game data and quit the game.")
            action: str = input("What do you want to do? ")
            if action == "ROLL":
                new_game.player.roll_dice(new_game)
                curr_tile: Tile = new_game.board.get_tiles()[new_game.player.location]
                print("You are now at " + str(curr_tile.name) + "!")
                if isinstance(curr_tile, StartTile) or isinstance(curr_tile, EmptySpace):
                    pass  # do nothing
                elif isinstance(curr_tile, Place):
                    if curr_tile.owner is None:
                        # Ask the player whether he/she wants to buy the place or not.
                        print("Enter 'Y' for yes.")
                        print("Enter anything else for no.")
                        buy_place: str = input("Do you want to buy " + str(curr_tile.name) + "? ")
                        if buy_place == "Y":
                            if new_game.player.buy_place(curr_tile):
                                print("Congratulations! You have successfully bought " + str(curr_tile.name) + "!")
                            else:
                                print("Sorry! You have insufficient gold!")

                    elif curr_tile in new_game.player.get_owned_list():
                        # Ask the player whether he/she wants to upgrade the place or not.
                        print("Enter 'Y' for yes.")
                        print("Enter anything else for no.")
                        upgrade_place: str = input("Do you want to upgrade " + str(curr_tile.name) + "? ")
                        if upgrade_place == "Y":
                            if new_game.player.upgrade_place(curr_tile):
                                print("Congratulations! You have successfully upgraded " + str(curr_tile.name) + "!")
                            else:
                                print("Sorry! You have insufficient gold!")
                    else:
                        # Ask the player whether he/she wants to acquire the place or not.
                        print("Enter 'Y' for yes.")
                        print("Enter anything else for no.")
                        acquire_place: str = input("Do you want to acquire " + str(curr_tile.name) + "? ")
                        if acquire_place == "Y":
                            if new_game.player.acquire_place(curr_tile, curr_tile.owner):
                                print("Congratulations! You have successfully acquired " + str(curr_tile.name) + "!")
                            else:
                                print("Sorry! You have insufficient gold!")

                elif isinstance(curr_tile, RandomRewardTile):
                    # Grant random reward
                    random_reward: RandomReward = RandomReward()
                    new_game.player.get_random_reward(random_reward)
                    print("Congratulations! You earned " + str(random_reward.reward_gold) + " gold and "
                          + str(random_reward.reward_exp) + " EXP!")

                elif isinstance(curr_tile, QuizTile):
                    # Choose a question for the player to answer
                    quiz_question: QuizQuestion = new_game.get_quiz_questions() \
                        [random.randint(0, len(new_game.get_quiz_questions()) - 1)]
                    print(str(quiz_question) + "\n")
                    input_answer: str = input("Your answer: ")
                    if new_game.player.answer_quiz_question(quiz_question, input_answer):
                        print("Congratulations! Your answer is correct!")
                    else:
                        print("Your answer is incorrect!")

                elif isinstance(curr_tile, UpgradeShop):
                    # Asking whether the player wants to buy an upgrade or not.
                    print("Enter 'Y' for yes.")
                    print("Enter anything else for no.")
                    buy_upgrade: str = input("Do you want to buy an upgrade? ")

                    if buy_upgrade == "Y":
                        # Asking the player to choose which upgrade to buy.
                        print("Below is a list of upgrades sold in the upgrade shop.")
                        upgrade_index: int = 1  # initial value
                        for upgrade in curr_tile.get_upgrades_sold():
                            print("UPGRADE #" + str(upgrade_index))
                            print(str(upgrade) + "\n")
                            upgrade_index += 1

                        buy_upgrade_index: int = int(input("Please enter the index of the upgrade "
                                                           "you want to buy (1 - " +
                                                           str(len(curr_tile.get_upgrades_sold())) + "): "))
                        while buy_upgrade_index < 1 or buy_upgrade_index > len(curr_tile.get_upgrades_sold()):
                            buy_upgrade_index = int(input("Sorry, invalid input! Please enter the index of the upgrade "
                                                          "you want to buy (1 - " +
                                                          str(len(curr_tile.get_upgrades_sold())) + "): "))

                        upgrade_to_buy: Upgrade = curr_tile.get_upgrades_sold()[buy_upgrade_index - 1]
                        if new_game.player.buy_upgrade(upgrade_to_buy):
                            print("Congratulations! You have successfully bought " + str(upgrade_to_buy.name) + "!")
                        else:
                            print("Sorry! You have insufficient gold!")

                else:
                    pass  # do nothing
            else:
                break
        else:
            new_game.cpu.gain_turn_reward()
            print("It is CPU's turn to roll the dice!")
            new_game.cpu.roll_dice(new_game)
            curr_tile: Tile = new_game.board.get_tiles()[new_game.cpu.location]
            print("CPU is now at " + str(curr_tile.name) + "!")
            if isinstance(curr_tile, StartTile) or isinstance(curr_tile, EmptySpace):
                pass  # do nothing
            elif isinstance(curr_tile, Place):
                if curr_tile.owner is None:
                    buy_place: bool = random.random() <= 0.75
                    if buy_place:
                        new_game.cpu.buy_place(curr_tile)

                elif curr_tile in new_game.cpu.get_owned_list():
                    upgrade_place: bool = random.random() <= 0.75
                    if upgrade_place:
                        new_game.cpu.upgrade_place(curr_tile)
                else:
                    acquire_place: bool = random.random() <= 0.75
                    if acquire_place:
                        new_game.cpu.acquire_place(curr_tile, curr_tile.owner)

            elif isinstance(curr_tile, RandomRewardTile):
                # Grant random reward
                random_reward: RandomReward = RandomReward()
                new_game.cpu.get_random_reward(random_reward)
                print("CPU earned " + str(random_reward.reward_gold) + " gold and "
                      + str(random_reward.reward_exp) + " EXP!")

            elif isinstance(curr_tile, QuizTile):
                # Choose a question for the CPU to answer
                quiz_question: QuizQuestion = new_game.get_quiz_questions() \
                    [random.randint(0, len(new_game.get_quiz_questions()) - 1)]
                possible_answers: list = ["A", "B", "C", "D"]
                input_answer: str = possible_answers[random.randint(0, len(possible_answers) - 1)]
                new_game.cpu.answer_quiz_question(quiz_question, input_answer)

            elif isinstance(curr_tile, UpgradeShop):
                buy_upgrade: bool = random.random() <= 0.75
                if buy_upgrade:
                    buy_upgrade_index: int = random.randint(1, len(curr_tile.get_upgrades_sold()))
                    upgrade_to_buy: Upgrade = curr_tile.get_upgrades_sold()[buy_upgrade_index - 1]
                    new_game.cpu.buy_upgrade(upgrade_to_buy)
            else:
                pass  # do nothing

        print("Enter 'Y' for yes.")
        print("Enter anything else for no.")
        continue_playing = input("Do you want to continue playing 'Own The Planet - Board Game Edition'? ")

    # Saving game data and quitting the game.
    save_game_data(new_game, file_name)
    return 0


if __name__ == '__main__':
    main()
