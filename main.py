import os
import re
import json
import statistics
import numpy as np
from scipy.stats import pearsonr  # For Pearson correlation
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
routing_distances = []  # Store routing distances for MAPE and correlation
llm_distances = []  # Store LLM distances for correlation

def comparison_test(port1, port2, comparison_num):
    # LLM prompt to predict nautical distances between two ports
    prompt_template = (f'Query: what nautical distance between {port1} and {port2}? '
                       f'Use the most efficient navigational routes. '
                       f'Return only distance in nautical miles accounting for land masses. '
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

    # Routing module output (actual distance between the ports)
    routing_output = routing.get_port_distance(port1, port2)

    # Parse the routing output
    if isinstance(routing_output, str):
        try:
            routing_output = json.loads(routing_output)
        except json.JSONDecodeError:
            raise ValueError(f"Failed to parse routing output: {routing_output}")

    routing_distance = routing_output.get("Distance (Nautical Miles)")
    if routing_distance is None:
        raise ValueError("Distance information not found in routing output")

    print(f"Distance from routing module: {routing_distance} nautical miles")

    # Calculate the difference between LLM distance and routing distance
    difference = llm_distance - routing_distance
    differences.append(difference)  # Store the differences for error metrics
    routing_distances.append(routing_distance)  # Store actual distances for correlation
    llm_distances.append(llm_distance)  # Store LLM-predicted distances for correlation

    # Store the comparison data for later analysis
    comparisons.append({
        "Comparison #": comparison_num,
        "Ports": {
            "Port 1": port1,
            "Port 2": port2
        },
        "LLM Distance (Nautical Miles)": llm_distance,
        "Routing Table Distance": routing_distance,
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

    # Statistical measures:
    # 1. Mean Absolute Error (MAE): Average of the absolute differences between LLM and actual distances.
    #    Lower MAE indicates better overall accuracy.
    mae = np.mean(np.abs(differences))  # Mean Absolute Error

    # 2. Root Mean Squared Error (RMSE): Similar to MAE, but squares the differences, making it more sensitive to large errors.
    #    RMSE penalizes larger errors more heavily than MAE.
    mse = np.mean(np.square(differences))  # Mean Squared Error
    rmse = np.sqrt(mse)  # Root Mean Squared Error

    # 3. Mean Absolute Percentage Error (MAPE): Measures the percentage difference between LLM and actual distances.
    #    MAPE is useful to understand the relative error, as a percentage of the actual distance.
    mape = np.mean([abs(diff) / routing if routing != 0 else 0 for diff, routing in zip(differences, routing_distances)]) * 100  # Mean Absolute Percentage Error

    # 4. Interquartile Range (IQR): Measures the spread of the middle 50% of the differences.
    #    IQR helps understand the variability of the prediction errors.
    q1 = np.percentile(differences, 25)
    q3 = np.percentile(differences, 75)
    iqr = q3 - q1  # Interquartile Range

    # 5. Correlation (Pearson's Correlation Coefficient): Measures the linear relationship between LLM predictions and actual distances.
    #    A high correlation (close to 1) means that the LLM distances follow the same trend as the actual distances.
    correlation, _ = pearsonr(llm_distances, routing_distances)

    # 6. R-Squared (Coefficient of Determination): Tells how much of the variance in actual distances is explained by the LLM's predictions.
    #    Higher R-squared values (closer to 1) mean better prediction accuracy.
    ss_res = np.sum(np.square(np.array(routing_distances) - np.array(llm_distances)))  # Sum of squared residuals
    ss_tot = np.sum(np.square(np.array(routing_distances) - np.mean(routing_distances)))  # Total sum of squares
    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0  # R-Squared

    # Store the statistical data
    statistics_data = {
        "Total Comparisons": n,
        "MAE (Mean Absolute Error)": mae,  # Avg absolute difference
        "MSE (Mean Squared Error)": mse,  # Avg of squared differences
        "RMSE (Root Mean Squared Error)": rmse,  # Sensitivity to large errors
        "MAPE (Mean Absolute Percentage Error)": mape,  # Error in percentage terms
        "IQR (Interquartile Range)": iqr,  # Middle 50% of errors
        "Correlation (Pearson)": correlation,  # Strength of linear relationship
        "R-Squared": r_squared  # Proportion of variance explained by LLM
    }

    # Write the statistics data (Table 2) to a separate JSON file
    with open('table2_statistics.json', 'w') as f:
        json.dump({"Statistics": statistics_data}, f, indent=4)

    # Print the statistics to the console for quick review
    print("Statistical Analysis of Differences:")
    print(f"MAE: {mae} nautical miles")
    print(f"MSE: {mse} nautical miles")
    print(f"RMSE: {rmse} nautical miles")
    print(f"MAPE: {mape}%")
    print(f"IQR: {iqr} nautical miles")
    print(f"Correlation (Pearson): {correlation}")
    print(f"R-Squared: {r_squared}")
