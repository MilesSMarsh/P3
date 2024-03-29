def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) + sum(
        fleet.num_ships for fleet in state.my_fleets()
    ) > sum(planet.num_ships for planet in state.enemy_planets()) + sum(
        fleet.num_ships for fleet in state.enemy_fleets()
    )


def have_small_amount_of_planets(state):
    return len(state.my_planets()) < 5


def neutral_planets_left(state):
    return len(state.neutral_planets()) > 0


def check_has_LGR(state):
    own_growth = sum(p.growth_rate for p in state.my_planets())
    enemy_growth = sum(p.growth_rate for p in state.enemy_planets())

    return own_growth >= enemy_growth


def check_ships(state):
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet:
        return False
    closest_planet = min(
        state.neutral_planets() + state.enemy_planets(),
        key=lambda t: state.distance(strongest_planet.ID, t.ID),
        default=None,
    )
    if not closest_planet:
        return False
    return (
        strongest_planet.num_ships
        > closest_planet.num_ships
        + state.distance(strongest_planet.ID, closest_planet.ID)
        * closest_planet.growth_rate
        + 1
    )
