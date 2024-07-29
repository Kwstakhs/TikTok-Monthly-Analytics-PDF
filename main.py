import os
from datetime import datetime
import pandas as pd
from data_processing import load_and_preprocess_csv, ensure_numeric, generate_summary_report
from plotting import plot_sum_metric, plot_normalized_metric
from pdf_generation import generate_pdf
import seaborn as sns

# Define the directory containing the CSV files
directory = 'Months CSV'
output_directory = 'Monthly Reports PDF'

# Create output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Initialize the budget dictionary
monthly_budgets = {
    'June': 50, 'May': 39, 'July': 0, 'April': 110
}

# Get all CSV files in the directory
csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

# Initialize list to hold data
all_data = []

# Process each CSV file
for file in csv_files:
    try:
        month_name = file.split('.')[0]  # Get the month name from the file name
        file_path = os.path.join(directory, file)
        df = load_and_preprocess_csv(file_path)

        # Assign the month to the dataframe
        df['Month'] = month_name

        # Append to the list
        all_data.append(df)
    except Exception as e:
        print(f"Error processing file {file}: {e}")

# Combine all monthly data
all_data = [df for df in all_data if not df.empty]
all_data_df = pd.concat(all_data).reset_index(drop=True)

# Define metrics for summing
sum_metrics = [
    'Video views', 'Reached audience', 'Profile views', 'Likes', 'Shares',
    'Comments', 'Product link clicks', 'Product link complete payment',
    'Product link GMV', 'Website clicks', 'Phone number clicks',
    'App download link clicks', 'Net growth', 'New followers', 'Lost followers'
]

# Filter sum_metrics to include only columns that are present in the data
sum_metrics = [metric for metric in sum_metrics if metric in all_data_df.columns]

# Ensure all necessary columns are numeric
all_data_df = ensure_numeric(all_data_df, sum_metrics)

# Sort months chronologically
month_order = sorted(all_data_df['Month'].unique(), key=lambda x: datetime.strptime(x, "%B"))
all_data_df['Month'] = pd.Categorical(all_data_df['Month'], categories=month_order, ordered=True)

# Define colors for each month dynamically
months = all_data_df['Month'].unique()
palette = sns.color_palette("rocket", len(months))
palette = dict(zip(months, palette))

# Create directories for saving graphs
os.makedirs('Graphs', exist_ok=True)
os.makedirs('Graphs/Performance', exist_ok=True)

# Initialize dictionary to keep track of links for content page
links = []
performance_links = []

# Plot each sum metric
for metric in sum_metrics:
    try:
        filename = plot_sum_metric(all_data_df, metric, "TikTok", palette)
        if filename:
            links.append((f"Total {metric}", filename))
    except Exception as e:
        print(f"Error plotting sum metric {metric}: {e}")

# Sum the values of each metric by month
monthly_data = all_data_df.groupby('Month', observed=True)[sum_metrics].sum().reset_index()

# Normalize the summed metrics by their respective budgets
for month in monthly_data['Month']:
    budget = monthly_budgets.get(month, 0)
    if budget > 0:
        monthly_data.loc[monthly_data['Month'] == month, [metric + ' per $' for metric in sum_metrics]] = \
            monthly_data.loc[monthly_data['Month'] == month, sum_metrics].div(budget).values
    else:
        monthly_data.loc[monthly_data['Month'] == month, [metric + ' per $' for metric in sum_metrics]] = 0

# Print the normalized data for debugging
print("Normalized monthly data:")
print(monthly_data)

# Plot the normalized metrics for each month
for metric in sum_metrics:
    try:
        filename = plot_normalized_metric(monthly_data, metric, "TikTok", palette)
        if filename:
            performance_links.append((f"{metric} per $", filename))
    except Exception as e:
        print(f"Error plotting normalized metric {metric}: {e}")

# Remove empty links
links = [link for link in links if link[1] is not None]
performance_links = [link for link in performance_links if link[1] is not None]

# Generate and save summary reports and PDFs
summary_sum, _ = generate_summary_report(all_data_df, sum_metrics, [])
if summary_sum is not None:
    generate_pdf("TikTok", summary_sum, None, links, performance_links, output_directory)
