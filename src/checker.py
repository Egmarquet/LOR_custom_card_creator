
unit_types = [
    'unit_norare',
    'unit_common',
    'unit_rare',
    'unit_epic',
    'unit_champion_base',
    'unit_champion_lvlup'
]

spell_types = [
    'spell_burst_common',
    'spell_burst_rare',
    'spell_burst_epic',
    'spell_burst_norare'
    'spell_slow_common',
    'spell_slow_rare',
    'spell_slow_epic',
    'spell_slow_norare',
    'spell_fast_common',
    'spell_fast_rare',
    'spell_fast_epic',
    'spell_fast_norare'
]

regions = [
    'bandle city',
    'bilgewater',
    'demacia',
    'freljord:',
    'ionia',
    'noxus',
    'piltover zaun',
    'runeterra',
    'shadow isles',
    'shurima',
    'targon',
    'void'
]

keywords = [
    'overwhelm',
    'double attack',
    'regeneration',
    'tough',
    'elusive',
    'lifesteal',
    'quick attack',
    'barrier',
    'ephemeral',
    'challenger',
    'fleeting',
    'fearsome',
    "can't block",
    'burst',
    'fast',
    'slow'
]

def check(field, value, allowed):
    if isinstance(value, list):
        rejected = str([v for v in value if v not in allowed])
        if rejected:
            return (False, {field:f'{rejected} Not accepted, must be one of {allowed}'})
        else:
            return (True,None)

    elif value in allowed:
        return (True,None)
    else:
        return (False,{field: f'Not accepted, must be one of {allowed}'})
