"""
for optimizing parameters for models
"""
import simulate
# import multiprocessing
from p_tqdm import p_map
import csv

def simulate_progress_SameRating_BackTo1500(parameters):
    result = {**parameters, **simulate.simulate_SameRating_BackTo1500(parameters)}
    # print(parameters)
    return result

def simulate_progress_SameRating_BackTo1500Yearly(parameters):
    result = {**parameters, **simulate.simulate_SameRating_BackTo1500Yearly(parameters)}
    # print(parameters)
    return result

def simulate_progress_SameRating(parameters):
    result = {**parameters, **simulate.simulate_SameRating(parameters)}
    # print(parameters)
    return result

def simulate_progress_SeparateRating(parameters):
    result = {**parameters, **simulate.simulate_SeparateRating(parameters)}
    # print(parameters)
    return result

def simulate_progress_SeparateRating_PreviousRevert(parameters):
    result = {**parameters, **simulate.simulate_SeparateRating_PreviousRevert(parameters)}
    # print(parameters)
    return result

def find_best(results):
    best_param = {
        'root series wins squared error' : 0,
        'brier' : 0,
        'logloss' : 0
    }
    
    for condition in best_param.keys():
        best = min(results, key = lambda x:x[condition])
        best_param[condition] = best
            
    return best_param

if __name__ == "__main__":

    best_parameters = {}
    
    # Conference Reset Model
    
    with open('parameters_SameRating_BackTo1500.csv') as file:
        reader = csv.DictReader(file)
        parameters = list(reader)
        
    # with multiprocessing.Pool() as pool:
        # results = pool.map(simulate_progress_SameRating_BackTo1500,parameters)
    results = p_map(simulate_progress_SameRating_BackTo1500,parameters)
    
    with open('parameters_SameRating_BackTo1500_result.csv','w',newline='') as file:
        conditions = results[0].keys()
        writer = csv.DictWriter(file,fieldnames = conditions)
        writer.writeheader()
        for result in results:
            writer.writerow(result)
    
    best_parameters['Conference Reset Model'] = {condition: value for condition, value in find_best(results).items()}
    
    # Season Reset Model
    
    with open('parameters_SameRating_BackTo1500Yearly.csv') as file:
        reader = csv.DictReader(file)
        parameters = list(reader)
        
    # with multiprocessing.Pool() as pool:
        # results = pool.map(simulate_progress_SameRating_BackTo1500Yearly,parameters)
    results = p_map(simulate_progress_SameRating_BackTo1500Yearly,parameters)
    
    with open('parameters_SameRating_BackTo1500Yearly_result.csv','w',newline='') as file:
        conditions = results[0].keys()
        writer = csv.DictWriter(file,fieldnames = conditions)
        writer.writeheader()
        for result in results:
            writer.writerow(result)
    
    best_parameters['Season Reset Model'] = {condition: value for condition, value in find_best(results).items()}
    
    # Modified Silver Model
    
    with open('parameters_SameRating.csv') as file:
        reader = csv.DictReader(file)
        parameters = list(reader)
        
    # with multiprocessing.Pool() as pool:
        # results = pool.map(simulate_progress_SameRating,parameters)
    results = p_map(simulate_progress_SameRating,parameters)
    
    with open('parameters_SameRating_result.csv','w',newline='') as file:
        conditions = results[0].keys()
        writer = csv.DictWriter(file,fieldnames = conditions)
        writer.writeheader()
        for result in results:
            writer.writerow(result)
    
    best_parameters['Modified Silver Model'] = {condition: value for condition, value in find_best(results).items()}
    
    # Split Elo Model

    with open('parameters_SeparateRating.csv') as file:
        reader = csv.DictReader(file)
        parameters = list(reader)
        
    # with multiprocessing.Pool() as pool:
        # results = pool.map(simulate_progress_SeparateRating,parameters)
    results = p_map(simulate_progress_SeparateRating,parameters)
    
    with open('parameters_SeparateRating_result.csv','w',newline='') as file:
        conditions = results[0].keys()
        writer = csv.DictWriter(file,fieldnames = conditions)
        writer.writeheader()
        for result in results:
            writer.writerow(result)
    
    best_parameters['Split Elo Model'] = {condition: value for condition, value in find_best(results).items()}
    
    # Blended Elo Model

    with open('parameters_SeparateRating_PreviousRevert.csv') as file:
        reader = csv.DictReader(file)
        parameters = list(reader)
        
    # with multiprocessing.Pool() as pool:
        # results = pool.map(simulate_progress_SeparateRating_PreviousRevert,parameters)
    results = p_map(simulate_progress_SeparateRating_PreviousRevert,parameters)
    
    with open('parameters_SeparateRating_PreviousRevert_result.csv','w',newline='') as file:
        conditions = results[0].keys()
        writer = csv.DictWriter(file,fieldnames = conditions)
        writer.writeheader()
        for result in results:
            writer.writerow(result)
    
    best_parameters['Blended Elo Model'] = {condition: value for condition, value in find_best(results).items()}
    
    for model,conditions in best_parameters.items():
        print(f"\n{model}")
        for condition, values in conditions.items():
            print(f"\n{condition}\n")
            for key, value in values.items():
                print(f"{key}: {value}")