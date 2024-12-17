# Copyright 2023 DeepMind Technologies
#
# Licensed under the Apache License, Version 2.0 (the "License");
# ...

"""A pyspiel config for a ransomware negotiation chat game."""

import collections

from ml_collections import config_dict

# Import necessary modules, renamed for the ransomware negotiation game
from open_spiel.python.games.chat_games.envs.base_envs import ransomware_negotiation_with_tone_info as env_ransomware_negotiation
from open_spiel.python.games.chat_games.envs.observations import summary
from open_spiel.python.games.chat_games.envs.observations import utils as obs_utils
from open_spiel.python.games.chat_games.envs.payoffs import ransomware_negotiation as payoffs_ransomware_negotiation
from open_spiel.python.games.chat_games.envs.scenarios.domains import ransomware_negotiation as scenario_ransomware_negotiation

def get_config():
    """Get configuration for the ransomware negotiation chat game."""
    config = config_dict.ConfigDict()

    num_players = 2

    # Observations for each player
    observations = [
        obs_utils.Observation(summary.PREFIX, summary.POSTFIX)
        for _ in range(num_players)
    ]

    # Header information specific to the ransomware game
    header = env_ransomware_negotiation.HEADER

    # Payoff function for the ransomware negotiation
    payoffs = [payoffs_ransomware_negotiation.PAYOFF]

    # Define the possible actions (tones) for negotiation strategies
    given_prompt_actions = collections.OrderedDict()
    negotiation_tones = ['threatening', 'conciliatory', 'firm', 'empathetic', 'any']
    given_prompt_actions[header.action_keys[0]] = negotiation_tones
    num_tones = len(negotiation_tones)

    # Private information for each player (e.g., ransom demand, data importance)
    given_private_info = collections.OrderedDict()
    given_private_info['ransom_demand'] = [
        scenario_ransomware_negotiation.RANSOM_DEMAND_ATTACKER,
        scenario_ransomware_negotiation.RANSOM_DEMAND_DEFENDER
    ]
    given_private_info['data_importance'] = [
        scenario_ransomware_negotiation.DATA_IMPORTANCE_ATTACKER,
        scenario_ransomware_negotiation.DATA_IMPORTANCE_DEFENDER
    ]

    # Define the initial scenario
    scenario_a = env_ransomware_negotiation.Scenario(
        scenario_ransomware_negotiation.SCENARIO_A,
        'Attacker',
        'Defender',
        scenario_ransomware_negotiation.RANSOM_DEMAND_ATTACKER,
        scenario_ransomware_negotiation.DATA_IMPORTANCE_DEFENDER,
        'firm'
    )

    # LLM termination prompt specific to the ransomware game
    llm_termination_prompt = scenario_ransomware_negotiation.LLM_TERMINATION_PROMPT

    params = {
        'num_distinct_actions': num_players * num_tones,
        'num_llm_seeds': 2,
        'num_players': num_players,
        'min_utility': min([float(p.min) for p in payoffs]),
        'max_utility': max([float(p.max) for p in payoffs]),
        'num_max_replies': 1
    }

    config.params = params

    config.game = config_dict.ConfigDict()
    config.game.observations = observations
    config.game.header = header
    config.game.payoffs = payoffs
    config.game.given_prompt_actions = given_prompt_actions
    config.game.num_private_info = (2, 2)
    config.game.given_names = ['Attacker', 'Defender']
    config.game.given_private_info = given_private_info
    config.game.initial_scenario = scenario_a
    config.game.llm_list_suffix = 'Response: '
    config.game.llm_termination_prompt = llm_termination_prompt

    return config
