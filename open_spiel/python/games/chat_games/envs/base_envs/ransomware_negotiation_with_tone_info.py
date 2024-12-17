# Copyright 2023 DeepMind Technologies
#
# Licensed under the Apache License, Version 2.0 (the "License");
# ...

"""A base environment for a ransomware negotiation chat game."""

import dataclasses

from open_spiel.python.games.chat_games.envs.comm_substrates import negotiations
from open_spiel.python.games.chat_games.envs.scenarios.domains import ransomware_negotiation as scenario_ransomware_negotiation
from open_spiel.python.games.chat_games.envs.utils import header
from open_spiel.python.games.chat_games.envs.utils import text

# Define action and info keys relevant to ransomware negotiation
action_keys = tuple(['tone'])
info_keys = ('ransom_demand', 'data_importance')

# Negotiation options format
negotiation_opts = (
    negotiations.NEGOTIATION_OPTS_PREFIX +
    'Ransom Demand:\n{ransom_demand}\n\n' +
    'Data Importance:\n{data_importance}\n\n' +
    'Tone: Use a {negotiation_tone} tone.\n' +
    negotiations.PLAIN
)

# Example dialogues demonstrating possible negotiation scenarios

# Example 1: Negotiation breaks down
email_1a = [
    'Hello Defender,',
    'We have encrypted your sensitive data. To regain access, you must pay 500,000 USD.',
    'You have 48 hours.',
    'Best regards,',
    'Attacker'
]
email_1a = (
    negotiations.PLAIN.format(sender='Attacker', receiver='Defender') +
    '\n\n'.join(text.wrap(email_1a))
)

email_2a = [
    'Hello Attacker,',
    'We will not negotiate under threats. Your actions are illegal, and authorities have been notified.',
    'This conversation is over.',
    'Sincerely,',
    'Defender'
]
email_2a = (
    negotiations.PLAIN.format(sender='Defender', receiver='Attacker') +
    '\n\n'.join(text.wrap(email_2a))
)

example_a = email_1a + email_2a
example_a = example_a.strip('\n')

# Example 2: Successful negotiation
email_1b = [
    'Hello Defender,',
    'Your data has been encrypted. To restore access, please pay 200,000 USD.',
    'Payment details are attached.',
    'Regards,',
    'Attacker'
]
email_1b = (
    negotiations.PLAIN.format(sender='Attacker', receiver='Defender') +
    '\n\n'.join(text.wrap(email_1b))
)

email_2b = [
    'Hello Attacker,',
    'We are willing to cooperate. However, the amount is too high for us.',
    'Can we agree on 100,000 USD?',
    'Thank you,',
    'Defender'
]
email_2b = (
    negotiations.PLAIN.format(sender='Defender', receiver='Attacker') +
    '\n\n'.join(text.wrap(email_2b))
)

email_3b = [
    'Defender,',
    'We accept your offer of 100,000 USD.',
    'Follow the payment instructions to regain access.',
    'Attacker'
]
email_3b = (
    negotiations.PLAIN.format(sender='Attacker', receiver='Defender') +
    '\n\n'.join(text.wrap(email_3b))
)

example_b = email_1b + email_2b + email_3b
example_b = example_b.strip('\n')

# Instructions and context for the LLM
instr_a = [
    'You are participating in a simulated ransomware negotiation. Your goal is to negotiate terms that are favorable for you while aiming for a resolution.',
    'You will read a dialogue between an attacker and a defender. After that, you will receive information about your position, including the ransom demand and the importance of the data involved.',
    'Based on this information, decide whether to:',
    '1) Accept the terms if they are acceptable to you.',
    '2) Reject the negotiation if an agreement cannot be reached.',
    '3) Propose a counter-offer with adjusted terms.',
    'Consider the following example dialogues. Components of the examples are separated by "&". Here is the first example where the negotiation breaks down.',
    '&' * 50
]
instr_b = [
    '&' * 50,
    'Here is a second example where the negotiation leads to an agreement.',
    '&' * 50
]
instr_c = [
    '&' * 50,
    'Now, you will receive your own negotiation scenario. Use the information provided to craft an appropriate response.',
    '&' * 50
]

# Information provided to the player
info = negotiation_opts.format(
    ransom_demand=scenario_ransomware_negotiation.RANSOM_DEMAND_ATTACKER,
    data_importance=scenario_ransomware_negotiation.DATA_IMPORTANCE_DEFENDER,
    negotiation_tone='firm'
).strip('\n')

# Assemble the context
context = (
    text.wrap(instr_a) + [example_a] +
    text.wrap(instr_b) + [example_b] +
    text.wrap(instr_c) + [info]
)

# Define the header
HEADER = header.Header(
    negotiations.PLAIN,
    negotiation_opts,
    negotiations.strip_msg,
    negotiations.SPECIAL_CHARS,
    action_keys,
    info_keys,
    '\n\n'.join(context)
)

@dataclasses.dataclass(frozen=True)
class Scenario(header.BaseScenario):
    ransom_demand: str
    data_importance: str
    negotiation_tone: str = 'firm'
