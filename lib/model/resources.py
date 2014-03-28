ALL_RESOURCES = [ORE, METAL, THORIUM, HYDROCARBON, DEUTERIUM]

ORE = 'ore'
METAL = 'metal'
THORIUM = 'thorium'
HYDROCARBON = 'hydrocarbon'
DEUTERIUM = 'deuterium'
SUN = 'sun'
ELECTRICITY = 'electricity'

def update_resources(resources, rates, num_secs, maxes=None):
    for res in ALL_RESOURCES:
        update = num_secs * rates[res]
        new_val = resources[res] + update
        if maxes and new_val > maxes[res]:
            new_val = maxes[res]
        resources[res] = new_val
