import pandas as pd
from fuzzywuzzy import process
import json
import searoute as sr
import os, random

# Load data from csv
root_path = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(root_path, '../data/portlist.csv')

# Get port database
df = pd.read_csv(csv_path, header=None, names=['Port', 'Country', 'Latitude', 'Longitude'])


def get_two_random_ports():
    # Select two random ports from the dataframe
    random_ports = df.sample(2)
    port_name1 = random_ports.iloc[0]['Port']
    port_name2 = random_ports.iloc[1]['Port']
    return port_name1, port_name2


# Combined function to perform fuzzy search on two ports and return sea route distance
def get_port_distance(port_name1, port_name2):
    # Fuzzy search for the first port
    match1, score1, idx1 = process.extractOne(port_name1, df['Port'])
    port1 = df.iloc[idx1]
    port1_info = {
        'Port': port1['Port'],
        'Country': port1['Country'],
        'Latitude': port1['Latitude'],
        'Longitude': port1['Longitude'],
        'Score': score1
    }

    # Fuzzy search for the second port
    match2, score2, idx2 = process.extractOne(port_name2, df['Port'])
    port2 = df.iloc[idx2]
    port2_info = {
        'Port': port2['Port'],
        'Country': port2['Country'],
        'Latitude': port2['Latitude'],
        'Longitude': port2['Longitude'],
        'Score': score2
    }

    # Calculate sea route distance between the two ports
    origin = [port1['Latitude'], port1['Longitude']]
    destination = [port2['Latitude'], port2['Longitude']]
    try:
        route_info = sr.searoute([origin[1], origin[0]], [destination[1], destination[0]], units="naut")
        distance_nm = route_info.get("properties", {}).get("length", None)
        distance = distance_nm if distance_nm is not None else "Distance not found"
    except Exception as e:
        distance = f"Error calculating route: {str(e)}"

    # Return the results
    return json.dumps({
        'Port 1': port1_info,
        'Port 2': port2_info,
        'Distance (Nautical Miles)': distance
    }, indent=4)



