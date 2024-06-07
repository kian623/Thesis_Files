"""
core formulas for ratings (probabilities in elo multiplier, MOV multiplier for margin_of_victory)
"""

def elo_multiplier(team,opponent,s = 400):
    return 1/(1+10 ** ((opponent - team)/(s)))

def margin_of_victory(winning_team,losing_team,lead):
    return ((lead + 3) ** 0.8)/(7.5+ 0.006 *(winning_team-losing_team))