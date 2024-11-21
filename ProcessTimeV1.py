import pandas as pd


file_path = "c:\\Users\\Ricardo Rivera\\OneDrive - Hanwha Q CELLS\\Documents\\Python\\TimeforEachProcess.xlsx"  # Replace with your file path
df = pd.read_excel(file_path)


time_columns = {}

# Iterate through columns and process only those that end with "Time"
for col in df.columns:
    if col.endswith("Time"):  # Check if the column name ends with "Time"
        df[col] = pd.to_datetime(df[col])
        if pd.api.types.is_datetime64_any_dtype(df[col]):  # Check if column is datetime
            df[col] = df[col].dt.time  # Extract only the time portion
            time_columns[col] = df[col]



# Now to create a new df to just have the time columns
time_df = pd.DataFrame(time_columns)

# Create new columns for time differences
time_diff_columns = {}

output_file = "TimeforEachProcessClean.xlsx"  # Replace with your desired output file name

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Original Data", index=False)  # Save the original data
    time_df.to_excel(writer, sheet_name="Time Columns", index=False)  # Save the modified columns 


# df.to_excel(output_file, index=False)

print(f"Time extracted for relevant columns and saved to a seperate sheet. Saved to {output_file}")

