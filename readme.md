

# Nautical Distance Comparison using LLM and Routing Table

This project compares nautical distances between two ports using an AI model (LLM) and a routing table. The script generates two outputs:
1. A **comparison table** that stores the LLM and routing table distances for multiple port pairs.
2. A **statistical report** that provides insights such as the mean absolute error (MAE), root mean squared error (RMSE), mean absolute percentage error (MAPE), and more, between the LLM-predicted distances and the actual routing distances.

## Features
- Query distances between random port pairs using a Large Language Model (LLM).
- Retrieve actual nautical distances from a routing module.
- Compare the distances and store the results in a structured format.
- Generate statistical summaries for the differences between the LLM's predictions and the routing table's distances.

## Prerequisites
- Python 3.11 or higher
- The following Python libraries are required:
  - `openai_api`: For interacting with the LLM.
  - `routing`: For retrieving actual nautical distances between ports.
  - `dotenv`: For loading environment variables.
  - `statistics`, `numpy`, `scipy`: For generating statistical reports and performing correlation analysis.

## Environment Variables
Define the `OPENAI_MODEL` environment variable in a `.env` file at the root of the project. The file should contain the following entry:

```
OPENAI_MODEL=<your_openai_model_key>
```

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

## Statistical Metrics
The script calculates the following metrics based on the difference between LLM-predicted and actual routing distances:
- **Mean Absolute Error (MAE)**: Average of absolute differences.
- **Root Mean Squared Error (RMSE)**: Square root of the mean of squared differences.
- **Mean Absolute Percentage Error (MAPE)**: Percentage difference between LLM and actual distances.
- **Interquartile Range (IQR)**: Spread of the middle 50% of the differences.
- **Pearson Correlation**: Measures the linear relationship between LLM predictions and actual distances.
- **R-Squared**: Proportion of variance in the actual distances explained by LLM predictions.

## License
This project is licensed under the MIT License.
