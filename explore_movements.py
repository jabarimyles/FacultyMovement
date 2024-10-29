import pandas as pd

# Load the Excel file
excel_file = '/Users/jabarimyles/Documents/Dissertation_Research/Escobedo/FHN_vFinal.xlsx'  # Replace with your file path

import pandas as pd
import re
from fuzzywuzzy import process
from matplotlib import pyplot as plt

# Function to fuzzy match and merge two DataFrames
def fuzzy_merge(df_left, df_right, left_on, right_on, rank_col,  threshold=90):
    # Convert columns to string and fill NaN values to avoid errors
    df_left[left_on] = df_left[left_on].fillna('').astype(str)
    df_right[right_on] = df_right[right_on].fillna('').astype(str)
    
    # Prepare a column for matched values and scores
    df_left['match_key'] = None
    df_left['match_score'] = None

    # Fuzzy match each val
    for idx, value in df_left[left_on].items():
        match_result = process.extractOne(value, df_right[right_on].tolist(), score_cutoff=threshold)
        
        # Check if a match was found
        if match_result:
            match, score = match_result
            df_left.at[idx, 'match_key'] = match
            df_left.at[idx, 'match_score'] = score

    # Perform a left join between df_left and df_right_filtered on the fuzzy matched key
    try: 
        #df_left = df_left.drop('University Name', axis=1)
        df_right_filtered = df_right[[right_on, rank_col]]
        merged_df = pd.merge(df_left, df_right_filtered, left_on=['match_key' ], right_on=[right_on], how='left')

    except:
        df_right_filtered = df_right[[right_on, rank_col]]
        merged_df = pd.merge(df_left, df_right_filtered, left_on=['match_key'], right_on=[right_on], how='left')

    return merged_df



# Function to clean up and parse the data
def parse_university_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = []
    # Updated headers as per your request
    headers = ["University Name", "B-FASP", "MVR", "MVS", "MVS2", "USNEWS", "D-C Cluster", "B-FASP Clustering"]

    # Regex pattern to capture the university name and the numeric columns
    pattern = r"^(.*?)(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([N/\d]+)\s+(\d+)\s+(\d+)$"

    for line in lines:
        match = re.match(pattern, line.strip())
        if match:
            university_name = match.group(1).strip()  # Capture university name
            row = [
                university_name,
                int(match.group(2)),  # B-FASP
                int(match.group(3)),  # MVR
                int(match.group(4)),  # MVS
                int(match.group(5)),  # MVS2
                int(match.group(6)),       # USNEWS (could be 'N/A')
                int(match.group(7)),   # D-C Cluster
                int(match.group(8))    # B-FASP Clustering
            ]
            data.append(row)

    # Create DataFrame
    df = pd.DataFrame(data, columns=headers)
    return df



# Optionally, save to CSV
bfasp_rankings = pd.read_csv('university_data.csv')


# Read all sheets into a dictionary of DataFrames
sheets_dict = pd.read_excel(excel_file, sheet_name=None)

# Concatenate all DataFrames into a single DataFrame
movement_df = pd.concat(sheets_dict.values(), ignore_index=True)
movement_df.columns = movement_df.columns.str.replace(' ', '', regex=True)

movement_df = fuzzy_merge(movement_df, bfasp_rankings, 'Currentlyworking', 'University Name', 'B-FASP')

bfasp_rankings = bfasp_rankings.rename(columns={'B-FASP': 'PreviousRanking1', 'University Name': 'PreviousUniversity1'})
movement_df = fuzzy_merge(movement_df, bfasp_rankings, 'Previouslyworked1', 'PreviousUniversity1', 'PreviousRanking1')

bfasp_rankings = bfasp_rankings.rename(columns={'PreviousRanking1': 'PreviousRanking2', 'PreviousUniversity1': 'PreviousUniversity2'})
movement_df = fuzzy_merge(movement_df, bfasp_rankings, 'Previouslyworked2', 'PreviousUniversity2', 'PreviousRanking2')
bfasp_rankings = bfasp_rankings.rename(columns={'PreviousRanking2': 'PreviousRanking3', 'PreviousUniversity2': 'PreviousUniversity3'})
movement_df = fuzzy_merge(movement_df, bfasp_rankings, 'Previouslyworked3', 'PreviousUniversity3', 'PreviousRanking3')
bfasp_rankings = bfasp_rankings.rename(columns={'PreviousRanking3': 'PreviousRanking4', 'PreviousUniversity3': 'PreviousUniversity4'})
movement_df = fuzzy_merge(movement_df, bfasp_rankings, 'Previouslyworked4', 'PreviousUniversity4', 'PreviousRanking4')



no_movers = movement_df[movement_df['Previouslyworked1'] == '']

one_movers = movement_df[(movement_df['Previouslyworked1'] != '') & (movement_df['Previouslyworked2'] == '')]
two_movers = movement_df[(movement_df['Previouslyworked2'] != '') & (movement_df['Previouslyworked3'] == '')]

three_movers = movement_df[(movement_df['Previouslyworked3'] != '') & (movement_df['Previouslyworked4'] == '')]
plt.hist(one_movers['B-FASP'] - one_movers['PreviousRanking1'])
plt.savefig("one_movers_hist.png")
print("The average move for a one mover was " + str(one_movers['B-FASP'].mean() - one_movers['PreviousRanking1'].mean()))
plt.clf()

plt.hist(two_movers['B-FASP'] - two_movers['PreviousRanking1'])
plt.savefig("two_movers_first_hist.png")
print("The average 1st move for a two mover was " + str(two_movers['B-FASP'].mean() - two_movers['PreviousRanking1'].mean()))
print("The average 2nd move for a two mover was " + str(two_movers['PreviousRanking1'].mean() - two_movers['PreviousRanking2'].mean()))

plt.clf()

plt.hist(two_movers['PreviousRanking1'] - two_movers['PreviousRanking2'])
plt.savefig("two_movers_second_hist.png")
plt.clf()

plt.hist(three_movers['B-FASP'] - three_movers['PreviousRanking1'])
plt.savefig("three_movers_first_hist.png")
print("The average 1st move for a one mover was " + str(three_movers['B-FASP'].mean() - three_movers['PreviousRanking1'].mean()))
print("The average 2nd move for a three mover was " + str(three_movers['PreviousRanking1'].mean() - three_movers['PreviousRanking2'].mean()))
print("The average 3rd move for a three mover was " + str(three_movers['PreviousRanking2'].mean() - three_movers['PreviousRanking3'].mean()))

plt.clf()

plt.hist(three_movers['PreviousRanking1'] - three_movers['PreviousRanking2'])
plt.savefig("three_movers_second_hist.png")
plt.clf()

plt.hist(three_movers['PreviousRanking2'] - three_movers['PreviousRanking3'])
plt.savefig("three_movers_third_hist.png")
plt.clf()

print(str(round(1- movement_df['postdoc'].isna().mean(),2)) + " percent of people did 1 postdoc")

print(str(round(no_movers.shape[0]/movement_df.shape[0],2)) + " percent of people moved 0 times")
print(str(round(one_movers.shape[0]/movement_df.shape[0],2)) + " percent of people moved 1 times")
print(str(round(two_movers.shape[0]/movement_df.shape[0],2)) + " percent of people moved 2 times")
print(str(round(three_movers.shape[0]/movement_df.shape[0],2)) + " percent of people moved 3 times")

# Display the movement DataFrame
print(movement_df)
