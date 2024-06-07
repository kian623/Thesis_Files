"""
to calculate per game changes and probabilites, as well as metrics
"""
import change
import tournament_utility
import numpy as np
    
def game(filename,k_factor,team_info,season,conference,round,write_csv,s = 400):
    data = {
        'season': season,
        'conference': conference,
        'round': round
    }
    
    games = tournament_utility.read_scores(filename) # read games from file
    
    win_probability = []
    
    for game in games:
        diff = game['score1'] - game['score2']
        
        game['starting elo1'] = team_info[game['name1']]
        game['starting elo2'] = team_info[game['name2']]
        
        # updating ratings
        if diff>0: # if team1 wins
            rating_change, expected_score = change.per_game(
                k_factor,
                game['starting elo1'],
                game['starting elo2'],
                diff
            )
            game['ending elo1'] = game['starting elo1'] + rating_change
            game['ending elo2'] = game['starting elo2'] - rating_change
        
        else: # if team2 wins
            rating_change, expected_score = change.per_game(
                k_factor,
                game['starting elo2'],
                game['starting elo1'],
                -diff
            )
            game['ending elo1'] = game['starting elo1'] - rating_change
            game['ending elo2'] = game['starting elo2'] + rating_change
        
        # record changes to ratings and record winner's probability to win
        win_probability.append(expected_score)
        team_info[game['name1']] = game['ending elo1']
        team_info[game['name2']] = game['ending elo2']
                
    tournament_utility.scores_add_new_elo(filename,games,write_csv) # set last parameter to True if we need to update ratings in xls files
    
    data['right prediction'] = sum(prob > 0.5 for prob in win_probability) # count number of games favored teams wins
    data['total games'] = sum(prob != 0.5 for prob in win_probability) # count number of games where there is a favored team
    data['all games'] = len(win_probability) # count all games
    data['brier'] = np.sum(np.square(np.ones(data['all games']) - win_probability))
    # sum of squared losses is calculated as follows:
    # 1. create vector(array) full of ones, with number of entries being equal to number of games
    # 2. subtract the win_probability vector from vector of 1s
    # 3. squared each entry, and find the sum of all the entries
    data['logloss'] = -np.sum(np.log(win_probability)) # sum of negative logarithm of win probabilities
    
    return data