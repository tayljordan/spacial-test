#!/usr/bin/env python3.11
import os
import re
import json
import statistics
from apis import openai_api, routing
from dotenv import load_dotenv

# Load environment variables
root_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(root_path, 'config.txt')
load_dotenv(config_path)
openai_model = os.getenv('OPENAI_MODEL')

if not openai_model:
    raise ValueError("OpenAI model not found. Check your config file.")

# Initialize lists for storing data
comparisons = []
differences = []

def comparison_test(port1, port2, comparison_num):
    prompt_template = (f'Query: what nautical distance between {port1} and {port2}?'
                       f'Return only distance in nautical miles accounting for land masses.'
                       f'Example output: 8345')

    # LLM output
    llm_output = openai_api.foundation(prompt_template, openai_model=openai_model)

    # Extract integer from the LLM output
    llm_distance = None
    match = re.search(r'\d+', llm_output)
    if match:
        llm_distance = int(match.group())

    if llm_distance is None:
        raise ValueError(f"Failed to parse distance from LLM output: {llm_output}")

    print(f"Nautical distance from LLM: {llm_distance} nautical miles")

    # Routing module output
    routing_output = routing.get_port_distance(port1, port2)

    # Check if routing output is a valid JSON string, otherwise raise an error
    if isinstance(routing_output, str):
        try:
            routing_output = json.loads(routing_output)
        except json.JSONDecodeError:
            raise ValueError(f"Failed to parse routing output: {routing_output}")

    # Extracting the distance from the routing output
    routing_distance = routing_output.get("Distance (Nautical Miles)")
    if routing_distance is None:
        raise ValueError("Distance information not found in routing output")

    print(f"Distance from routing module: {routing_distance} nautical miles")

    # Calculate the difference and store in the differences list
    difference = llm_distance - routing_distance
    differences.append(difference)

    # Store the comparison in the comparisons list
    comparisons.append({
        "Comparison #": comparison_num,
        "Ports": {
            "Port 1": port1,
            "Port 2": port2
        },
        "LLM Distance (Nautical Miles)": llm_distance,
        "Routing Table Distance": routing_output,
        "Difference (LLM - Routing Distance)": difference
    })

if __name__ == "__main__":
    n = 3  # Number of comparisons to run

    for i in range(n):
        # Get two random ports for comparison
        output = routing.get_two_random_ports()
        print(output)

        departure_port = output[0]
        arrival_port = output[1]

        # Perform the comparison and store the results
        comparison_test(departure_port, arrival_port, i + 1)

    # Write the comparison data (Table 1) to a JSON file
    with open('table1_comparisons.json', 'w') as f:
        json.dump({"Comparisons": comparisons}, f, indent=4)

    # Calculate statistical metrics for the differences (Table 2)
    min_difference = min(differences)
    max_difference = max(differences)
    mean_difference = statistics.mean(differences)
    std_deviation = statistics.stdev(differences) if len(differences) > 1 else 0

    # Store the statistical data
    statistics_data = {
        "Total Comparisons": n,
        "Min Difference": min_difference,
        "Max Difference": max_difference,
        "Mean Difference": mean_difference,
        "Standard Deviation of Difference": std_deviation
    }

    # Write the statistics data (Table 2) to a separate JSON file
    with open('table2_statistics.json', 'w') as f:
        json.dump({"Statistics": statistics_data}, f, indent=4)
