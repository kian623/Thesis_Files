# Thesis_Files
Files and code used for my BS Math Thesis in UP Diliman

To use the codes, the **numpy** and **p_tqdm** packages must be installed.

## Models

Kindly refer to the following table regarding which naming conventions used in functions and csv files refers to which model.

| Model                   | Function                       |
|-------------------------|--------------------------------|
| Conference Reset Model  | SameRating_BackTo1500          |
| Season Reset Model      | SameRating_BackTo1500Yearly    |
| Modified Silver Model   | SameRating                     |
| Split Elo Model         | SeparateRating                 |
| Blended Elo Model       | SeparateRating_PreviousRevert  |

## Optimizing Parameters

To optimize parameters, simply run `optimize.py`. The default values for the grid search are those indicated in the manuscript of my thesis. To change these values, edit the necessary CSV files (csv files without "_result"). Values of the objective functions for each set of parameters can be found in the csv files ending in "_result".

## Evaluate Objective Functions and Modify CSV Files Containing Ratings

To find the value of objective functions for certain parameters, run `main.py`. The CSV files can also be edited using this.

CSV files containing ratings before and after each game for each conference can be accessed by choosing the folder with the following hierarchy: season\conference\round.

CSV files containing probabilities of a team to win each round of the playoffs can be found on **Playoffs** folder for each model. These files are simly contains (in order) Elo Ratings, probability to win round 1, probability to win round 2, probability to win round 2, and the expected number of series wins for each playoff team. To parse the data, note that rows 1-8 contains the details for the 1st to 8th seeds of the 2016-17 Philippine Cup, 9-16 contains the details for the 1st to 8th seeds of the 2017 Commissioner's Cup, and so on.

Also in the **Playoffs** folder is `PBA playoff predictions.xlsx`, which simply compiles the information in the CSV files in the folder. Note that the values of this spreadsheet is NOT automatically updated when the values in the other files in the folder is updated. Values in the current spreadsheet are obtained using optimal parameter settings for each model. Optimal parameter values can be found in ``Optimized Parameter Values per Objective Function.txt``. Only included in the thesis are parameters for the optimized RMSE.
