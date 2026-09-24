# A helpful nutrition assistant 
## Environment setup 
`pip install -r requirements.txt` 

## Usage 
`python3 main.py` will open an interactive command line program. The user will be required to input their user name for the first time. Then the program will automatically load data and start service. 

### help
type `help` will give all supported commands.
### exit 
type `exit` will exit the program, the record and user data will be saved automatically.
### search 
type `search x` will search related food name according to query `x`.
### eat 
type `eat id n` will record the food you eat, please input the fdc_id of the food to avoid confusion. The fdc_id can be found by search. `id` is the fdc_id, `n` is the weight of the food in gram. 
### today 
type `today` will print a brief summary of what user has eaten for today.
### newday
type `newday` will start a new day and save the previous record to the history.
### history
type `history` will show a brief report of all past records.
### recommend
type `recommend mode` will give a recommend meal according to the `mode`. The user can select the mode from `cheap`: gives the cheapest meal satisfying the needs, `prefer`: prefer the food the user has eaten for the past, `random`: randomly give a meal that satisfies the need. 
### load & save 
type `load (path)` and `save (path)` will save and load past history from `path`, the `path` is optional, if not used, the program will save and load from default file path.
### clear
type `clear` to clear current records and past history entirely.
