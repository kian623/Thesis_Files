"""
- to calculate metrics on 2016-17 season to 2022-23 season
- in writing round probabilities, up until 2024 Philippine Cup is done
- only csv files from 2016-17 season to 2022-23 season for ratings can be edited
"""
import simulate
import simulate2

def print_results(data):
    for metric,values in data.items():
        print(f'{metric}: {values}')

def Conference_Reset_Model(write_csv,write_probabilities):
    print('\nConference Reset Model\n')
    k = int(input('k: '))
    parameters = {'k' : k, 'revert': 1}

    if write_probabilities == 1:
        simulate2.simulate_SameRating_BackTo1500(parameters)

    print_results(simulate.simulate_SameRating_BackTo1500(parameters,write_csv))

def Season_Reset_Model(write_csv,write_probabilities):
    print('\nSeason Reset Model\n')
    k = int(input('k: '))
    revert = float(input('C: '))
    parameters = {'k' : k, 'revert': revert}

    if write_probabilities == 1:
        simulate2.simulate_SameRating_BackTo1500Yearly(parameters)

    print_results(simulate.simulate_SameRating_BackTo1500Yearly(parameters,write_csv))

def Modified_Silver_Model(write_csv,write_probabilities):
    print('\nModified Silver Model\n')
    k = int(input('k: '))
    revert_season = float(input('C_S: '))
    revert_conference = float(input('C_C: '))
    parameters = {'k' : k, 'revert_season': revert_season, 'revert_conference': revert_conference}

    if write_probabilities == 1:
        simulate2.simulate_SameRating(parameters)

    print_results(simulate.simulate_SameRating(parameters,write_csv))

def Split_Elo_Model(write_csv,write_probabilities):
    print('\nSplit Elo Model\n')
    k = int(input('k: '))
    revert = float(input('C: '))
    parameters = {'k' : k, 'revert': revert}

    if write_probabilities == 1:
        simulate2.simulate_SeparateRating(parameters)

    print_results(simulate.simulate_SeparateRating(parameters,write_csv))

def Blended_Elo_Model(write_csv,write_probabilities):
    print('\nBlended Elo Model\n')
    k = int(input('k: '))
    revert = float(input('C_P: '))
    revert_conference = float(input('C_T: '))
    parameters = {'k' : k, 'revert': revert, 'revert_conference': revert_conference}

    if write_probabilities == 1:
        simulate2.simulate_SeparateRating_PreviousRevert(parameters)

    print_results(simulate.simulate_SeparateRating_PreviousRevert(parameters,write_csv))

prompt = 'Input is not in the given choices.'
models = {
    1: Conference_Reset_Model,
    2: Season_Reset_Model,
    3: Modified_Silver_Model,
    4: Split_Elo_Model,
    5: Blended_Elo_Model
}  
while True:
    print('\nModels')
    print('1: Conference Reset Model')
    print('2: Season Reset Model')
    print('3: Modified Silver Model')
    print('4: Split Elo Model')
    print('5: Blended Elo Model')
    model = int(input('\nChoose the model you wish by typing the appropriate integer: '))
    if model in [1,2,3,4,5]:
        write_csv = int(input('Do you want to write results to csv files? Type 1 if Yes, and 0 otherwise. '))
        if write_csv not in [0,1]:
            print(prompt)
            break
        elif write_csv == 1:
            write_csv = True
        else:
            write_csv = False
        write_probabilities = int(input('Do you want to write probabilities to win each round to csv? Type 1 if Yes, and 0 otherwise. '))
        if write_probabilities not in [0,1]:
            print(prompt)
            break
        
        models[model](write_csv,write_probabilities)
        break
    else:
        print(prompt)
        break