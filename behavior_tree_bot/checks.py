def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) + sum(
        fleet.num_ships for fleet in state.my_fleets()
    ) > sum(planet.num_ships for planet in state.enemy_planets()) + sum(
        fleet.num_ships for fleet in state.enemy_fleets()
    )


def have_smaller_fleet(state):
    return not (
        sum(planet.num_ships for planet in state.my_planets())
        + sum(fleet.num_ships for fleet in state.my_fleets())
        > sum(planet.num_ships for planet in state.enemy_planets())
        + sum(fleet.num_ships for fleet in state.enemy_fleets())
    )


def check_if_LGR(state):
    largest_growth_planet = max(
        state.my_planets() + state.not_my_planets(),
        key=lambda p: p.growth_rate,
        default=None,
    )

    return largest_growth_planet in state.my_planets()
