import pybikes
import pandas as pd
import time


capital_bikeshare = pybikes.get('velib')
capital_bikeshare.update()


def get_state(capital_bikeshare):
    
    full_list_state = list()
    
    for station in capital_bikeshare.stations:

        name = station.name
        total_bikes = station.bikes
        free_bikes = station.free
        lat = station.latitude
        long = station.longitude

        full_list_state.append([name, total_bikes, free_bikes, lat, long])

    state = pd.DataFrame(full_list_state, columns=["name", "total_bikes", "free_bikes", "lat", "long"])

    return state



def stream_bikes_all(capital_bikeshare, seconds_delay, number_of_changes):
       
    n = 0
    
    while True:
        n += 1
        print(n)
    
    
        ### Get the latest state.
        latest_state = get_state(capital_bikeshare)
        print(latest_state.shape)

        #wait untill getting again updates
        time.sleep(seconds_delay)
        
        ### Get the new state.
        new_state = get_state(capital_bikeshare)
        print(new_state.shape)
        
        
        ## when total number of changes reach, stop
        if n == number_of_changes: 
            break
    
    
    return latest_state, new_state
    
    
def differences_check(latest_state, new_state):

    for index, row in latest_state.iterrows():
        name = (row["name"])
        free_bikes_initial = row["free_bikes"]


        #cross check with newest state
        filtered_df = new_state[new_state['name'] == name]

        #get free bikes
        free_bikes_new = filtered_df['free_bikes'].values[0]

        #differences
        diff = free_bikes_initial - free_bikes_new

        #print(f"Initial number of free bikes {free_bikes_initial}, new free bikes {free_bikes_new}. Diff is {diff}")

        if diff < 0:
            print("One more free bike available")
            
        elif diff > 0:
            print("One bike was taken")

        else:
            #print("No difference")
            continue
    
    
    
    
def main(capital_bikeshare):

    latest_state, new_state = stream_bikes_all(capital_bikeshare, seconds_delay=30, number_of_changes=1)


    differences_check(latest_state, new_state)
    
    return latest_state, new_state
    
#start
latest_state, new_state = main(capital_bikeshare)
