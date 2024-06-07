"""
for reading and writing csv files for ratings
"""
from csv import DictReader,DictWriter

def read_scores(filename):
    
    with open(filename) as file:
        reader = DictReader(file)
        data = list(reader)
            
        # create list of lists that contains data
        games = [row for row in data]
    
    for game in games:
        game['score1'] = int(game['score1'])
        game['score2'] = int(game['score2'])
    
    return games

def scores_add_new_elo(filename,games,write_csv): # write to csv if write_csv = True
    
    if write_csv == True:
        info = games[:]
        field_names = [
            'name1',
            'starting elo1',
            'score1',
            'ending elo1',
            'name2',
            'starting elo2',
            'score2',
            'ending elo2'
        ]
        with open(filename, 'w', newline = '') as file:
            writer = DictWriter(file, fieldnames = field_names)
            writer.writeheader()
            writer.writerows(info)