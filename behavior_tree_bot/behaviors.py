import sys

sys.path.insert(0, "../")
from planet_wars import issue_order


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
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

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


def consolidate(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my weakest planet
    weakest_planet = min(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find my planet with the highest growth rate
    LGR_planet = max(state.my_planets(), key=lambda p: p.growth_rate, default=None)

    # (4) determine number of ships to send
    num_ships_to_send = weakest_planet.num_ships / 2

    if not LGR_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (5) send ships from weak planet to LGR planet
        return issue_order(state, weakest_planet.ID, LGR_planet.ID, num_ships_to_send)


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


def send_to_closest_LGR(state):
    largest_growth_planet = max(
        state.my_planets(),
        key=lambda p: p.growth_rate,
        default=None,
    )

    closest_planet = min(
        state.not_my_planets(),
        key=lambda p: state.distance(largest_growth_planet, p),
        default=None,
    )
    return issue_order(
        state,
        largest_growth_planet,
        closest_planet,
        largest_growth_planet.num_ships / 2,
    )
