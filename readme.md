Here is the README in a code block for easy copy and paste:


# Nautical Distance Comparison using LLM and Routing Table

This project compares nautical distances between two ports using an AI model (LLM) and a routing table. The script generates two outputs:
1. A **comparison table** that stores the LLM and routing table distances for multiple port pairs.
2. A **statistical report** that provides insights such as the minimum, maximum, mean, and standard deviation of the differences between the LLM-predicted distances and the actual routing distances.

## Features
- Query distances between random port pairs using a Large Language Model (LLM).
- Retrieve actual nautical distances from a routing module.
- Compare the distances and store the results in a structured format.
- Generate statistical summaries for the differences between the LLM's predictions and the routing table's distances.

## Prerequisites
- Python 3.11
- The following Python libraries are required:
  - `openai_api`: For interacting with the LLM.
  - `routing`: For retrieving actual nautical distances between ports.
  - `dotenv`: For loading environment variables.
  - `statistics`: For generating statistical reports.

## Environment Variables
Make sure to define the `OPENAI_MODEL` in your environment by providing a `.env` file at the root of the project. This file should contain the following:


OPENAI_MODEL=<your_openai_model>


## How It Works
1. The script randomly selects pairs of ports.
2. It queries the LLM for the nautical distance between the ports.
3. It retrieves the actual distance from the routing table.
4. It compares the LLM-predicted distance with the actual distance and stores the results.
5. After the comparisons, the script calculates statistical metrics and generates a report.

### Output Files
- **`table1_comparisons.json`**: Contains detailed comparison results for each port pair.
- **`table2_statistics.json`**: Contains statistical summaries of the differences between LLM-predicted distances and routing distances.

## Usage

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```bash
   cd <project-directory>
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file and add your OpenAI model key:
   ```bash
   echo "OPENAI_MODEL=<your_openai_model>" > .env
   ```

5. Run the script:
   ```bash
   python main.py
   ```

6. After the script runs, check the generated JSON files:
   - **`table1_comparisons.json`**: Contains the comparison data.
   - **`table2_statistics.json`**: Contains the statistical analysis.

## Example Output

### `table1_comparisons.json`
```json
{
    "Comparisons": [
        {
            "Comparison #": 1,
            "Ports": {
                "Port 1": "Singapore",
                "Port 2": "Nagoya"
            },
            "LLM Distance (Nautical Miles)": 2600,
            "Routing Table Distance": {
                "Port 1": {
                    "Port": "Singapore",
                    "Country": "Singapore",
                    "Latitude": 1.26,
                    "Longitude": 103.8,
                    "Score": 100
                },
                "Port 2": {
                    "Port": "Nagoya",
                    "Country": "Japan",
                    "Latitude": 35.05,
                    "Longitude": 136.86,
                    "Score": 100
                },
                "Distance (Nautical Miles)": 2849.05
            },
            "Difference (LLM - Routing Distance)": -249.05
        }
    ]
}
```

### `table2_statistics.json`
```json
{
    "Statistics": {
        "Total Comparisons": 3,
        "Min Difference": -249.05,
        "Max Difference": 100,
        "Mean Difference": -74.26,
        "Standard Deviation of Difference": 160.52
    }
}
```

## License
This project is licensed under the MIT License.
