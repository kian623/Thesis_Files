"""
for calculating round probabilities of each playoff team per conference
"""
import simulate_round
import playoffs_8teams2
import csv

def reset_rating(teams,revert,current = None,conference = None,SeparateRatingPreviousRevert = False,BackTo1500 = False):
    if current == None: # for models with one rating per team
        if BackTo1500 == False: # for cases when starting rating for a conference is based on previous rating
            for team,rating in teams.items():
                teams[team] = rating*revert + 1500 * (1-revert)
        else: # for resetting to 1500
            for team in teams.keys():
                teams[team] = 1500
    else: # for models with three ratings
        # two dictionaries for ratings, one for the ending rating of a team per conference and one is current ratings
        if SeparateRatingPreviousRevert == False: # for Split Elo Model
            for team,ratings in teams.items():
                current[team] = ratings[conference] * revert + 1500 * (1 - revert)
        else:
            for team,rating in teams.items(): # for Blended Elo Model
                current[team] = rating[conference] * revert['conference'] + current[team] * revert['previous'] + 1500 * (1 - revert['previous'] - revert['conference'])
                # revert['conference'] is C_T
                # revert['previous'] is C_P

def update_main_ratings(teams,current_ratings,conference):
    # to record a team's rating at the end of a conference for models with three ratings
    for key,value in current_ratings.items():
        teams[key][conference] = value

def change_name(old_name,new_name,teams,current_ratings):
    # for renaming teams
    teams[new_name] = teams.pop(old_name)
    current_ratings[new_name] = current_ratings.pop(old_name) # for SEM and BEM


# for probabilities per conference, edit if necessary
def results_computer(data):
    temp = [info['data'] for info in data if 'data' in info.keys()] # take data only at the end of elimination round
    results = []
    for result in temp:
        results += result.values()
    return results

def simulate_SameRating(parameters,write_csv = False):
    # parameters = {k_, revert_season, revert_conference}
    
    if 'k' in parameters.keys():
        parameters = {
                'k_filipino': int(parameters['k']),
                'k_import': int(parameters['k']),
                'revert_season': round(float(parameters['revert_season']),2),
                'revert_filipino': round(float(parameters['revert_conference']),2),
                'revert_import': round(float(parameters['revert_conference']),2)
        }
    
    # initialize teams
    
    teams = {
        'San Miguel' : 1500,
        'Ginebra' : 1500,
        'Alaska' : 1500,
        'Star' : 1500,
        'TNT' : 1500,
        'Phoenix' : 1500,
        'Rain or Shine' : 1500,
        'Meralco' : 1500,
        'Globalport' : 1500,
        'NLEX' : 1500,
        'Mahindra' : 1500,
        'Blackwater' : 1500
    }
    
    data = []
    
    # 2016-17 season
    
    # Philippine
    
    info = simulate_round.game(
        '2016-17/philippine/eliminations.csv',
        parameters['k_filipino'],
        teams,
        '2016-17','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['San Miguel'],
        2 : teams['Alaska'],
        3 : teams['Star'],
        4 : teams['TNT'],
        5 : teams['Globalport'],
        6 : teams['Phoenix'],
        7 : teams['Ginebra'],
        8 : teams['Rain or Shine'],
    }
    
    wins = {
        1 : 3,
        2 : 0,
        3 : 1,
        4 : 1,
        5 : 0,
        6 : 0,
        7 : 2,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2016-17/philippine/playoffs.csv',
        parameters['k_filipino'],
        teams,
        '2016-17','philippine','playoffs',write_csv
    )
    
    data.append(info)
    
    # Commissioner's
    
    reset_rating(teams,parameters['revert_filipino'])
    
    info = simulate_round.game(
        '2016-17/commissioner/eliminations.csv',
        parameters['k_import'],
        teams,
        '2016-17','commissioner','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['Ginebra'],
        2 : teams['San Miguel'],
        3 : teams['Star'],
        4 : teams['TNT'],
        5 : teams['Meralco'],
        6 : teams['Rain or Shine'],
        7 : teams['Phoenix'],
        8 : teams['Globalport']
    }
    
    wins = {
        1 : 1,
        2 : 3,
        3 : 1,
        4 : 2,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2016-17/commissioner/playoffs.csv',
        parameters['k_import'],
        teams,
        '2016-17','commissioner','playoffs',write_csv
    )
    
    data.append(info)
    
    # Governors'
    
    reset_rating(teams,parameters['revert_import'])
    teams['Kia'] = teams.pop('Mahindra')
    
    info = simulate_round.game(
        '2016-17/governors/eliminations.csv',
        parameters['k_import'],
        teams,
        '2016-17','governors','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['Meralco'],
        2 : teams['TNT'],
        3 : teams['Ginebra'],
        4 : teams['Star'],
        5 : teams['NLEX'],
        6 : teams['San Miguel'],
        7 : teams['Rain or Shine'],
        8 : teams['Blackwater']
    }
    
    wins = {
        1 : 2,
        2 : 1,
        3 : 3,
        4 : 1,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2016-17/governors/playoffs.csv',
        parameters['k_import'],
        teams,
        '2016-17','governors','playoffs',write_csv
    )
    
    data.append(info)
    
    # 2017-18 season
    
    # Philippine
    
    reset_rating(teams,parameters['revert_season'])
    teams['Magnolia'] = teams.pop('Star')
    
    info = simulate_round.game(
        '2017-18/philippine/eliminations.csv',
        parameters['k_filipino'],
        teams,
        '2017-18','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['San Miguel'],
        2 : teams['Magnolia'],
        3 : teams['Alaska'],
        4 : teams['Ginebra'],
        5 : teams['Rain or Shine'],
        6 : teams['NLEX'],
        7 : teams['Globalport'],
        8 : teams['TNT'],
    }
    
    wins = {
        1 : 3,
        2 : 2,
        3 : 0,
        4 : 1,
        5 : 0,
        6 : 1,
        7 : 0,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2017-18/philippine/playoffs.csv',
        parameters['k_filipino'],
        teams,
        '2017-18','philippine','playoffs',write_csv
    )
    
    data.append(info)
    
    # Commissioner's
    
    reset_rating(teams,parameters['revert_filipino'])
    teams['Columbian'] = teams.pop('Kia')
    
    info = simulate_round.game(
        '2017-18/commissioner/eliminations.csv',
        parameters['k_import'],
        teams,
        '2017-18','commissioner','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['Rain or Shine'],
        2 : teams['Alaska'],
        3 : teams['TNT'],
        4 : teams['Meralco'],
        5 : teams['Ginebra'],
        6 : teams['San Miguel'],
        7 : teams['Magnolia'],
        8 : teams['Globalport']
    }
    
    wins = {
        1 : 1,
        2 : 1,
        3 : 0,
        4 : 0,
        5 : 3,
        6 : 2,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2017-18/commissioner/playoffs.csv',
        parameters['k_import'],
        teams,
        '2017-18','commissioner','playoffs',write_csv
    )
    
    data.append(info)
    
    # Governors'
    
    reset_rating(teams,parameters['revert_import'])
    teams['NorthPort'] = teams.pop('Globalport')
    
    info = simulate_round.game(
        '2017-18/governors/eliminations.csv',
        parameters['k_import'],
        teams,
        '2017-18','governors','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['Ginebra'],
        2 : teams['Phoenix'],
        3 : teams['Alaska'],
        4 : teams['Magnolia'],
        5 : teams['Blackwater'],
        6 : teams['San Miguel'],
        7 : teams['Meralco'],
        8 : teams['NLEX']
    }
    
    wins = {
        1 : 1,
        2 : 0,
        3 : 2,
        4 : 3,
        5 : 0,
        6 : 0,
        7 : 1,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2017-18/governors/playoffs.csv',
        parameters['k_import'],
        teams,
        '2017-18','governors','playoffs',write_csv
    )
    
    data.append(info)
    
    # 2018-19 season
    
    # Philippine
    
    reset_rating(teams,parameters['revert_season'])
    
    info = simulate_round.game(
        '2018-19/philippine/eliminations.csv',
        parameters['k_filipino'],
        teams,
        '2018-19','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['Phoenix'],
        2 : teams['Rain or Shine'],
        3 : teams['Ginebra'],
        4 : teams['TNT'],
        5 : teams['San Miguel'],
        6 : teams['Magnolia'],
        7 : teams['NorthPort'],
        8 : teams['Alaska'],
    }
    
    wins = {
        1 : 1,
        2 : 1,
        3 : 0,
        4 : 0,
        5 : 3,
        6 : 2,
        7 : 0,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2018-19/philippine/playoffs.csv',
        parameters['k_filipino'],
        teams,
        '2018-19','philippine','playoffs',write_csv
    )
    
    data.append(info)
    
    # Commissioner's
    
    reset_rating(teams,parameters['revert_filipino'])
    
    info = simulate_round.game(
        '2018-19/commissioner/eliminations.csv',
        parameters['k_import'],
        teams,
        '2018-19','commissioner','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['TNT'],
        2 : teams['NorthPort'],
        3 : teams['Blackwater'],
        4 : teams['Ginebra'],
        5 : teams['Magnolia'],
        6 : teams['Rain or Shine'],
        7 : teams['San Miguel'],
        8 : teams['Alaska']
    }
    
    wins = {
        1 : 2,
        2 : 0,
        3 : 0,
        4 : 1,
        5 : 0,
        6 : 1,
        7 : 3,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2018-19/commissioner/playoffs.csv',
        parameters['k_import'],
        teams,
        '2018-19','commissioner','playoffs',write_csv
    )
    
    data.append(info)
    
    # Governors'
    
    reset_rating(teams,parameters['revert_import'])
    
    info = simulate_round.game(
        '2018-19/governors/eliminations.csv',
        parameters['k_import'],
        teams,
        '2018-19','governors','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['NLEX'],
        2 : teams['Meralco'],
        3 : teams['TNT'],
        4 : teams['Ginebra'],
        5 : teams['San Miguel'],
        6 : teams['Magnolia'],
        7 : teams['Alaska'],
        8 : teams['NorthPort']
    }
    
    wins = {
        1 : 0,
        2 : 2,
        3 : 1,
        4 : 3,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 1,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2018-19/governors/playoffs.csv',
        parameters['k_import'],
        teams,
        '2018-19','governors','playoffs',write_csv
    )
    
    data.append(info)
    
    # 2020 season
    
    # Philippine
    
    reset_rating(teams,parameters['revert_season'])
    teams['Terrafirma'] = teams.pop('Columbian')
    
    info = simulate_round.game(
        '2020/philippine/eliminations.csv',
        parameters['k_filipino'],
        teams,
        '2020','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['Ginebra'],
        2 : teams['Phoenix'],
        3 : teams['TNT'],
        4 : teams['San Miguel'],
        5 : teams['Meralco'],
        6 : teams['Alaska'],
        7 : teams['Magnolia'],
        8 : teams['Rain or Shine'],
    }
    
    wins = {
        1 : 3,
        2 : 1,
        3 : 2,
        4 : 0,
        5 : 1,
        6 : 0,
        7 : 0,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2020/philippine/playoffs.csv',
        parameters['k_filipino'],
        teams,
        '2020','philippine','playoffs',write_csv
    )
    
    data.append(info)
    
    # 2021 season
    
    # Philippine
    
    reset_rating(teams,parameters['revert_season'])
    
    info = simulate_round.game(
        '2021/philippine/eliminations.csv',
        parameters['k_filipino'],
        teams,
        '2021','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['TNT'],
        2 : teams['Meralco'],
        3 : teams['Magnolia'],
        4 : teams['San Miguel'],
        5 : teams['NorthPort'],
        6 : teams['Rain or Shine'],
        7 : teams['NLEX'],
        8 : teams['Ginebra'],
    }
    
    wins = {
        1 : 3,
        2 : 1,
        3 : 2,
        4 : 1,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2021/philippine/playoffs.csv',
        parameters['k_filipino'],
        teams,
        '2021','philippine','playoffs',write_csv
    )
    
    data.append(info)
    
    # Governors'
    
    reset_rating(teams,parameters['revert_filipino'])
    
    info = simulate_round.game(
        '2021/governors/eliminations.csv',
        parameters['k_import'],
        teams,
        '2021','governors','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['Magnolia'],
        2 : teams['NLEX'],
        3 : teams['TNT'],
        4 : teams['Meralco'],
        5 : teams['San Miguel'],
        6 : teams['Ginebra'],
        7 : teams['Alaska'],
        8 : teams['Phoenix']
    }
    
    wins = {
        1 : 1,
        2 : 1,
        3 : 0,
        4 : 2,
        5 : 0,
        6 : 3,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2021/governors/playoffs.csv',
        parameters['k_import'],
        teams,
        '2021','governors','playoffs',write_csv
    )
    
    data.append(info)
    
    # 2022-23 season
    
    # Philippine
    
    reset_rating(teams,parameters['revert_season'])
    teams['Converge'] = teams.pop('Alaska')
    
    info = simulate_round.game(
        '2022-23/philippine/eliminations.csv',
        parameters['k_filipino'],
        teams,
        '2022-23','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['San Miguel'],
        2 : teams['TNT'],
        3 : teams['Magnolia'],
        4 : teams['Ginebra'],
        5 : teams['Meralco'],
        6 : teams['NLEX'],
        7 : teams['Converge'],
        8 : teams['Blackwater'],
    }
    
    wins = {
        1 : 3,
        2 : 2,
        3 : 1,
        4 : 0,
        5 : 1,
        6 : 0,
        7 : 0,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2022-23/philippine/playoffs.csv',
        parameters['k_filipino'],
        teams,
        '2022-23','philippine','playoffs',write_csv
    )
    
    data.append(info)
    
    # Commissioner's
    
    reset_rating(teams,parameters['revert_filipino'])
    teams['Bay Area'] = 1500
    
    info = simulate_round.game(
        '2022-23/commissioner/eliminations.csv',
        parameters['k_import'],
        teams,
        '2022-23','commissioner','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['Bay Area'],
        2 : teams['Magnolia'],
        3 : teams['Ginebra'],
        4 : teams['Converge'],
        5 : teams['San Miguel'],
        6 : teams['NorthPort'],
        7 : teams['Phoenix'],
        8 : teams['Rain or Shine']
    }
    
    wins = {
        1 : 2,
        2 : 1,
        3 : 3,
        4 : 0,
        5 : 1,
        6 : 0,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2022-23/commissioner/playoffs.csv',
        parameters['k_import'],
        teams,
        '2022-23','commissioner','playoffs',write_csv
    )
    
    data.append(info)
    
    # Governors'
    
    reset_rating(teams,parameters['revert_import'])
    del teams['Bay Area']
    
    info = simulate_round.game(
        '2022-23/governors/eliminations.csv',
        parameters['k_import'],
        teams,
        '2022-23','governors','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['TNT'],
        2 : teams['San Miguel'],
        3 : teams['Ginebra'],
        4 : teams['Meralco'],
        5 : teams['Magnolia'],
        6 : teams['NLEX'],
        7 : teams['Converge'],
        8 : teams['Phoenix']
    }
    
    wins = {
        1 : 3,
        2 : 1,
        3 : 2,
        4 : 1,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2022-23/governors/playoffs.csv',
        parameters['k_import'],
        teams,
        '2022-23','governors','playoffs',write_csv
    )
    
    data.append(info)
    
    # 2023-24
    
    # Commissioner
    
    reset_rating(teams,parameters['revert_season'])
    
    info = simulate_round.game(
        '2023-24/commissioner/eliminations.csv',
        parameters['k_import'],
        teams,
        '2023-24','commissioner','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['Magnolia'],
        2 : teams['San Miguel'],
        3 : teams['Ginebra'],
        4 : teams['Phoenix'],
        5 : teams['Meralco'],
        6 : teams['NorthPort'],
        7 : teams['Rain or Shine'],
        8 : teams['TNT']
    }
    wins = {
        1 : 2,
        2 : 3,
        3 : 1,
        4 : 1,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    data.append(info)
    
    info = simulate_round.game(
        '2023-24/commissioner/playoffs.csv',
        parameters['k_import'],
        teams,
        '2023-24','commissioner','playoffs',write_csv
    )
    data.append(info)
    
    # Philippine
    
    reset_rating(teams,parameters['revert_filipino'])
    
    info = simulate_round.game(
        '2023-24/philippine/eliminations.csv',
        parameters['k_filipino'],
        teams,
        '2023-24','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['San Miguel'],
        2 : teams['Ginebra'],
        3 : teams['Meralco'],
        4 : teams['TNT'],
        5 : teams['Rain or Shine'],
        6 : teams['NLEX'],
        7 : teams['Magnolia'],
        8 : teams['Terrafirma'],
    }
    
    # wins = {
        # 1 : 3,
        # 2 : 2,
        # 3 : 1,
        # 4 : 0,
        # 5 : 1,
        # 6 : 0,
        # 7 : 0,
        # 8 : 0
    # }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)
    
    data.append(info)
    
    # info = simulate_round.game(
        # '2023-24/philippine/playoffs.csv',
        # parameters['k_filipino'],
        # teams,
        # '2023-24','philippine','playoffs',write_csv
    # )
    
    # data.append(info)
    
    with open('Playoffs/modified_silver.csv','w',newline='') as file:
        writer = csv.writer(file)
        writer.writerows(results_computer(data))

def simulate_SameRating_BackTo1500Yearly(parameters,write_csv = False):
    # parameters = {k_filipino, k_import, revert_season, revert_filipino, revert_import}
    
    if 'k' in parameters.keys():
        parameters = {
                'k_filipino': int(parameters['k']),
                'k_import': int(parameters['k']),
                'revert_season': round(float(parameters['revert']),2),
                'revert_filipino': round(float(parameters['revert']),2),
                'revert_import': round(float(parameters['revert']),2)
        }
    
    # initialize teams
    
    teams = {
        'San Miguel' : 1500,
        'Ginebra' : 1500,
        'Alaska' : 1500,
        'Star' : 1500,
        'TNT' : 1500,
        'Phoenix' : 1500,
        'Rain or Shine' : 1500,
        'Meralco' : 1500,
        'Globalport' : 1500,
        'NLEX' : 1500,
        'Mahindra' : 1500,
        'Blackwater' : 1500
    }
    
    data = []
    
    # 2016-17 season
    
    # Philippine
    
    info = simulate_round.game(
        '2016-17/philippine/eliminations.csv',
        parameters['k_filipino'],
        teams,
        '2016-17','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['San Miguel'],
        2 : teams['Alaska'],
        3 : teams['Star'],
        4 : teams['TNT'],
        5 : teams['Globalport'],
        6 : teams['Phoenix'],
        7 : teams['Ginebra'],
        8 : teams['Rain or Shine'],
    }
    
    wins = {
        1 : 3,
        2 : 0,
        3 : 1,
        4 : 1,
        5 : 0,
        6 : 0,
        7 : 2,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)
    
    
    data.append(info)
    
    info = simulate_round.game(
        '2016-17/philippine/playoffs.csv',
        parameters['k_filipino'],
        teams,
        '2016-17','philippine','playoffs',write_csv
    )
    
    data.append(info)
    
    # Commissioner's
    
    reset_rating(teams,parameters['revert_filipino'])
    
    info = simulate_round.game(
        '2016-17/commissioner/eliminations.csv',
        parameters['k_import'],
        teams,
        '2016-17','commissioner','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['Ginebra'],
        2 : teams['San Miguel'],
        3 : teams['Star'],
        4 : teams['TNT'],
        5 : teams['Meralco'],
        6 : teams['Rain or Shine'],
        7 : teams['Phoenix'],
        8 : teams['Globalport']
    }
    
    wins = {
        1 : 1,
        2 : 3,
        3 : 1,
        4 : 2,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2016-17/commissioner/playoffs.csv',
        parameters['k_import'],
        teams,
        '2016-17','commissioner','playoffs',write_csv
    )
    
    data.append(info)
    
    # Governors'
    
    reset_rating(teams,parameters['revert_import'])
    teams['Kia'] = teams.pop('Mahindra')
    
    info = simulate_round.game(
        '2016-17/governors/eliminations.csv',
        parameters['k_import'],
        teams,
        '2016-17','governors','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['Meralco'],
        2 : teams['TNT'],
        3 : teams['Ginebra'],
        4 : teams['Star'],
        5 : teams['NLEX'],
        6 : teams['San Miguel'],
        7 : teams['Rain or Shine'],
        8 : teams['Blackwater']
    }
    
    wins = {
        1 : 2,
        2 : 1,
        3 : 3,
        4 : 1,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2016-17/governors/playoffs.csv',
        parameters['k_import'],
        teams,
        '2016-17','governors','playoffs',write_csv
    )
    
    data.append(info)
    
    # 2017-18 season
    
    # Philippine
    
    reset_rating(teams,parameters['revert_season'],BackTo1500 = True)
    teams['Magnolia'] = teams.pop('Star')
    
    info = simulate_round.game(
        '2017-18/philippine/eliminations.csv',
        parameters['k_filipino'],
        teams,
        '2017-18','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['San Miguel'],
        2 : teams['Magnolia'],
        3 : teams['Alaska'],
        4 : teams['Ginebra'],
        5 : teams['Rain or Shine'],
        6 : teams['NLEX'],
        7 : teams['Globalport'],
        8 : teams['TNT'],
    }
    
    wins = {
        1 : 3,
        2 : 2,
        3 : 0,
        4 : 1,
        5 : 0,
        6 : 1,
        7 : 0,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2017-18/philippine/playoffs.csv',
        parameters['k_filipino'],
        teams,
        '2017-18','philippine','playoffs',write_csv
    )
    
    data.append(info)
    
    # Commissioner's
    
    reset_rating(teams,parameters['revert_filipino'])
    teams['Columbian'] = teams.pop('Kia')
    
    info = simulate_round.game(
        '2017-18/commissioner/eliminations.csv',
        parameters['k_import'],
        teams,
        '2017-18','commissioner','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['Rain or Shine'],
        2 : teams['Alaska'],
        3 : teams['TNT'],
        4 : teams['Meralco'],
        5 : teams['Ginebra'],
        6 : teams['San Miguel'],
        7 : teams['Magnolia'],
        8 : teams['Globalport']
    }
    
    wins = {
        1 : 1,
        2 : 1,
        3 : 0,
        4 : 0,
        5 : 3,
        6 : 2,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2017-18/commissioner/playoffs.csv',
        parameters['k_import'],
        teams,
        '2017-18','commissioner','playoffs',write_csv
    )
    
    data.append(info)
    
    # Governors'
    
    reset_rating(teams,parameters['revert_import'])
    teams['NorthPort'] = teams.pop('Globalport')
    
    info = simulate_round.game(
        '2017-18/governors/eliminations.csv',
        parameters['k_import'],
        teams,
        '2017-18','governors','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['Ginebra'],
        2 : teams['Phoenix'],
        3 : teams['Alaska'],
        4 : teams['Magnolia'],
        5 : teams['Blackwater'],
        6 : teams['San Miguel'],
        7 : teams['Meralco'],
        8 : teams['NLEX']
    }
    
    wins = {
        1 : 1,
        2 : 0,
        3 : 2,
        4 : 3,
        5 : 0,
        6 : 0,
        7 : 1,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2017-18/governors/playoffs.csv',
        parameters['k_import'],
        teams,
        '2017-18','governors','playoffs',write_csv
    )
    
    data.append(info)
    
    # 2018-19 season
    
    # Philippine
    
    reset_rating(teams,parameters['revert_season'],BackTo1500 = True)
    
    info = simulate_round.game(
        '2018-19/philippine/eliminations.csv',
        parameters['k_filipino'],
        teams,
        '2018-19','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['Phoenix'],
        2 : teams['Rain or Shine'],
        3 : teams['Ginebra'],
        4 : teams['TNT'],
        5 : teams['San Miguel'],
        6 : teams['Magnolia'],
        7 : teams['NorthPort'],
        8 : teams['Alaska'],
    }
    
    wins = {
        1 : 1,
        2 : 1,
        3 : 0,
        4 : 0,
        5 : 3,
        6 : 2,
        7 : 0,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2018-19/philippine/playoffs.csv',
        parameters['k_filipino'],
        teams,
        '2018-19','philippine','playoffs',write_csv
    )
    
    data.append(info)
    
    # Commissioner's
    
    reset_rating(teams,parameters['revert_filipino'])
    
    info = simulate_round.game(
        '2018-19/commissioner/eliminations.csv',
        parameters['k_import'],
        teams,
        '2018-19','commissioner','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['TNT'],
        2 : teams['NorthPort'],
        3 : teams['Blackwater'],
        4 : teams['Ginebra'],
        5 : teams['Magnolia'],
        6 : teams['Rain or Shine'],
        7 : teams['San Miguel'],
        8 : teams['Alaska']
    }
    
    wins = {
        1 : 2,
        2 : 0,
        3 : 0,
        4 : 1,
        5 : 0,
        6 : 1,
        7 : 3,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2018-19/commissioner/playoffs.csv',
        parameters['k_import'],
        teams,
        '2018-19','commissioner','playoffs',write_csv
    )
    
    data.append(info)
    
    # Governors'
    
    reset_rating(teams,parameters['revert_import'])
    
    info = simulate_round.game(
        '2018-19/governors/eliminations.csv',
        parameters['k_import'],
        teams,
        '2018-19','governors','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['NLEX'],
        2 : teams['Meralco'],
        3 : teams['TNT'],
        4 : teams['Ginebra'],
        5 : teams['San Miguel'],
        6 : teams['Magnolia'],
        7 : teams['Alaska'],
        8 : teams['NorthPort']
    }
    
    wins = {
        1 : 0,
        2 : 2,
        3 : 1,
        4 : 3,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 1,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2018-19/governors/playoffs.csv',
        parameters['k_import'],
        teams,
        '2018-19','governors','playoffs',write_csv
    )
    
    data.append(info)
    
    # 2020 season
    
    # Philippine
    
    reset_rating(teams,parameters['revert_season'],BackTo1500 = True)
    teams['Terrafirma'] = teams.pop('Columbian')
    
    info = simulate_round.game(
        '2020/philippine/eliminations.csv',
        parameters['k_filipino'],
        teams,
        '2020','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['Ginebra'],
        2 : teams['Phoenix'],
        3 : teams['TNT'],
        4 : teams['San Miguel'],
        5 : teams['Meralco'],
        6 : teams['Alaska'],
        7 : teams['Magnolia'],
        8 : teams['Rain or Shine'],
    }
    
    wins = {
        1 : 3,
        2 : 1,
        3 : 2,
        4 : 0,
        5 : 1,
        6 : 0,
        7 : 0,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2020/philippine/playoffs.csv',
        parameters['k_filipino'],
        teams,
        '2020','philippine','playoffs',write_csv
    )
    
    data.append(info)
    
    # 2021 season
    
    # Philippine
    
    reset_rating(teams,parameters['revert_season'],BackTo1500 = True)
    
    info = simulate_round.game(
        '2021/philippine/eliminations.csv',
        parameters['k_filipino'],
        teams,
        '2021','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['TNT'],
        2 : teams['Meralco'],
        3 : teams['Magnolia'],
        4 : teams['San Miguel'],
        5 : teams['NorthPort'],
        6 : teams['Rain or Shine'],
        7 : teams['NLEX'],
        8 : teams['Ginebra'],
    }
    
    wins = {
        1 : 3,
        2 : 1,
        3 : 2,
        4 : 1,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2021/philippine/playoffs.csv',
        parameters['k_filipino'],
        teams,
        '2021','philippine','playoffs',write_csv
    )
    
    data.append(info)
    
    # Governors'
    
    reset_rating(teams,parameters['revert_filipino'])
    
    info = simulate_round.game(
        '2021/governors/eliminations.csv',
        parameters['k_import'],
        teams,
        '2021','governors','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['Magnolia'],
        2 : teams['NLEX'],
        3 : teams['TNT'],
        4 : teams['Meralco'],
        5 : teams['San Miguel'],
        6 : teams['Ginebra'],
        7 : teams['Alaska'],
        8 : teams['Phoenix']
    }
    
    wins = {
        1 : 1,
        2 : 1,
        3 : 0,
        4 : 2,
        5 : 0,
        6 : 3,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2021/governors/playoffs.csv',
        parameters['k_import'],
        teams,
        '2021','governors','playoffs',write_csv
    )
    
    data.append(info)
    
    # 2022-23 season
    
    # Philippine
    
    reset_rating(teams,parameters['revert_season'], BackTo1500 = True)
    teams['Converge'] = teams.pop('Alaska')
    
    info = simulate_round.game(
        '2022-23/philippine/eliminations.csv',
        parameters['k_filipino'],
        teams,
        '2022-23','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['San Miguel'],
        2 : teams['TNT'],
        3 : teams['Magnolia'],
        4 : teams['Ginebra'],
        5 : teams['Meralco'],
        6 : teams['NLEX'],
        7 : teams['Converge'],
        8 : teams['Blackwater'],
    }
    
    wins = {
        1 : 3,
        2 : 2,
        3 : 1,
        4 : 0,
        5 : 1,
        6 : 0,
        7 : 0,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2022-23/philippine/playoffs.csv',
        parameters['k_filipino'],
        teams,
        '2022-23','philippine','playoffs',write_csv
    )
    
    data.append(info)
    
    # Commissioner's
    
    reset_rating(teams,parameters['revert_filipino'])
    teams['Bay Area'] = 1500
    
    info = simulate_round.game(
        '2022-23/commissioner/eliminations.csv',
        parameters['k_import'],
        teams,
        '2022-23','commissioner','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['Bay Area'],
        2 : teams['Magnolia'],
        3 : teams['Ginebra'],
        4 : teams['Converge'],
        5 : teams['San Miguel'],
        6 : teams['NorthPort'],
        7 : teams['Phoenix'],
        8 : teams['Rain or Shine']
    }
    
    wins = {
        1 : 2,
        2 : 1,
        3 : 3,
        4 : 0,
        5 : 1,
        6 : 0,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2022-23/commissioner/playoffs.csv',
        parameters['k_import'],
        teams,
        '2022-23','commissioner','playoffs',write_csv
    )
    
    data.append(info)
    
    # Governors'
    
    reset_rating(teams,parameters['revert_import'])
    del teams['Bay Area']
    
    info = simulate_round.game(
        '2022-23/governors/eliminations.csv',
        parameters['k_import'],
        teams,
        '2022-23','governors','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['TNT'],
        2 : teams['San Miguel'],
        3 : teams['Ginebra'],
        4 : teams['Meralco'],
        5 : teams['Magnolia'],
        6 : teams['NLEX'],
        7 : teams['Converge'],
        8 : teams['Phoenix']
    }
    
    wins = {
        1 : 3,
        2 : 1,
        3 : 2,
        4 : 1,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2022-23/governors/playoffs.csv',
        parameters['k_import'],
        teams,
        '2022-23','governors','playoffs',write_csv
    )
    
    data.append(info)
    
    # 2023-24
    
    # Commissioner
    
    reset_rating(teams,parameters['revert_season'],BackTo1500 = True)
    
    info = simulate_round.game(
        '2023-24/commissioner/eliminations.csv',
        parameters['k_import'],
        teams,
        '2023-24','commissioner','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['Magnolia'],
        2 : teams['San Miguel'],
        3 : teams['Ginebra'],
        4 : teams['Phoenix'],
        5 : teams['Meralco'],
        6 : teams['NorthPort'],
        7 : teams['Rain or Shine'],
        8 : teams['TNT']
    }
    wins = {
        1 : 2,
        2 : 3,
        3 : 1,
        4 : 1,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    data.append(info)
    
    info = simulate_round.game(
        '2023-24/commissioner/playoffs.csv',
        parameters['k_import'],
        teams,
        '2023-24','commissioner','playoffs',write_csv
    )
    data.append(info)
    
    # Philippine
    
    reset_rating(teams,parameters['revert_filipino'])
    
    info = simulate_round.game(
        '2023-24/philippine/eliminations.csv',
        parameters['k_filipino'],
        teams,
        '2023-24','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['San Miguel'],
        2 : teams['Ginebra'],
        3 : teams['Meralco'],
        4 : teams['TNT'],
        5 : teams['Rain or Shine'],
        6 : teams['NLEX'],
        7 : teams['Magnolia'],
        8 : teams['Terrafirma'],
    }
    
    # wins = {
        # 1 : 3,
        # 2 : 2,
        # 3 : 1,
        # 4 : 0,
        # 5 : 1,
        # 6 : 0,
        # 7 : 0,
        # 8 : 0
    # }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)
    
    data.append(info)
    
    # info = simulate_round.game(
        # '2023-24/philippine/playoffs.csv',
        # parameters['k_filipino'],
        # teams,
        # '2023-24','philippine','playoffs',write_csv
    # )
    
    # data.append(info)
    
    with open('Playoffs/season_reset.csv','w',newline='') as file:
        writer = csv.writer(file)
        writer.writerows(results_computer(data))

def simulate_SameRating_BackTo1500(parameters,write_csv = False):
    # parameters = {k_filipino, k_import, revert_season, revert_filipino, revert_import}
    
    if 'k' in parameters.keys():
        parameters = {
                'k_filipino': int(parameters['k']),
                'k_import': int(parameters['k']),
                'revert_season': 0,
                'revert_filipino': 0,
                'revert_import': 0
        }
    
    # initialize teams
    
    teams = {
        'San Miguel' : 1500,
        'Ginebra' : 1500,
        'Alaska' : 1500,
        'Star' : 1500,
        'TNT' : 1500,
        'Phoenix' : 1500,
        'Rain or Shine' : 1500,
        'Meralco' : 1500,
        'Globalport' : 1500,
        'NLEX' : 1500,
        'Mahindra' : 1500,
        'Blackwater' : 1500
    }
    
    data = []
    
    # 2016-17 season
    
    # Philippine
    
    info = simulate_round.game(
        '2016-17/philippine/eliminations.csv',
        parameters['k_filipino'],
        teams,
        '2016-17','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['San Miguel'],
        2 : teams['Alaska'],
        3 : teams['Star'],
        4 : teams['TNT'],
        5 : teams['Globalport'],
        6 : teams['Phoenix'],
        7 : teams['Ginebra'],
        8 : teams['Rain or Shine'],
    }
    
    wins = {
        1 : 3,
        2 : 0,
        3 : 1,
        4 : 1,
        5 : 0,
        6 : 0,
        7 : 2,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)\
    
    data.append(info)
    
    info = simulate_round.game(
        '2016-17/philippine/playoffs.csv',
        parameters['k_filipino'],
        teams,
        '2016-17','philippine','playoffs',write_csv
    )
    
    data.append(info)
    
    # Commissioner's
    
    reset_rating(teams,parameters['revert_filipino'],BackTo1500 = True)
    
    info = simulate_round.game(
        '2016-17/commissioner/eliminations.csv',
        parameters['k_import'],
        teams,
        '2016-17','commissioner','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['Ginebra'],
        2 : teams['San Miguel'],
        3 : teams['Star'],
        4 : teams['TNT'],
        5 : teams['Meralco'],
        6 : teams['Rain or Shine'],
        7 : teams['Phoenix'],
        8 : teams['Globalport']
    }
    
    wins = {
        1 : 1,
        2 : 3,
        3 : 1,
        4 : 2,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2016-17/commissioner/playoffs.csv',
        parameters['k_import'],
        teams,
        '2016-17','commissioner','playoffs',write_csv
    )
    
    data.append(info)
    
    # Governors'
    
    reset_rating(teams,parameters['revert_import'],BackTo1500 = True)
    teams['Kia'] = teams.pop('Mahindra')
    
    info = simulate_round.game(
        '2016-17/governors/eliminations.csv',
        parameters['k_import'],
        teams,
        '2016-17','governors','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['Meralco'],
        2 : teams['TNT'],
        3 : teams['Ginebra'],
        4 : teams['Star'],
        5 : teams['NLEX'],
        6 : teams['San Miguel'],
        7 : teams['Rain or Shine'],
        8 : teams['Blackwater']
    }
    
    wins = {
        1 : 2,
        2 : 1,
        3 : 3,
        4 : 1,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2016-17/governors/playoffs.csv',
        parameters['k_import'],
        teams,
        '2016-17','governors','playoffs',write_csv
    )
    
    data.append(info)
    
    # 2017-18 season
    
    # Philippine
    
    reset_rating(teams,parameters['revert_season'],BackTo1500 = True)
    teams['Magnolia'] = teams.pop('Star')
    
    info = simulate_round.game(
        '2017-18/philippine/eliminations.csv',
        parameters['k_filipino'],
        teams,
        '2017-18','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['San Miguel'],
        2 : teams['Magnolia'],
        3 : teams['Alaska'],
        4 : teams['Ginebra'],
        5 : teams['Rain or Shine'],
        6 : teams['NLEX'],
        7 : teams['Globalport'],
        8 : teams['TNT'],
    }
    
    wins = {
        1 : 3,
        2 : 2,
        3 : 0,
        4 : 1,
        5 : 0,
        6 : 1,
        7 : 0,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2017-18/philippine/playoffs.csv',
        parameters['k_filipino'],
        teams,
        '2017-18','philippine','playoffs',write_csv
    )
    
    data.append(info)
    
    # Commissioner's
    
    reset_rating(teams,parameters['revert_filipino'],BackTo1500 = True)
    teams['Columbian'] = teams.pop('Kia')
    
    info = simulate_round.game(
        '2017-18/commissioner/eliminations.csv',
        parameters['k_import'],
        teams,
        '2017-18','commissioner','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['Rain or Shine'],
        2 : teams['Alaska'],
        3 : teams['TNT'],
        4 : teams['Meralco'],
        5 : teams['Ginebra'],
        6 : teams['San Miguel'],
        7 : teams['Magnolia'],
        8 : teams['Globalport']
    }
    
    wins = {
        1 : 1,
        2 : 1,
        3 : 0,
        4 : 0,
        5 : 3,
        6 : 2,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b05sf(ranking)
    data.append(info)
    
    info = simulate_round.game(
        '2017-18/commissioner/playoffs.csv',
        parameters['k_import'],
        teams,
        '2017-18','commissioner','playoffs',write_csv
    )
    
    data.append(info)
    
    # Governors'
    
    reset_rating(teams,parameters['revert_import'],BackTo1500 = True)
    teams['NorthPort'] = teams.pop('Globalport')
    
    info = simulate_round.game(
        '2017-18/governors/eliminations.csv',
        parameters['k_import'],
        teams,
        '2017-18','governors','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['Ginebra'],
        2 : teams['Phoenix'],
        3 : teams['Alaska'],
        4 : teams['Magnolia'],
        5 : teams['Blackwater'],
        6 : teams['San Miguel'],
        7 : teams['Meralco'],
        8 : teams['NLEX']
    }
    
    wins = {
        1 : 1,
        2 : 0,
        3 : 2,
        4 : 3,
        5 : 0,
        6 : 0,
        7 : 1,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2017-18/governors/playoffs.csv',
        parameters['k_import'],
        teams,
        '2017-18','governors','playoffs',write_csv
    )
    
    data.append(info)
    
    # 2018-19 season
    
    # Philippine
    
    reset_rating(teams,parameters['revert_season'],BackTo1500 = True)
    
    info = simulate_round.game(
        '2018-19/philippine/eliminations.csv',
        parameters['k_filipino'],
        teams,
        '2018-19','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['Phoenix'],
        2 : teams['Rain or Shine'],
        3 : teams['Ginebra'],
        4 : teams['TNT'],
        5 : teams['San Miguel'],
        6 : teams['Magnolia'],
        7 : teams['NorthPort'],
        8 : teams['Alaska'],
    }
    
    wins = {
        1 : 1,
        2 : 1,
        3 : 0,
        4 : 0,
        5 : 3,
        6 : 2,
        7 : 0,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2018-19/philippine/playoffs.csv',
        parameters['k_filipino'],
        teams,
        '2018-19','philippine','playoffs',write_csv
    )
    
    data.append(info)
    
    # Commissioner's
    
    reset_rating(teams,parameters['revert_filipino'],BackTo1500 = True)
    
    info = simulate_round.game(
        '2018-19/commissioner/eliminations.csv',
        parameters['k_import'],
        teams,
        '2018-19','commissioner','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['TNT'],
        2 : teams['NorthPort'],
        3 : teams['Blackwater'],
        4 : teams['Ginebra'],
        5 : teams['Magnolia'],
        6 : teams['Rain or Shine'],
        7 : teams['San Miguel'],
        8 : teams['Alaska']
    }
    
    wins = {
        1 : 2,
        2 : 0,
        3 : 0,
        4 : 1,
        5 : 0,
        6 : 1,
        7 : 3,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2018-19/commissioner/playoffs.csv',
        parameters['k_import'],
        teams,
        '2018-19','commissioner','playoffs',write_csv
    )
    
    data.append(info)
    
    # Governors'
    
    reset_rating(teams,parameters['revert_import'],BackTo1500 = True)
    
    info = simulate_round.game(
        '2018-19/governors/eliminations.csv',
        parameters['k_import'],
        teams,
        '2018-19','governors','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['NLEX'],
        2 : teams['Meralco'],
        3 : teams['TNT'],
        4 : teams['Ginebra'],
        5 : teams['San Miguel'],
        6 : teams['Magnolia'],
        7 : teams['Alaska'],
        8 : teams['NorthPort']
    }
    
    wins = {
        1 : 0,
        2 : 2,
        3 : 1,
        4 : 3,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 1,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2018-19/governors/playoffs.csv',
        parameters['k_import'],
        teams,
        '2018-19','governors','playoffs',write_csv
    )
    
    data.append(info)
    
    # 2020 season
    
    # Philippine
    
    reset_rating(teams,parameters['revert_season'],BackTo1500 = True)
    teams['Terrafirma'] = teams.pop('Columbian')
    
    info = simulate_round.game(
        '2020/philippine/eliminations.csv',
        parameters['k_filipino'],
        teams,
        '2020','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['Ginebra'],
        2 : teams['Phoenix'],
        3 : teams['TNT'],
        4 : teams['San Miguel'],
        5 : teams['Meralco'],
        6 : teams['Alaska'],
        7 : teams['Magnolia'],
        8 : teams['Rain or Shine'],
    }
    
    wins = {
        1 : 3,
        2 : 1,
        3 : 2,
        4 : 0,
        5 : 1,
        6 : 0,
        7 : 0,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2020/philippine/playoffs.csv',
        parameters['k_filipino'],
        teams,
        '2020','philippine','playoffs',write_csv
    )
    
    data.append(info)
    
    # 2021 season
    
    # Philippine
    
    reset_rating(teams,parameters['revert_season'],BackTo1500 = True)
    
    info = simulate_round.game(
        '2021/philippine/eliminations.csv',
        parameters['k_filipino'],
        teams,
        '2021','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['TNT'],
        2 : teams['Meralco'],
        3 : teams['Magnolia'],
        4 : teams['San Miguel'],
        5 : teams['NorthPort'],
        6 : teams['Rain or Shine'],
        7 : teams['NLEX'],
        8 : teams['Ginebra'],
    }
    
    wins = {
        1 : 3,
        2 : 1,
        3 : 2,
        4 : 1,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2021/philippine/playoffs.csv',
        parameters['k_filipino'],
        teams,
        '2021','philippine','playoffs',write_csv
    )
    
    data.append(info)
    
    # Governors'
    
    reset_rating(teams,parameters['revert_filipino'],BackTo1500 = True)
    
    info = simulate_round.game(
        '2021/governors/eliminations.csv',
        parameters['k_import'],
        teams,
        '2021','governors','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['Magnolia'],
        2 : teams['NLEX'],
        3 : teams['TNT'],
        4 : teams['Meralco'],
        5 : teams['San Miguel'],
        6 : teams['Ginebra'],
        7 : teams['Alaska'],
        8 : teams['Phoenix']
    }
    
    wins = {
        1 : 1,
        2 : 1,
        3 : 0,
        4 : 2,
        5 : 0,
        6 : 3,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2021/governors/playoffs.csv',
        parameters['k_import'],
        teams,
        '2021','governors','playoffs',write_csv
    )
    
    data.append(info)
    
    # 2022-23 season
    
    # Philippine
    
    reset_rating(teams,parameters['revert_season'],BackTo1500 = True)
    teams['Converge'] = teams.pop('Alaska')
    
    info = simulate_round.game(
        '2022-23/philippine/eliminations.csv',
        parameters['k_filipino'],
        teams,
        '2022-23','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['San Miguel'],
        2 : teams['TNT'],
        3 : teams['Magnolia'],
        4 : teams['Ginebra'],
        5 : teams['Meralco'],
        6 : teams['NLEX'],
        7 : teams['Converge'],
        8 : teams['Blackwater'],
    }
    
    wins = {
        1 : 3,
        2 : 2,
        3 : 1,
        4 : 0,
        5 : 1,
        6 : 0,
        7 : 0,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2022-23/philippine/playoffs.csv',
        parameters['k_filipino'],
        teams,
        '2022-23','philippine','playoffs',write_csv
    )
    
    data.append(info)
    
    # Commissioner's
    
    reset_rating(teams,parameters['revert_filipino'],BackTo1500 = True)
    teams['Bay Area'] = 1500
    
    info = simulate_round.game(
        '2022-23/commissioner/eliminations.csv',
        parameters['k_import'],
        teams,
        '2022-23','commissioner','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['Bay Area'],
        2 : teams['Magnolia'],
        3 : teams['Ginebra'],
        4 : teams['Converge'],
        5 : teams['San Miguel'],
        6 : teams['NorthPort'],
        7 : teams['Phoenix'],
        8 : teams['Rain or Shine']
    }
    
    wins = {
        1 : 2,
        2 : 1,
        3 : 3,
        4 : 0,
        5 : 1,
        6 : 0,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2022-23/commissioner/playoffs.csv',
        parameters['k_import'],
        teams,
        '2022-23','commissioner','playoffs',write_csv
    )
    
    data.append(info)
    
    # Governors'
    
    reset_rating(teams,parameters['revert_import'],BackTo1500 = True)
    del teams['Bay Area']
    
    info = simulate_round.game(
        '2022-23/governors/eliminations.csv',
        parameters['k_import'],
        teams,
        '2022-23','governors','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['TNT'],
        2 : teams['San Miguel'],
        3 : teams['Ginebra'],
        4 : teams['Meralco'],
        5 : teams['Magnolia'],
        6 : teams['NLEX'],
        7 : teams['Converge'],
        8 : teams['Phoenix']
    }
    
    wins = {
        1 : 3,
        2 : 1,
        3 : 2,
        4 : 1,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2022-23/governors/playoffs.csv',
        parameters['k_import'],
        teams,
        '2022-23','governors','playoffs',write_csv
    )
    
    data.append(info)
    
    # 2023-24
    
    # Commissioner
    
    reset_rating(teams,parameters['revert_import'],BackTo1500 = True)
    
    info = simulate_round.game(
        '2023-24/commissioner/eliminations.csv',
        parameters['k_import'],
        teams,
        '2023-24','commissioner','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['Magnolia'],
        2 : teams['San Miguel'],
        3 : teams['Ginebra'],
        4 : teams['Phoenix'],
        5 : teams['Meralco'],
        6 : teams['NorthPort'],
        7 : teams['Rain or Shine'],
        8 : teams['TNT']
    }
    wins = {
        1 : 2,
        2 : 3,
        3 : 1,
        4 : 1,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    data.append(info)
    
    info = simulate_round.game(
        '2023-24/commissioner/playoffs.csv',
        parameters['k_import'],
        teams,
        '2023-24','commissioner','playoffs',write_csv
    )
    data.append(info)
    
    # Philippine
    
    reset_rating(teams,parameters['revert_filipino'],BackTo1500 = True)
    
    info = simulate_round.game(
        '2023-24/philippine/eliminations.csv',
        parameters['k_filipino'],
        teams,
        '2023-24','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : teams['San Miguel'],
        2 : teams['Ginebra'],
        3 : teams['Meralco'],
        4 : teams['TNT'],
        5 : teams['Rain or Shine'],
        6 : teams['NLEX'],
        7 : teams['Magnolia'],
        8 : teams['Terrafirma'],
    }
    
    # wins = {
        # 1 : 3,
        # 2 : 2,
        # 3 : 1,
        # 4 : 0,
        # 5 : 1,
        # 6 : 0,
        # 7 : 0,
        # 8 : 0
    # }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)
    
    data.append(info)
    
    # info = simulate_round.game(
        # '2023-24/philippine/playoffs.csv',
        # parameters['k_filipino'],
        # teams,
        # '2023-24','philippine','playoffs',write_csv
    # )
    
    # data.append(info)
    
    with open('Playoffs/conference_reset.csv','w',newline='') as file:
        writer = csv.writer(file)
        writer.writerows(results_computer(data))

def simulate_SeparateRating(parameters,write_csv = False):
    # parameters = {k, revert}
    
    if type(parameters['k']) == str:
        parameters = {
                'k': int(parameters['k']),
                'revert': round(float(parameters['revert']),2)
        }
    
    # initialize teams
    
    teams = {
        'San Miguel' : {
            'Philippine' : 1500,
            'Commissioner' : 1500,
            'Governors' : 1500
        },
        'Ginebra' : {
            'Philippine' : 1500,
            'Commissioner' : 1500,
            'Governors' : 1500
        },
        'Alaska' : {
            'Philippine' : 1500,
            'Commissioner' : 1500,
            'Governors' : 1500
        },
        'Star' : {
            'Philippine' : 1500,
            'Commissioner' : 1500,
            'Governors' : 1500
        },
        'TNT' : {
            'Philippine' : 1500,
            'Commissioner' : 1500,
            'Governors' : 1500
        },
        'Phoenix' : {
            'Philippine' : 1500,
            'Commissioner' : 1500,
            'Governors' : 1500
        },
        'Rain or Shine' : {
            'Philippine' : 1500,
            'Commissioner' : 1500,
            'Governors' : 1500
        },
        'Meralco' : {
            'Philippine' : 1500,
            'Commissioner' : 1500,
            'Governors' : 1500
        },
        'Globalport' : {
            'Philippine' : 1500,
            'Commissioner' : 1500,
            'Governors' : 1500
        },
        'NLEX' : {
            'Philippine' : 1500,
            'Commissioner' : 1500,
            'Governors' : 1500
        },
        'Mahindra' : {
            'Philippine' : 1500,
            'Commissioner' : 1500,
            'Governors' : 1500
        },
        'Blackwater' : {
            'Philippine' : 1500,
            'Commissioner' : 1500,
            'Governors' : 1500
        }
    }
    
    data = []
    
    current_ratings = {
        'San Miguel' : 1500,
        'Ginebra' : 1500,
        'Alaska' : 1500,
        'Star' : 1500,
        'TNT' : 1500,
        'Phoenix' : 1500,
        'Rain or Shine' : 1500,
        'Meralco' : 1500,
        'Globalport' : 1500,
        'NLEX' : 1500,
        'Mahindra' : 1500,
        'Blackwater' : 1500
    }
    
    # 2016-17 season
    
    # Philippine
    
    info = simulate_round.game(
        '2016-17/philippine/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2016-17','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['San Miguel'],
        2 : current_ratings['Alaska'],
        3 : current_ratings['Star'],
        4 : current_ratings['TNT'],
        5 : current_ratings['Globalport'],
        6 : current_ratings['Phoenix'],
        7 : current_ratings['Ginebra'],
        8 : current_ratings['Rain or Shine'],
    }
    
    wins = {
        1 : 3,
        2 : 0,
        3 : 1,
        4 : 1,
        5 : 0,
        6 : 0,
        7 : 2,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2016-17/philippine/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2016-17','philippine','playoffs',write_csv
    )
    
    data.append(info)
    update_main_ratings(teams,current_ratings,'Philippine')
    
    # Commissioner's
    
    reset_rating(teams,parameters['revert'],current_ratings,'Commissioner')
    
    info = simulate_round.game(
        '2016-17/commissioner/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2016-17','commissioner','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['Ginebra'],
        2 : current_ratings['San Miguel'],
        3 : current_ratings['Star'],
        4 : current_ratings['TNT'],
        5 : current_ratings['Meralco'],
        6 : current_ratings['Rain or Shine'],
        7 : current_ratings['Phoenix'],
        8 : current_ratings['Globalport']
    }
    
    wins = {
        1 : 1,
        2 : 3,
        3 : 1,
        4 : 2,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2016-17/commissioner/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2016-17','commissioner','playoffs',write_csv
    )
    
    data.append(info)
    update_main_ratings(teams,current_ratings,'Commissioner')
    
    # Governors'
    
    reset_rating(teams,parameters['revert'],current_ratings,'Governors')
    change_name('Mahindra','Kia',teams,current_ratings)
    
    info = simulate_round.game(
        '2016-17/governors/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2016-17','governors','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['Meralco'],
        2 : current_ratings['TNT'],
        3 : current_ratings['Ginebra'],
        4 : current_ratings['Star'],
        5 : current_ratings['NLEX'],
        6 : current_ratings['San Miguel'],
        7 : current_ratings['Rain or Shine'],
        8 : current_ratings['Blackwater']
    }
    
    wins = {
        1 : 2,
        2 : 1,
        3 : 3,
        4 : 1,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2016-17/governors/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2016-17','governors','playoffs',write_csv
    )
    
    data.append(info)
    update_main_ratings(teams,current_ratings,'Governors')
    
    # 2017-18 season
    
    # Philippine
    
    reset_rating(teams,parameters['revert'],current_ratings,'Philippine')
    change_name('Star','Magnolia',teams,current_ratings)
    
    info = simulate_round.game(
        '2017-18/philippine/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2017-18','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['San Miguel'],
        2 : current_ratings['Magnolia'],
        3 : current_ratings['Alaska'],
        4 : current_ratings['Ginebra'],
        5 : current_ratings['Rain or Shine'],
        6 : current_ratings['NLEX'],
        7 : current_ratings['Globalport'],
        8 : current_ratings['TNT'],
    }
    
    wins = {
        1 : 3,
        2 : 2,
        3 : 0,
        4 : 1,
        5 : 0,
        6 : 1,
        7 : 0,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2017-18/philippine/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2017-18','philippine','playoffs',write_csv
    )
    
    data.append(info)
    update_main_ratings(teams,current_ratings,'Philippine')
    
    # Commissioner's
    
    reset_rating(teams,parameters['revert'],current_ratings,'Commissioner')
    change_name('Kia','Columbian',teams,current_ratings)
    
    info = simulate_round.game(
        '2017-18/commissioner/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2017-18','commissioner','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['Rain or Shine'],
        2 : current_ratings['Alaska'],
        3 : current_ratings['TNT'],
        4 : current_ratings['Meralco'],
        5 : current_ratings['Ginebra'],
        6 : current_ratings['San Miguel'],
        7 : current_ratings['Magnolia'],
        8 : current_ratings['Globalport']
    }
    
    wins = {
        1 : 1,
        2 : 1,
        3 : 0,
        4 : 0,
        5 : 3,
        6 : 2,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2017-18/commissioner/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2017-18','commissioner','playoffs',write_csv
    )
    
    data.append(info)
    update_main_ratings(teams,current_ratings,'Commissioner')
    
    # Governors'
    
    reset_rating(teams,parameters['revert'],current_ratings,'Governors')
    change_name('Globalport','NorthPort',teams,current_ratings)
    
    info = simulate_round.game(
        '2017-18/governors/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2017-18','governors','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['Ginebra'],
        2 : current_ratings['Phoenix'],
        3 : current_ratings['Alaska'],
        4 : current_ratings['Magnolia'],
        5 : current_ratings['Blackwater'],
        6 : current_ratings['San Miguel'],
        7 : current_ratings['Meralco'],
        8 : current_ratings['NLEX']
    }
    
    wins = {
        1 : 1,
        2 : 0,
        3 : 2,
        4 : 3,
        5 : 0,
        6 : 0,
        7 : 1,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2017-18/governors/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2017-18','governors','playoffs',write_csv
    )
    
    data.append(info)
    update_main_ratings(teams,current_ratings,'Governors')
    
    # 2018-19 season
    
    # Philippine
    
    reset_rating(teams,parameters['revert'],current_ratings,'Philippine')
    
    info = simulate_round.game(
        '2018-19/philippine/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2018-19','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['Phoenix'],
        2 : current_ratings['Rain or Shine'],
        3 : current_ratings['Ginebra'],
        4 : current_ratings['TNT'],
        5 : current_ratings['San Miguel'],
        6 : current_ratings['Magnolia'],
        7 : current_ratings['NorthPort'],
        8 : current_ratings['Alaska'],
    }
    
    wins = {
        1 : 1,
        2 : 1,
        3 : 0,
        4 : 0,
        5 : 3,
        6 : 2,
        7 : 0,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2018-19/philippine/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2018-19','philippine','playoffs',write_csv
    )
    
    data.append(info)
    update_main_ratings(teams,current_ratings,'Philippine')
    
    # Commissioner's
    
    reset_rating(teams,parameters['revert'],current_ratings,'Commissioner')
    
    info = simulate_round.game(
        '2018-19/commissioner/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2018-19','commissioner','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['TNT'],
        2 : current_ratings['NorthPort'],
        3 : current_ratings['Blackwater'],
        4 : current_ratings['Ginebra'],
        5 : current_ratings['Magnolia'],
        6 : current_ratings['Rain or Shine'],
        7 : current_ratings['San Miguel'],
        8 : current_ratings['Alaska']
    }
    
    wins = {
        1 : 2,
        2 : 0,
        3 : 0,
        4 : 1,
        5 : 0,
        6 : 1,
        7 : 3,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2018-19/commissioner/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2018-19','commissioner','playoffs',write_csv
    )
    
    data.append(info)
    update_main_ratings(teams,current_ratings,'Commissioner')
    
    # Governors'
    
    reset_rating(teams,parameters['revert'],current_ratings,'Governors')
    
    info = simulate_round.game(
        '2018-19/governors/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2018-19','governors','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['NLEX'],
        2 : current_ratings['Meralco'],
        3 : current_ratings['TNT'],
        4 : current_ratings['Ginebra'],
        5 : current_ratings['San Miguel'],
        6 : current_ratings['Magnolia'],
        7 : current_ratings['Alaska'],
        8 : current_ratings['NorthPort']
    }
    
    wins = {
        1 : 0,
        2 : 2,
        3 : 1,
        4 : 3,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 1,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2018-19/governors/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2018-19','governors','playoffs',write_csv
    )
    
    data.append(info)
    update_main_ratings(teams,current_ratings,'Governors')
    
    # 2020 season
    
    # Philippine
    
    reset_rating(teams,parameters['revert'],current_ratings,'Philippine')
    change_name('Columbian','Terrafirma',teams,current_ratings)
    
    info = simulate_round.game(
        '2020/philippine/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2020','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['Ginebra'],
        2 : current_ratings['Phoenix'],
        3 : current_ratings['TNT'],
        4 : current_ratings['San Miguel'],
        5 : current_ratings['Meralco'],
        6 : current_ratings['Alaska'],
        7 : current_ratings['Magnolia'],
        8 : current_ratings['Rain or Shine'],
    }
    
    wins = {
        1 : 3,
        2 : 1,
        3 : 2,
        4 : 0,
        5 : 1,
        6 : 0,
        7 : 0,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2020/philippine/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2020','philippine','playoffs',write_csv
    )
    
    data.append(info)
    update_main_ratings(teams,current_ratings,'Philippine')
    
    # 2021 season
    
    # Philippine
    
    reset_rating(teams,parameters['revert'],current_ratings,'Philippine')
    
    info = simulate_round.game(
        '2021/philippine/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2021','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['TNT'],
        2 : current_ratings['Meralco'],
        3 : current_ratings['Magnolia'],
        4 : current_ratings['San Miguel'],
        5 : current_ratings['NorthPort'],
        6 : current_ratings['Rain or Shine'],
        7 : current_ratings['NLEX'],
        8 : current_ratings['Ginebra'],
    }
    
    wins = {
        1 : 3,
        2 : 1,
        3 : 2,
        4 : 1,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2021/philippine/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2021','philippine','playoffs',write_csv
    )
    
    data.append(info)
    update_main_ratings(teams,current_ratings,'Philippine')
    
    # Governors'
    
    reset_rating(teams,parameters['revert'],current_ratings,'Governors')
    
    info = simulate_round.game(
        '2021/governors/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2021','governors','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['Magnolia'],
        2 : current_ratings['NLEX'],
        3 : current_ratings['TNT'],
        4 : current_ratings['Meralco'],
        5 : current_ratings['San Miguel'],
        6 : current_ratings['Ginebra'],
        7 : current_ratings['Alaska'],
        8 : current_ratings['Phoenix']
    }
    
    wins = {
        1 : 1,
        2 : 1,
        3 : 0,
        4 : 2,
        5 : 0,
        6 : 3,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2021/governors/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2021','governors','playoffs',write_csv
    )
    
    data.append(info)
    update_main_ratings(teams,current_ratings,'Governors')
    
    # 2022-23 season
    
    # Philippine
    
    reset_rating(teams,parameters['revert'],current_ratings,'Philippine')
    change_name('Alaska','Converge',teams,current_ratings)
    
    info = simulate_round.game(
        '2022-23/philippine/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2022-23','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['San Miguel'],
        2 : current_ratings['TNT'],
        3 : current_ratings['Magnolia'],
        4 : current_ratings['Ginebra'],
        5 : current_ratings['Meralco'],
        6 : current_ratings['NLEX'],
        7 : current_ratings['Converge'],
        8 : current_ratings['Blackwater'],
    }
    
    wins = {
        1 : 3,
        2 : 2,
        3 : 1,
        4 : 0,
        5 : 1,
        6 : 0,
        7 : 0,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2022-23/philippine/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2022-23','philippine','playoffs',write_csv
    )
    
    data.append(info)
    update_main_ratings(teams,current_ratings,'Philippine')
    
    # Commissioner's
    
    reset_rating(teams,parameters['revert'],current_ratings,'Commissioner')
    current_ratings['Bay Area'] = 1500
    
    info = simulate_round.game(
        '2022-23/commissioner/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2022-23','commissioner','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['Bay Area'],
        2 : current_ratings['Magnolia'],
        3 : current_ratings['Ginebra'],
        4 : current_ratings['Converge'],
        5 : current_ratings['San Miguel'],
        6 : current_ratings['NorthPort'],
        7 : current_ratings['Phoenix'],
        8 : current_ratings['Rain or Shine']
    }
    
    wins = {
        1 : 2,
        2 : 1,
        3 : 3,
        4 : 0,
        5 : 1,
        6 : 0,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2022-23/commissioner/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2022-23','commissioner','playoffs',write_csv
    )
    
    del current_ratings['Bay Area']
    data.append(info)
    update_main_ratings(teams,current_ratings,'Commissioner')
    
    # Governors'
    
    reset_rating(teams,parameters['revert'],current_ratings,'Governors')
    
    info = simulate_round.game(
        '2022-23/governors/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2022-23','governors','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['TNT'],
        2 : current_ratings['San Miguel'],
        3 : current_ratings['Ginebra'],
        4 : current_ratings['Meralco'],
        5 : current_ratings['Magnolia'],
        6 : current_ratings['NLEX'],
        7 : current_ratings['Converge'],
        8 : current_ratings['Phoenix']
    }
    
    wins = {
        1 : 3,
        2 : 1,
        3 : 2,
        4 : 1,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2022-23/governors/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2022-23','governors','playoffs',write_csv
    )
    
    data.append(info)
    update_main_ratings(teams,current_ratings,'Governors')
    
    # 2023-24
    
    # Commissioner
    
    reset_rating(teams,parameters['revert'],current_ratings,'Commissioner')
    
    info = simulate_round.game(
        '2023-24/commissioner/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2023-24','commissioner','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['Magnolia'],
        2 : current_ratings['San Miguel'],
        3 : current_ratings['Ginebra'],
        4 : current_ratings['Phoenix'],
        5 : current_ratings['Meralco'],
        6 : current_ratings['NorthPort'],
        7 : current_ratings['Rain or Shine'],
        8 : current_ratings['TNT']
    }
    wins = {
        1 : 2,
        2 : 3,
        3 : 1,
        4 : 1,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    data.append(info)
    
    info = simulate_round.game(
        '2023-24/commissioner/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2023-24','commissioner','playoffs',write_csv
    )
    data.append(info)
    update_main_ratings(teams,current_ratings,'Commissioner')
    
    # Philippine
    
    reset_rating(teams,parameters['revert'],current_ratings,'Philippine')
    
    info = simulate_round.game(
        '2023-24/philippine/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2023-24','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['San Miguel'],
        2 : current_ratings['Ginebra'],
        3 : current_ratings['Meralco'],
        4 : current_ratings['TNT'],
        5 : current_ratings['Rain or Shine'],
        6 : current_ratings['NLEX'],
        7 : current_ratings['Magnolia'],
        8 : current_ratings['Terrafirma'],
    }
    
    # wins = {
        # 1 : 3,
        # 2 : 2,
        # 3 : 1,
        # 4 : 0,
        # 5 : 1,
        # 6 : 0,
        # 7 : 0,
        # 8 : 0
    # }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)
    
    data.append(info)
    
    # info = simulate_round.game(
        # '2023-24/philippine/playoffs.csv',
        # parameters['k'],
        # current_ratings,
        # '2023-24','philippine','playoffs',write_csv
    # )
    
    # data.append(info)
    # update_main_ratings(teams,current_ratings,'Philippine')
    
    with open('Playoffs/split_elo.csv','w',newline='') as file:
        writer = csv.writer(file)
        writer.writerows(results_computer(data))

def simulate_SeparateRating_PreviousRevert(parameters,write_csv = False):
    # parameters = {k,revert_season,revert_filipino,revert_import,revert_previous_conference}
    
    if 'revert' in parameters.keys():
        parameters = {
                'k': int(parameters['k']),
                'revert_season': round(float(parameters['revert']),2),
                'revert_filipino': round(float(parameters['revert']),2),
                'revert_import': round(float(parameters['revert']),2),
                'revert_conference': round(float(parameters['revert_conference']),2)
        }
    
    # initialize teams
    
    teams = {
        'San Miguel' : {
            'Philippine' : 1500,
            'Commissioner' : 1500,
            'Governors' : 1500
        },
        'Ginebra' : {
            'Philippine' : 1500,
            'Commissioner' : 1500,
            'Governors' : 1500
        },
        'Alaska' : {
            'Philippine' : 1500,
            'Commissioner' : 1500,
            'Governors' : 1500
        },
        'Star' : {
            'Philippine' : 1500,
            'Commissioner' : 1500,
            'Governors' : 1500
        },
        'TNT' : {
            'Philippine' : 1500,
            'Commissioner' : 1500,
            'Governors' : 1500
        },
        'Phoenix' : {
            'Philippine' : 1500,
            'Commissioner' : 1500,
            'Governors' : 1500
        },
        'Rain or Shine' : {
            'Philippine' : 1500,
            'Commissioner' : 1500,
            'Governors' : 1500
        },
        'Meralco' : {
            'Philippine' : 1500,
            'Commissioner' : 1500,
            'Governors' : 1500
        },
        'Globalport' : {
            'Philippine' : 1500,
            'Commissioner' : 1500,
            'Governors' : 1500
        },
        'NLEX' : {
            'Philippine' : 1500,
            'Commissioner' : 1500,
            'Governors' : 1500
        },
        'Mahindra' : {
            'Philippine' : 1500,
            'Commissioner' : 1500,
            'Governors' : 1500
        },
        'Blackwater' : {
            'Philippine' : 1500,
            'Commissioner' : 1500,
            'Governors' : 1500
        }
    }
    
    data = []
    
    current_ratings = {
        'San Miguel' : 1500,
        'Ginebra' : 1500,
        'Alaska' : 1500,
        'Star' : 1500,
        'TNT' : 1500,
        'Phoenix' : 1500,
        'Rain or Shine' : 1500,
        'Meralco' : 1500,
        'Globalport' : 1500,
        'NLEX' : 1500,
        'Mahindra' : 1500,
        'Blackwater' : 1500
    }
    
    # 2016-17 season
    
    # Philippine
    
    info = simulate_round.game(
        '2016-17/philippine/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2016-17','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['San Miguel'],
        2 : current_ratings['Alaska'],
        3 : current_ratings['Star'],
        4 : current_ratings['TNT'],
        5 : current_ratings['Globalport'],
        6 : current_ratings['Phoenix'],
        7 : current_ratings['Ginebra'],
        8 : current_ratings['Rain or Shine'],
    }
    
    wins = {
        1 : 3,
        2 : 0,
        3 : 1,
        4 : 1,
        5 : 0,
        6 : 0,
        7 : 2,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2016-17/philippine/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2016-17','philippine','playoffs',write_csv
    )
    
    data.append(info)
    update_main_ratings(teams,current_ratings,'Philippine')
    
    # Commissioner's
    
    reset_rating(teams,{'previous': parameters['revert_filipino'], 'conference':parameters ['revert_conference']},current_ratings,'Commissioner',True)
    
    info = simulate_round.game(
        '2016-17/commissioner/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2016-17','commissioner','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['Ginebra'],
        2 : current_ratings['San Miguel'],
        3 : current_ratings['Star'],
        4 : current_ratings['TNT'],
        5 : current_ratings['Meralco'],
        6 : current_ratings['Rain or Shine'],
        7 : current_ratings['Phoenix'],
        8 : current_ratings['Globalport']
    }
    
    wins = {
        1 : 1,
        2 : 3,
        3 : 1,
        4 : 2,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2016-17/commissioner/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2016-17','commissioner','playoffs',write_csv
    )
    
    data.append(info)
    update_main_ratings(teams,current_ratings,'Commissioner')
    
    # Governors'
    
    reset_rating(teams,{'previous': parameters['revert_import'], 'conference': parameters['revert_conference']},current_ratings,'Governors',True)
    change_name('Mahindra','Kia',teams,current_ratings)
    
    info = simulate_round.game(
        '2016-17/governors/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2016-17','governors','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['Meralco'],
        2 : current_ratings['TNT'],
        3 : current_ratings['Ginebra'],
        4 : current_ratings['Star'],
        5 : current_ratings['NLEX'],
        6 : current_ratings['San Miguel'],
        7 : current_ratings['Rain or Shine'],
        8 : current_ratings['Blackwater']
    }
    
    wins = {
        1 : 2,
        2 : 1,
        3 : 3,
        4 : 1,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2016-17/governors/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2016-17','governors','playoffs',write_csv
    )
    
    data.append(info)
    update_main_ratings(teams,current_ratings,'Governors')
    
    # 2017-18 season
    
    # Philippine
    
    reset_rating(teams,{'previous': parameters['revert_season'], 'conference': parameters['revert_conference']},current_ratings,'Philippine',True)
    change_name('Star','Magnolia',teams,current_ratings)
    
    info = simulate_round.game(
        '2017-18/philippine/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2017-18','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['San Miguel'],
        2 : current_ratings['Magnolia'],
        3 : current_ratings['Alaska'],
        4 : current_ratings['Ginebra'],
        5 : current_ratings['Rain or Shine'],
        6 : current_ratings['NLEX'],
        7 : current_ratings['Globalport'],
        8 : current_ratings['TNT'],
    }
    
    wins = {
        1 : 3,
        2 : 2,
        3 : 0,
        4 : 1,
        5 : 0,
        6 : 1,
        7 : 0,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2017-18/philippine/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2017-18','philippine','playoffs',write_csv
    )
    
    data.append(info)
    update_main_ratings(teams,current_ratings,'Philippine')
    
    # Commissioner's
    
    reset_rating(teams,{'previous': parameters['revert_filipino'], 'conference':parameters ['revert_conference']},current_ratings,'Commissioner',True)
    change_name('Kia','Columbian',teams,current_ratings)
    
    info = simulate_round.game(
        '2017-18/commissioner/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2017-18','commissioner','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['Rain or Shine'],
        2 : current_ratings['Alaska'],
        3 : current_ratings['TNT'],
        4 : current_ratings['Meralco'],
        5 : current_ratings['Ginebra'],
        6 : current_ratings['San Miguel'],
        7 : current_ratings['Magnolia'],
        8 : current_ratings['Globalport']
    }
    
    wins = {
        1 : 1,
        2 : 1,
        3 : 0,
        4 : 0,
        5 : 3,
        6 : 2,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2017-18/commissioner/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2017-18','commissioner','playoffs',write_csv
    )
    
    data.append(info)
    update_main_ratings(teams,current_ratings,'Commissioner')
    
    # Governors'
    
    reset_rating(teams,{'previous': parameters['revert_import'], 'conference': parameters['revert_conference']},current_ratings,'Governors',True)
    change_name('Globalport','NorthPort',teams,current_ratings)
    
    info = simulate_round.game(
        '2017-18/governors/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2017-18','governors','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['Ginebra'],
        2 : current_ratings['Phoenix'],
        3 : current_ratings['Alaska'],
        4 : current_ratings['Magnolia'],
        5 : current_ratings['Blackwater'],
        6 : current_ratings['San Miguel'],
        7 : current_ratings['Meralco'],
        8 : current_ratings['NLEX']
    }
    
    wins = {
        1 : 1,
        2 : 0,
        3 : 2,
        4 : 3,
        5 : 0,
        6 : 0,
        7 : 1,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2017-18/governors/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2017-18','governors','playoffs',write_csv
    )
    
    data.append(info)
    update_main_ratings(teams,current_ratings,'Governors')
    
    # 2018-19 season
    
    # Philippine
    
    reset_rating(teams,{'previous': parameters['revert_season'], 'conference': parameters['revert_conference']},current_ratings,'Philippine',True)
    
    info = simulate_round.game(
        '2018-19/philippine/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2018-19','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['Phoenix'],
        2 : current_ratings['Rain or Shine'],
        3 : current_ratings['Ginebra'],
        4 : current_ratings['TNT'],
        5 : current_ratings['San Miguel'],
        6 : current_ratings['Magnolia'],
        7 : current_ratings['NorthPort'],
        8 : current_ratings['Alaska'],
    }
    
    wins = {
        1 : 1,
        2 : 1,
        3 : 0,
        4 : 0,
        5 : 3,
        6 : 2,
        7 : 0,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2018-19/philippine/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2018-19','philippine','playoffs',write_csv
    )
    
    data.append(info)
    update_main_ratings(teams,current_ratings,'Philippine')
    
    # Commissioner's
    
    reset_rating(teams,{'previous': parameters['revert_filipino'], 'conference':parameters ['revert_conference']},current_ratings,'Commissioner',True)
    
    info = simulate_round.game(
        '2018-19/commissioner/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2018-19','commissioner','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['TNT'],
        2 : current_ratings['NorthPort'],
        3 : current_ratings['Blackwater'],
        4 : current_ratings['Ginebra'],
        5 : current_ratings['Magnolia'],
        6 : current_ratings['Rain or Shine'],
        7 : current_ratings['San Miguel'],
        8 : current_ratings['Alaska']
    }
    
    wins = {
        1 : 2,
        2 : 0,
        3 : 0,
        4 : 1,
        5 : 0,
        6 : 1,
        7 : 3,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2018-19/commissioner/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2018-19','commissioner','playoffs',write_csv
    )
    
    data.append(info)
    update_main_ratings(teams,current_ratings,'Commissioner')
    
    # Governors'
    
    reset_rating(teams,{'previous': parameters['revert_import'], 'conference': parameters['revert_conference']},current_ratings,'Governors',True)
    
    info = simulate_round.game(
        '2018-19/governors/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2018-19','governors','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['NLEX'],
        2 : current_ratings['Meralco'],
        3 : current_ratings['TNT'],
        4 : current_ratings['Ginebra'],
        5 : current_ratings['San Miguel'],
        6 : current_ratings['Magnolia'],
        7 : current_ratings['Alaska'],
        8 : current_ratings['NorthPort']
    }
    
    wins = {
        1 : 0,
        2 : 2,
        3 : 1,
        4 : 3,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 1,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2018-19/governors/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2018-19','governors','playoffs',write_csv
    )
    
    data.append(info)
    update_main_ratings(teams,current_ratings,'Governors')
    
    # 2020 season
    
    # Philippine
    
    reset_rating(teams,{'previous': parameters['revert_season'], 'conference': parameters['revert_conference']},current_ratings,'Philippine',True)
    change_name('Columbian','Terrafirma',teams,current_ratings)
    
    info = simulate_round.game(
        '2020/philippine/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2020','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['Ginebra'],
        2 : current_ratings['Phoenix'],
        3 : current_ratings['TNT'],
        4 : current_ratings['San Miguel'],
        5 : current_ratings['Meralco'],
        6 : current_ratings['Alaska'],
        7 : current_ratings['Magnolia'],
        8 : current_ratings['Rain or Shine'],
    }
    
    wins = {
        1 : 3,
        2 : 1,
        3 : 2,
        4 : 0,
        5 : 1,
        6 : 0,
        7 : 0,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2020/philippine/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2020','philippine','playoffs',write_csv
    )
    
    data.append(info)
    update_main_ratings(teams,current_ratings,'Philippine')
    
    # 2021 season
    
    # Philippine
    
    reset_rating(teams,{'previous': parameters['revert_season'], 'conference': parameters['revert_conference']},current_ratings,'Philippine',True)
    
    info = simulate_round.game(
        '2021/philippine/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2021','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['TNT'],
        2 : current_ratings['Meralco'],
        3 : current_ratings['Magnolia'],
        4 : current_ratings['San Miguel'],
        5 : current_ratings['NorthPort'],
        6 : current_ratings['Rain or Shine'],
        7 : current_ratings['NLEX'],
        8 : current_ratings['Ginebra'],
    }
    
    wins = {
        1 : 3,
        2 : 1,
        3 : 2,
        4 : 1,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2021/philippine/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2021','philippine','playoffs',write_csv
    )
    
    data.append(info)
    update_main_ratings(teams,current_ratings,'Philippine')
    
    # Governors'
    
    reset_rating(teams,{'previous': parameters['revert_filipino'], 'conference': parameters['revert_conference']},current_ratings,'Governors',True)
    
    info = simulate_round.game(
        '2021/governors/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2021','governors','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['Magnolia'],
        2 : current_ratings['NLEX'],
        3 : current_ratings['TNT'],
        4 : current_ratings['Meralco'],
        5 : current_ratings['San Miguel'],
        6 : current_ratings['Ginebra'],
        7 : current_ratings['Alaska'],
        8 : current_ratings['Phoenix']
    }
    
    wins = {
        1 : 1,
        2 : 1,
        3 : 0,
        4 : 2,
        5 : 0,
        6 : 3,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2021/governors/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2021','governors','playoffs',write_csv
    )
    
    data.append(info)
    update_main_ratings(teams,current_ratings,'Governors')
    
    # 2022-23 season
    
    # Philippine
    
    reset_rating(teams,{'previous': parameters['revert_season'], 'conference': parameters['revert_conference']},current_ratings,'Philippine',True)
    change_name('Alaska','Converge',teams,current_ratings)
    
    info = simulate_round.game(
        '2022-23/philippine/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2022-23','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['San Miguel'],
        2 : current_ratings['TNT'],
        3 : current_ratings['Magnolia'],
        4 : current_ratings['Ginebra'],
        5 : current_ratings['Meralco'],
        6 : current_ratings['NLEX'],
        7 : current_ratings['Converge'],
        8 : current_ratings['Blackwater'],
    }
    
    wins = {
        1 : 3,
        2 : 2,
        3 : 1,
        4 : 0,
        5 : 1,
        6 : 0,
        7 : 0,
        8 : 0
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2022-23/philippine/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2022-23','philippine','playoffs',write_csv
    )
    
    data.append(info)
    update_main_ratings(teams,current_ratings,'Philippine')
    
    # Commissioner's
    
    reset_rating(teams,{'previous': parameters['revert_filipino'], 'conference':parameters ['revert_conference']},current_ratings,'Commissioner',True)
    current_ratings['Bay Area'] = 1500
    
    info = simulate_round.game(
        '2022-23/commissioner/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2022-23','commissioner','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['Bay Area'],
        2 : current_ratings['Magnolia'],
        3 : current_ratings['Ginebra'],
        4 : current_ratings['Converge'],
        5 : current_ratings['San Miguel'],
        6 : current_ratings['NorthPort'],
        7 : current_ratings['Phoenix'],
        8 : current_ratings['Rain or Shine']
    }
    
    wins = {
        1 : 2,
        2 : 1,
        3 : 3,
        4 : 0,
        5 : 1,
        6 : 0,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2022-23/commissioner/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2022-23','commissioner','playoffs',write_csv
    )
    
    del current_ratings['Bay Area']
    data.append(info)
    update_main_ratings(teams,current_ratings,'Commissioner')
    
    # Governors'
    
    reset_rating(teams,{'previous': parameters['revert_import'], 'conference': parameters['revert_conference']},current_ratings,'Governors',True)
    
    info = simulate_round.game(
        '2022-23/governors/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2022-23','governors','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['TNT'],
        2 : current_ratings['San Miguel'],
        3 : current_ratings['Ginebra'],
        4 : current_ratings['Meralco'],
        5 : current_ratings['Magnolia'],
        6 : current_ratings['NLEX'],
        7 : current_ratings['Converge'],
        8 : current_ratings['Phoenix']
    }
    
    wins = {
        1 : 3,
        2 : 1,
        3 : 2,
        4 : 1,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    
    data.append(info)
    
    info = simulate_round.game(
        '2022-23/governors/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2022-23','governors','playoffs',write_csv
    )
    
    data.append(info)
    update_main_ratings(teams,current_ratings,'Governors')
    
    # 2023-24
    
    # Commissioner
    
    reset_rating(teams,{'previous': parameters['revert_season'], 'conference':parameters ['revert_conference']},current_ratings,'Commissioner',True)
    
    info = simulate_round.game(
        '2023-24/commissioner/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2023-24','commissioner','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['Magnolia'],
        2 : current_ratings['San Miguel'],
        3 : current_ratings['Ginebra'],
        4 : current_ratings['Phoenix'],
        5 : current_ratings['Meralco'],
        6 : current_ratings['NorthPort'],
        7 : current_ratings['Rain or Shine'],
        8 : current_ratings['TNT']
    }
    wins = {
        1 : 2,
        2 : 3,
        3 : 1,
        4 : 1,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0,
    }
    
    info['data'] = playoffs_8teams2.predict_wins_twice4_b05sf(ranking)
    data.append(info)
    
    info = simulate_round.game(
        '2023-24/commissioner/playoffs.csv',
        parameters['k'],
        current_ratings,
        '2023-24','commissioner','playoffs',write_csv
    )
    data.append(info)
    update_main_ratings(teams,current_ratings,'Commissioner')
    
    # Philippine
    
    reset_rating(teams,{'previous': parameters['revert_season'], 'conference': parameters['revert_conference']},current_ratings,'Philippine',True)
    
    info = simulate_round.game(
        '2023-24/philippine/eliminations.csv',
        parameters['k'],
        current_ratings,
        '2023-24','philippine','eliminations',write_csv
    )
    
    ranking = {
        1 : current_ratings['San Miguel'],
        2 : current_ratings['Ginebra'],
        3 : current_ratings['Meralco'],
        4 : current_ratings['TNT'],
        5 : current_ratings['Rain or Shine'],
        6 : current_ratings['NLEX'],
        7 : current_ratings['Magnolia'],
        8 : current_ratings['Terrafirma'],
    }
    
    # wins = {
        # 1 : 3,
        # 2 : 2,
        # 3 : 1,
        # 4 : 0,
        # 5 : 1,
        # 6 : 0,
        # 7 : 0,
        # 8 : 0
    # }
    
    info['data'] = playoffs_8teams2.predict_wins_twice2_b07sf(ranking)
    
    data.append(info)
    
    # info = simulate_round.game(
        # '2023-24/philippine/playoffs.csv',
        # parameters['k'],
        # teams,
        # '2023-24','philippine','playoffs',write_csv
    # )
    
    # data.append(info)
    # update_main_ratings(teams,current_ratings,'Philippine')
        
    with open('Playoffs/blended_elo.csv','w',newline='') as file:
        writer = csv.writer(file)
        writer.writerows(results_computer(data))