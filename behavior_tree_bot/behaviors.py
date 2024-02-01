import sys

sys.path.insert(0, "../")
from planet_wars import issue_order
from random import randrange


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(
            state,
            strongest_planet.ID,
            weakest_planet.ID,
            strongest_planet.num_ships / 2,
        )


def spread_to_weakest_neutral_planet(state):
    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(
        state.neutral_planets(), key=lambda p: p.num_ships, default=None
    )

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(
            state,
            strongest_planet.ID,
            weakest_planet.ID,
            strongest_planet.num_ships / 2,
        )


def attack_closest(state):
    # (1) If we currently have a fleet in flight, abort plan.
    # if len(state.my_fleets()) >= 1:
    #     return False
    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the closest enemy planet.
    closest_planet = min(
        state.neutral_planets() + state.enemy_planets(),
        key=lambda t: state.distance(strongest_planet.ID, t.ID),
        default=None,
    )
    ships_needed = (
        closest_planet.num_ships
        + state.distance(strongest_planet.ID, closest_planet.ID)
        * strongest_planet.growth_rate
        + 1
    )

    if not strongest_planet or not closest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(
            state,
            strongest_planet.ID,
            closest_planet.ID,
            ships_needed,
        )


def attack_closest_enemy(state):
    # (1) If we currently have a fleet in flight, abort plan.
    # if len(state.my_fleets()) >= 1:
    #     return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the closest enemy planet.
    closest_planet = min(
        state.enemy_planets(),
        key=lambda t: state.distance(strongest_planet.ID, t.ID),
        default=None,
    )

    if not strongest_planet or not closest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(
            state,
            strongest_planet.ID,
            closest_planet.ID,
            strongest_planet.num_ships / 2,
        )


def attack_largest_growth_rate(state):
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    largest_growth_planet = max(
        state.my_planets() + state.not_my_planets(),
        key=lambda p: p.growth_rate,
        default=None,
    )
    if not strongest_planet or not largest_growth_planet:
        # No legal source or destination
        return False

    return issue_order(
        state,
        strongest_planet.ID,
        largest_growth_planet.ID,
        strongest_planet.num_ships / 2,
    )


def reinforce(state):
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    current_planets = list(
        filter(lambda e: e.ID != strongest_planet.ID, state.my_planets())
    )
    if len(current_planets) == 0:
        return False
    random_planet = randrange(0, len(current_planets))
    return issue_order(
        state,
        current_planets[random_planet].ID,
        strongest_planet.ID,
        current_planets[random_planet].num_ships / 2,
    )
