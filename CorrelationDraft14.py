import pandas as pd
from datetime import timedelta
import re

# File paths
soe_file_path = r'D:\SPCE\BTECH PROJECT\28thApril2025\SOE_26042025.csv'
all_points_file_path = r'D:\SPCE\BTECH PROJECT\New folder\all_points (3).xlsx'
output_file_path = r'D:\SPCE\BTECH PROJECT\NEWerProcessed_Output22.xlsx'

# Load the SOE CSV file
df = pd.read_csv(soe_file_path, usecols=(0, 1, 2, 3, 4, 5, 6, 7), 
                 names=['Area', 'CATEGORY', 'LOCATION', 'TEXT', 'comp_id', 'date', 'time', 'ms'])

print("Step 1: Total rows in SOE file:", df.shape[0])

# Clean CATEGORY field
df['CATEGORY'] = df['CATEGORY'].str.strip()
allowed_categories = ['765KV-CB', '400KV-CB']
df1 = df[df['CATEGORY'].isin(allowed_categories)].copy()

print("Step 2: Rows after CATEGORY filter:", df1.shape[0])

# Convert 'date' and 'time' to datetime
df1['datetime'] = pd.to_datetime(df1['date'] + ' ' + df1['time'], dayfirst=True, errors='coerce')
df1.dropna(subset=['datetime'], inplace=True)

# List to store results
results = []

# Process each row in df1
for i in range(df1.shape[0]):
    text_field = df1.iloc[i, 3]
    match1 = re.search(r'\((.*?)\)', text_field)
    if match1:
        try:
            station_name1 = match1.group(1)
            if '_' not in station_name1:  # Skip ICT lines
                event_time = df1.iloc[i]['datetime']
                start_time = event_time - timedelta(minutes=15)
                time_window_end = event_time + timedelta(minutes=15)

                seen_combinations = set()

                for j in range(i + 1, df1.shape[0]):
                    current_time = df1.iloc[j]['datetime']
                    if current_time <= time_window_end:
                        text_field2 = df1.iloc[j, 3]
                        match2 = re.search(r'\((.*?)\)', text_field2)
                        if not match2:
                            continue
                        station_name2 = match2.group(1)

                        names = sorted([station_name1.strip(), station_name2.strip()])
                        arranged_name = f"4_{names[0]}_{names[1]}"

                        if (arranged_name, event_time) in seen_combinations:
                            continue
                        seen_combinations.add((arranged_name, event_time))

                        results.append({
                            'Station Name 1': station_name1,
                            'Station Name 2': station_name2,
                            'Arranged Name': arranged_name,
                            'Event Time': event_time,
                            'Start Time': start_time,
                            'End Time': time_window_end
                        })

                        break  # Stop after first valid match
        except Exception as e:
            print(f"Error processing row {i}: {e}")
            continue

# Convert results to DataFrame
results_df = pd.DataFrame(results)
print("Step 3: Matched events (results_df):", results_df.shape[0])
print(results_df.head())

# Load all_points data
all_points_df = pd.read_excel(all_points_file_path)
print("Step 4: Loaded all_points entries:", all_points_df.shape[0])

# Filter all_points_df for matches with "Arranged Name" and containing "MW"
final_results = []
for _, row in results_df.iterrows():
    matches = all_points_df[all_points_df['LongId'].astype(str).str.contains(row['Arranged Name'], na=False)]
    mw_matches = matches[matches['LongId'].str.contains('MW', na=False)]

    for _, match in mw_matches.iterrows():
        final_results.append({
            'Station Name 1': row['Station Name 1'],
            'Station Name 2': row['Station Name 2'],
            'Arranged Name': row['Arranged Name'],
            'Matched LongId': match['LongId'],
            'Point ID': match['PointId'],
            'Event Time': row['Event Time'],
            'Start Time': row['Start Time'],
            'End Time': row['End Time']
        })

# Convert final results to DataFrame and save as Excel
final_results_df = pd.DataFrame(final_results)
print("Step 5: Final matched MW points:", final_results_df.shape[0])
print(final_results_df.head())

final_results_df.to_excel(output_file_path, index=False)
print(f"\u2705 Results saved to {output_file_path}")
