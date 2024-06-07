"""
for calculating probability of a team to win each round for simulate.py
"""
import math
from multipliers import elo_multiplier as win_chance

def combination(n,r):
    return math.factorial(n)/(math.factorial(n-r)*math.factorial(r))

def binomial_pmf(wins,games,per_game_win_probability):
    return combination(games,wins) * (per_game_win_probability ** wins) * ((1-per_game_win_probability) ** (games-wins))

def binomial_cdf(max_games,per_game_win_probability):
    max_wins = (max_games + 1) // 2 # max_wins is half the number of available games rounded up
    total_probability = 0
    for games in range(max_wins, max_games+1):
        total_probability += binomial_pmf(max_wins-1,games-1,per_game_win_probability)*per_game_win_probability
    return total_probability

def twice_to_beat_cdf(per_game_win_probability):
    return per_game_win_probability + (1-per_game_win_probability)*per_game_win_probability

# create dictionary containing probabilities of each team beating every other team    
def win_probability_matrix(teams): # teams is a dictionary, seed: rating
    prob_matrix = {
        1 : 0,
        2 : 0,
        3 : 0,
        4 : 0,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0,
    }
                    
    for idx in range(1,9):
        temp_prob_matrix = {
            1 : 0,
            2 : 0,
            3 : 0,
            4 : 0,
            5 : 0,
            6 : 0,
            7 : 0,
            8 : 0,
        }
        for idx2 in range(1,9):
            if idx != idx2:
                temp_prob_matrix[idx2] = win_chance(teams[idx],teams[idx2],400)
        prob_matrix[idx] = temp_prob_matrix
    return prob_matrix

def predict_wins_twice2_b05sf(teams):
    
    prob_matrix = win_probability_matrix(teams)
    
    # win_round_matchup_seed: probability of seed to win matchup of round
    
    win_1_1_1 = twice_to_beat_cdf(prob_matrix[1][8])
    win_1_1_8 = 1-win_1_1_1
    win_1_2_4 = binomial_cdf(3,prob_matrix[4][5])
    win_1_2_5 = 1-win_1_2_4
    win_1_3_2 = twice_to_beat_cdf(prob_matrix[2][7])
    win_1_3_7 = 1-win_1_3_2
    win_1_4_3 = binomial_cdf(3,prob_matrix[3][6])
    win_1_4_6 = 1-win_1_4_3
    
    win_2_1_1 = win_1_1_1 * (binomial_cdf(5,prob_matrix[1][4]) * win_1_2_4 + binomial_cdf(5,prob_matrix[1][5]) * win_1_2_5)
    win_2_1_8 = win_1_1_8 * (binomial_cdf(5,prob_matrix[8][4]) * win_1_2_4 + binomial_cdf(5,prob_matrix[8][5]) * win_1_2_5)
    win_2_1_4 = win_1_2_4 * (binomial_cdf(5,prob_matrix[4][1]) * win_1_1_1 + binomial_cdf(5,prob_matrix[4][8]) * win_1_1_8)
    win_2_1_5 = win_1_2_5 * (binomial_cdf(5,prob_matrix[5][1]) * win_1_1_1 + binomial_cdf(5,prob_matrix[5][8]) * win_1_1_8)
    win_2_2_2 = win_1_3_2 * (binomial_cdf(5,prob_matrix[2][3]) * win_1_4_3 + binomial_cdf(5,prob_matrix[2][6]) * win_1_4_6)
    win_2_2_7 = win_1_3_7 * (binomial_cdf(5,prob_matrix[7][3]) * win_1_4_3 + binomial_cdf(5,prob_matrix[7][6]) * win_1_4_6)
    win_2_2_3 = win_1_4_3 * (binomial_cdf(5,prob_matrix[3][2]) * win_1_3_2 + binomial_cdf(5,prob_matrix[3][7]) * win_1_3_7)
    win_2_2_6 = win_1_4_6 * (binomial_cdf(5,prob_matrix[6][2]) * win_1_3_2 + binomial_cdf(5,prob_matrix[6][7]) * win_1_3_7)
    
    win_3_1 = win_2_1_1 * (binomial_cdf(7,prob_matrix[1][2]) * win_2_2_2 + binomial_cdf(7,prob_matrix[1][7]) * win_2_2_7 + binomial_cdf(7,prob_matrix[1][3]) * win_2_2_3 + binomial_cdf(7,prob_matrix[1][6]) * win_2_2_6)
    win_3_8 = win_2_1_8 * (binomial_cdf(7,prob_matrix[8][2]) * win_2_2_2 + binomial_cdf(7,prob_matrix[8][7]) * win_2_2_7 + binomial_cdf(7,prob_matrix[8][3]) * win_2_2_3 + binomial_cdf(7,prob_matrix[8][6]) * win_2_2_6)
    win_3_4 = win_2_1_4 * (binomial_cdf(7,prob_matrix[4][2]) * win_2_2_2 + binomial_cdf(7,prob_matrix[4][7]) * win_2_2_7 + binomial_cdf(7,prob_matrix[4][3]) * win_2_2_3 + binomial_cdf(7,prob_matrix[4][6]) * win_2_2_6)
    win_3_5 = win_2_1_5 * (binomial_cdf(7,prob_matrix[5][2]) * win_2_2_2 + binomial_cdf(7,prob_matrix[5][7]) * win_2_2_7 + binomial_cdf(7,prob_matrix[5][3]) * win_2_2_3 + binomial_cdf(7,prob_matrix[5][6]) * win_2_2_6)
    win_3_2 = win_2_2_2 * (binomial_cdf(7,prob_matrix[2][1]) * win_2_1_1 + binomial_cdf(7,prob_matrix[2][8]) * win_2_1_8 + binomial_cdf(7,prob_matrix[2][4]) * win_2_1_4 + binomial_cdf(7,prob_matrix[2][5]) * win_2_1_5)
    win_3_7 = win_2_2_7 * (binomial_cdf(7,prob_matrix[7][1]) * win_2_1_1 + binomial_cdf(7,prob_matrix[7][8]) * win_2_1_8 + binomial_cdf(7,prob_matrix[7][4]) * win_2_1_4 + binomial_cdf(7,prob_matrix[7][5]) * win_2_1_5)
    win_3_3 = win_2_2_3 * (binomial_cdf(7,prob_matrix[3][1]) * win_2_1_1 + binomial_cdf(7,prob_matrix[3][8]) * win_2_1_8 + binomial_cdf(7,prob_matrix[3][4]) * win_2_1_4 + binomial_cdf(7,prob_matrix[3][5]) * win_2_1_5)
    win_3_6 = win_2_2_6 * (binomial_cdf(7,prob_matrix[6][1]) * win_2_1_1 + binomial_cdf(7,prob_matrix[6][8]) * win_2_1_8 + binomial_cdf(7,prob_matrix[6][4]) * win_2_1_4 + binomial_cdf(7,prob_matrix[6][5]) * win_2_1_5)
    
    # probability of seed to win rounds 1,2,3
    series_wins = {
        1 : [win_1_1_1,win_2_1_1,win_3_1],
        2 : [win_1_3_2,win_2_2_2,win_3_2],
        3 : [win_1_4_3,win_2_2_3,win_3_3],
        4 : [win_1_2_4,win_2_1_4,win_3_4],
        5 : [win_1_2_5,win_2_1_5,win_3_5],
        6 : [win_1_4_6,win_2_2_6,win_3_6],
        7 : [win_1_3_7,win_2_2_7,win_3_7],
        8 : [win_1_1_8,win_2_1_8,win_3_8]
    }
    
    for key,value in series_wins.items():
        value.append(0) # expected number of series wins is value[3] 
        for idx in range(3):
            value[3] += value[idx]
    
    return series_wins

def predict_wins_twice4_b05sf(teams):
    
    prob_matrix = win_probability_matrix(teams)
    
    # win_round_matchup_seed: probability of seed to win matchup of round
    
    win_1_1_1 = twice_to_beat_cdf(prob_matrix[1][8])
    win_1_1_8 = 1-win_1_1_1
    win_1_2_4 = twice_to_beat_cdf(prob_matrix[4][5])
    win_1_2_5 = 1-win_1_2_4
    win_1_3_2 = twice_to_beat_cdf(prob_matrix[2][7])
    win_1_3_7 = 1-win_1_3_2
    win_1_4_3 = twice_to_beat_cdf(prob_matrix[3][6])
    win_1_4_6 = 1-win_1_4_3
    
    win_2_1_1 = win_1_1_1 * (binomial_cdf(5,prob_matrix[1][4]) * win_1_2_4 + binomial_cdf(5,prob_matrix[1][5]) * win_1_2_5)
    win_2_1_8 = win_1_1_8 * (binomial_cdf(5,prob_matrix[8][4]) * win_1_2_4 + binomial_cdf(5,prob_matrix[8][5]) * win_1_2_5)
    win_2_1_4 = win_1_2_4 * (binomial_cdf(5,prob_matrix[4][1]) * win_1_1_1 + binomial_cdf(5,prob_matrix[4][8]) * win_1_1_8)
    win_2_1_5 = win_1_2_5 * (binomial_cdf(5,prob_matrix[5][1]) * win_1_1_1 + binomial_cdf(5,prob_matrix[5][8]) * win_1_1_8)
    win_2_2_2 = win_1_3_2 * (binomial_cdf(5,prob_matrix[2][3]) * win_1_4_3 + binomial_cdf(5,prob_matrix[2][6]) * win_1_4_6)
    win_2_2_7 = win_1_3_7 * (binomial_cdf(5,prob_matrix[7][3]) * win_1_4_3 + binomial_cdf(5,prob_matrix[7][6]) * win_1_4_6)
    win_2_2_3 = win_1_4_3 * (binomial_cdf(5,prob_matrix[3][2]) * win_1_3_2 + binomial_cdf(5,prob_matrix[3][7]) * win_1_3_7)
    win_2_2_6 = win_1_4_6 * (binomial_cdf(5,prob_matrix[6][2]) * win_1_3_2 + binomial_cdf(5,prob_matrix[6][7]) * win_1_3_7)
    
    win_3_1 = win_2_1_1 * (binomial_cdf(7,prob_matrix[1][2]) * win_2_2_2 + binomial_cdf(7,prob_matrix[1][7]) * win_2_2_7 + binomial_cdf(7,prob_matrix[1][3]) * win_2_2_3 + binomial_cdf(7,prob_matrix[1][6]) * win_2_2_6)
    win_3_8 = win_2_1_8 * (binomial_cdf(7,prob_matrix[8][2]) * win_2_2_2 + binomial_cdf(7,prob_matrix[8][7]) * win_2_2_7 + binomial_cdf(7,prob_matrix[8][3]) * win_2_2_3 + binomial_cdf(7,prob_matrix[8][6]) * win_2_2_6)
    win_3_4 = win_2_1_4 * (binomial_cdf(7,prob_matrix[4][2]) * win_2_2_2 + binomial_cdf(7,prob_matrix[4][7]) * win_2_2_7 + binomial_cdf(7,prob_matrix[4][3]) * win_2_2_3 + binomial_cdf(7,prob_matrix[4][6]) * win_2_2_6)
    win_3_5 = win_2_1_5 * (binomial_cdf(7,prob_matrix[5][2]) * win_2_2_2 + binomial_cdf(7,prob_matrix[5][7]) * win_2_2_7 + binomial_cdf(7,prob_matrix[5][3]) * win_2_2_3 + binomial_cdf(7,prob_matrix[5][6]) * win_2_2_6)
    win_3_2 = win_2_2_2 * (binomial_cdf(7,prob_matrix[2][1]) * win_2_1_1 + binomial_cdf(7,prob_matrix[2][8]) * win_2_1_8 + binomial_cdf(7,prob_matrix[2][4]) * win_2_1_4 + binomial_cdf(7,prob_matrix[2][5]) * win_2_1_5)
    win_3_7 = win_2_2_7 * (binomial_cdf(7,prob_matrix[7][1]) * win_2_1_1 + binomial_cdf(7,prob_matrix[7][8]) * win_2_1_8 + binomial_cdf(7,prob_matrix[7][4]) * win_2_1_4 + binomial_cdf(7,prob_matrix[7][5]) * win_2_1_5)
    win_3_3 = win_2_2_3 * (binomial_cdf(7,prob_matrix[3][1]) * win_2_1_1 + binomial_cdf(7,prob_matrix[3][8]) * win_2_1_8 + binomial_cdf(7,prob_matrix[3][4]) * win_2_1_4 + binomial_cdf(7,prob_matrix[3][5]) * win_2_1_5)
    win_3_6 = win_2_2_6 * (binomial_cdf(7,prob_matrix[6][1]) * win_2_1_1 + binomial_cdf(7,prob_matrix[6][8]) * win_2_1_8 + binomial_cdf(7,prob_matrix[6][4]) * win_2_1_4 + binomial_cdf(7,prob_matrix[6][5]) * win_2_1_5)
    
    series_wins = {
        1 : [win_1_1_1,win_2_1_1,win_3_1],
        2 : [win_1_3_2,win_2_2_2,win_3_2],
        3 : [win_1_4_3,win_2_2_3,win_3_3],
        4 : [win_1_2_4,win_2_1_4,win_3_4],
        5 : [win_1_2_5,win_2_1_5,win_3_5],
        6 : [win_1_4_6,win_2_2_6,win_3_6],
        7 : [win_1_3_7,win_2_2_7,win_3_7],
        8 : [win_1_1_8,win_2_1_8,win_3_8]
    }
    
    for key,value in series_wins.items():
        value.append(0)
        for idx in range(3):
            value[3] += value[idx]
    
    return series_wins

def predict_wins_twice2_b07sf(teams):
    
    prob_matrix = win_probability_matrix(teams)
    
    # win_round_matchup_seed: probability of seed to win matchup of round
    
    win_1_1_1 = twice_to_beat_cdf(prob_matrix[1][8])
    win_1_1_8 = 1-win_1_1_1
    win_1_2_4 = binomial_cdf(3,prob_matrix[4][5])
    win_1_2_5 = 1-win_1_2_4
    win_1_3_2 = twice_to_beat_cdf(prob_matrix[2][7])
    win_1_3_7 = 1-win_1_3_2
    win_1_4_3 = binomial_cdf(3,prob_matrix[3][6])
    win_1_4_6 = 1-win_1_4_3
    
    win_2_1_1 = win_1_1_1 * (binomial_cdf(7,prob_matrix[1][4]) * win_1_2_4 + binomial_cdf(7,prob_matrix[1][5]) * win_1_2_5)
    win_2_1_8 = win_1_1_8 * (binomial_cdf(7,prob_matrix[8][4]) * win_1_2_4 + binomial_cdf(7,prob_matrix[8][5]) * win_1_2_5)
    win_2_1_4 = win_1_2_4 * (binomial_cdf(7,prob_matrix[4][1]) * win_1_1_1 + binomial_cdf(7,prob_matrix[4][8]) * win_1_1_8)
    win_2_1_5 = win_1_2_5 * (binomial_cdf(7,prob_matrix[5][1]) * win_1_1_1 + binomial_cdf(7,prob_matrix[5][8]) * win_1_1_8)
    win_2_2_2 = win_1_3_2 * (binomial_cdf(7,prob_matrix[2][3]) * win_1_4_3 + binomial_cdf(7,prob_matrix[2][6]) * win_1_4_6)
    win_2_2_7 = win_1_3_7 * (binomial_cdf(7,prob_matrix[7][3]) * win_1_4_3 + binomial_cdf(7,prob_matrix[7][6]) * win_1_4_6)
    win_2_2_3 = win_1_4_3 * (binomial_cdf(7,prob_matrix[3][2]) * win_1_3_2 + binomial_cdf(7,prob_matrix[3][7]) * win_1_3_7)
    win_2_2_6 = win_1_4_6 * (binomial_cdf(7,prob_matrix[6][2]) * win_1_3_2 + binomial_cdf(7,prob_matrix[6][7]) * win_1_3_7)
    
    win_3_1 = win_2_1_1 * (binomial_cdf(7,prob_matrix[1][2]) * win_2_2_2 + binomial_cdf(7,prob_matrix[1][7]) * win_2_2_7 + binomial_cdf(7,prob_matrix[1][3]) * win_2_2_3 + binomial_cdf(7,prob_matrix[1][6]) * win_2_2_6)
    win_3_8 = win_2_1_8 * (binomial_cdf(7,prob_matrix[8][2]) * win_2_2_2 + binomial_cdf(7,prob_matrix[8][7]) * win_2_2_7 + binomial_cdf(7,prob_matrix[8][3]) * win_2_2_3 + binomial_cdf(7,prob_matrix[8][6]) * win_2_2_6)
    win_3_4 = win_2_1_4 * (binomial_cdf(7,prob_matrix[4][2]) * win_2_2_2 + binomial_cdf(7,prob_matrix[4][7]) * win_2_2_7 + binomial_cdf(7,prob_matrix[4][3]) * win_2_2_3 + binomial_cdf(7,prob_matrix[4][6]) * win_2_2_6)
    win_3_5 = win_2_1_5 * (binomial_cdf(7,prob_matrix[5][2]) * win_2_2_2 + binomial_cdf(7,prob_matrix[5][7]) * win_2_2_7 + binomial_cdf(7,prob_matrix[5][3]) * win_2_2_3 + binomial_cdf(7,prob_matrix[5][6]) * win_2_2_6)
    win_3_2 = win_2_2_2 * (binomial_cdf(7,prob_matrix[2][1]) * win_2_1_1 + binomial_cdf(7,prob_matrix[2][8]) * win_2_1_8 + binomial_cdf(7,prob_matrix[2][4]) * win_2_1_4 + binomial_cdf(7,prob_matrix[2][5]) * win_2_1_5)
    win_3_7 = win_2_2_7 * (binomial_cdf(7,prob_matrix[7][1]) * win_2_1_1 + binomial_cdf(7,prob_matrix[7][8]) * win_2_1_8 + binomial_cdf(7,prob_matrix[7][4]) * win_2_1_4 + binomial_cdf(7,prob_matrix[7][5]) * win_2_1_5)
    win_3_3 = win_2_2_3 * (binomial_cdf(7,prob_matrix[3][1]) * win_2_1_1 + binomial_cdf(7,prob_matrix[3][8]) * win_2_1_8 + binomial_cdf(7,prob_matrix[3][4]) * win_2_1_4 + binomial_cdf(7,prob_matrix[3][5]) * win_2_1_5)
    win_3_6 = win_2_2_6 * (binomial_cdf(7,prob_matrix[6][1]) * win_2_1_1 + binomial_cdf(7,prob_matrix[6][8]) * win_2_1_8 + binomial_cdf(7,prob_matrix[6][4]) * win_2_1_4 + binomial_cdf(7,prob_matrix[6][5]) * win_2_1_5)
    
    series_wins = {
        1 : [win_1_1_1,win_2_1_1,win_3_1],
        2 : [win_1_3_2,win_2_2_2,win_3_2],
        3 : [win_1_4_3,win_2_2_3,win_3_3],
        4 : [win_1_2_4,win_2_1_4,win_3_4],
        5 : [win_1_2_5,win_2_1_5,win_3_5],
        6 : [win_1_4_6,win_2_2_6,win_3_6],
        7 : [win_1_3_7,win_2_2_7,win_3_7],
        8 : [win_1_1_8,win_2_1_8,win_3_8]
    }
    
    for key,value in series_wins.items():
        value.append(0)
        for idx in range(3):
            value[3] += value[idx]
        
    return series_wins

def predict_wins_twice4_b07sf(teams):
    
    prob_matrix = win_probability_matrix(teams)
    
    # win_round_matchup_seed: probability of seed to win matchup of round
    
    win_1_1_1 = twice_to_beat_cdf(prob_matrix[1][8])
    win_1_1_8 = 1-win_1_1_1
    win_1_2_4 = twice_to_beat_cdf(prob_matrix[4][5])
    win_1_2_5 = 1-win_1_2_4
    win_1_3_2 = twice_to_beat_cdf(prob_matrix[2][7])
    win_1_3_7 = 1-win_1_3_2
    win_1_4_3 = twice_to_beat_cdf(prob_matrix[3][6])
    win_1_4_6 = 1-win_1_4_3
    
    win_2_1_1 = win_1_1_1 * (binomial_cdf(7,prob_matrix[1][4]) * win_1_2_4 + binomial_cdf(7,prob_matrix[1][5]) * win_1_2_5)
    win_2_1_8 = win_1_1_8 * (binomial_cdf(7,prob_matrix[8][4]) * win_1_2_4 + binomial_cdf(7,prob_matrix[8][5]) * win_1_2_5)
    win_2_1_4 = win_1_2_4 * (binomial_cdf(7,prob_matrix[4][1]) * win_1_1_1 + binomial_cdf(7,prob_matrix[4][8]) * win_1_1_8)
    win_2_1_5 = win_1_2_5 * (binomial_cdf(7,prob_matrix[5][1]) * win_1_1_1 + binomial_cdf(7,prob_matrix[5][8]) * win_1_1_8)
    win_2_2_2 = win_1_3_2 * (binomial_cdf(7,prob_matrix[2][3]) * win_1_4_3 + binomial_cdf(7,prob_matrix[2][6]) * win_1_4_6)
    win_2_2_7 = win_1_3_7 * (binomial_cdf(7,prob_matrix[7][3]) * win_1_4_3 + binomial_cdf(7,prob_matrix[7][6]) * win_1_4_6)
    win_2_2_3 = win_1_4_3 * (binomial_cdf(7,prob_matrix[3][2]) * win_1_3_2 + binomial_cdf(7,prob_matrix[3][7]) * win_1_3_7)
    win_2_2_6 = win_1_4_6 * (binomial_cdf(7,prob_matrix[6][2]) * win_1_3_2 + binomial_cdf(7,prob_matrix[6][7]) * win_1_3_7)
    
    win_3_1 = win_2_1_1 * (binomial_cdf(7,prob_matrix[1][2]) * win_2_2_2 + binomial_cdf(7,prob_matrix[1][7]) * win_2_2_7 + binomial_cdf(7,prob_matrix[1][3]) * win_2_2_3 + binomial_cdf(7,prob_matrix[1][6]) * win_2_2_6)
    win_3_8 = win_2_1_8 * (binomial_cdf(7,prob_matrix[8][2]) * win_2_2_2 + binomial_cdf(7,prob_matrix[8][7]) * win_2_2_7 + binomial_cdf(7,prob_matrix[8][3]) * win_2_2_3 + binomial_cdf(7,prob_matrix[8][6]) * win_2_2_6)
    win_3_4 = win_2_1_4 * (binomial_cdf(7,prob_matrix[4][2]) * win_2_2_2 + binomial_cdf(7,prob_matrix[4][7]) * win_2_2_7 + binomial_cdf(7,prob_matrix[4][3]) * win_2_2_3 + binomial_cdf(7,prob_matrix[4][6]) * win_2_2_6)
    win_3_5 = win_2_1_5 * (binomial_cdf(7,prob_matrix[5][2]) * win_2_2_2 + binomial_cdf(7,prob_matrix[5][7]) * win_2_2_7 + binomial_cdf(7,prob_matrix[5][3]) * win_2_2_3 + binomial_cdf(7,prob_matrix[5][6]) * win_2_2_6)
    win_3_2 = win_2_2_2 * (binomial_cdf(7,prob_matrix[2][1]) * win_2_1_1 + binomial_cdf(7,prob_matrix[2][8]) * win_2_1_8 + binomial_cdf(7,prob_matrix[2][4]) * win_2_1_4 + binomial_cdf(7,prob_matrix[2][5]) * win_2_1_5)
    win_3_7 = win_2_2_7 * (binomial_cdf(7,prob_matrix[7][1]) * win_2_1_1 + binomial_cdf(7,prob_matrix[7][8]) * win_2_1_8 + binomial_cdf(7,prob_matrix[7][4]) * win_2_1_4 + binomial_cdf(7,prob_matrix[7][5]) * win_2_1_5)
    win_3_3 = win_2_2_3 * (binomial_cdf(7,prob_matrix[3][1]) * win_2_1_1 + binomial_cdf(7,prob_matrix[3][8]) * win_2_1_8 + binomial_cdf(7,prob_matrix[3][4]) * win_2_1_4 + binomial_cdf(7,prob_matrix[3][5]) * win_2_1_5)
    win_3_6 = win_2_2_6 * (binomial_cdf(7,prob_matrix[6][1]) * win_2_1_1 + binomial_cdf(7,prob_matrix[6][8]) * win_2_1_8 + binomial_cdf(7,prob_matrix[6][4]) * win_2_1_4 + binomial_cdf(7,prob_matrix[6][5]) * win_2_1_5)
    
    series_wins = {
        1 : [win_1_1_1,win_2_1_1,win_3_1],
        2 : [win_1_3_2,win_2_2_2,win_3_2],
        3 : [win_1_4_3,win_2_2_3,win_3_3],
        4 : [win_1_2_4,win_2_1_4,win_3_4],
        5 : [win_1_2_5,win_2_1_5,win_3_5],
        6 : [win_1_4_6,win_2_2_6,win_3_6],
        7 : [win_1_3_7,win_2_2_7,win_3_7],
        8 : [win_1_1_8,win_2_1_8,win_3_8]
    }
    
    for key,value in series_wins.items():
        value.append(0)
        for idx in range(3):
            value[3] += value[idx]
    return series_wins