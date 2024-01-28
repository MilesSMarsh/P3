#!/usr/bin/env python
#

"""
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import logging, traceback, sys, os, inspect

logging.basicConfig(filename=__file__[:-3] + ".log", filemode="w", level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check

from planet_wars import PlanetWars, finish_turn


# You have to improve this tree or create an entire new one that is capable
# of winning against all the 5 opponent bots
def setup_behavior_tree():
    # Top-down construction of behavior tree
    root = Selector(name="High Level Ordering of Strategies")

    spread_sequence = Sequence(name="spread")

    check_amount_of_planets = Check(have_small_amount_of_planets)
    spread_selector = Selector(name="spread_selector")

    neutral_sequence = Sequence(name="neutral_sequence")
    enemy_spread_action = Action(attack_weakest_enemy_planet)

    neutral_exist = Check(neutral_planets_left)
    neutral_spread_action = Action(spread_to_weakest_neutral_planet)

    neutral_sequence.child_nodes = [neutral_exist, neutral_spread_action]
    spread_selector.child_nodes = [neutral_sequence, enemy_spread_action]
    spread_sequence.child_nodes = [check_amount_of_planets, spread_selector]

    attacking_selector = Selector(name="attacking selector")
    larger_growth_sequence = Sequence()
    check_growth_node = Check(check_has_LGR)
    attack_largest_enemy = Action(attack_largest_growth_rate)
    attack_smallest_enemy = Action(attack_weakest_enemy_planet)

    larger_growth_sequence.child_nodes = [check_growth_node, attack_largest_enemy]
    attacking_selector.child_nodes = [larger_growth_sequence, attack_smallest_enemy]

    root.child_nodes = [spread_sequence, attacking_selector, enemy_spread_action]

    logging.info("\n" + root.tree_to_string())
    return root


# You don't need to change this function
def do_turn(state):
    behavior_tree.execute(planet_wars)


if __name__ == "__main__":
    logging.basicConfig(
        filename=__file__[:-3] + ".log", filemode="w", level=logging.DEBUG
    )

    behavior_tree = setup_behavior_tree()
    try:
        map_data = ""
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                do_turn(planet_wars)
                finish_turn()
                map_data = ""
            else:
                map_data += current_line + "\n"

    except KeyboardInterrupt:
        print("ctrl-c, leaving ...")
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")
