"""
for calculating rating change for a game, as well as probability
"""

from multipliers import elo_multiplier,margin_of_victory

def per_game(k_factor, winning_team, losing_team, lead, s = 400):
    expected_score = elo_multiplier(winning_team,losing_team,s)
    return k_factor * margin_of_victory(
        winning_team,
        losing_team,
        lead
    ) * (1-expected_score), expected_score