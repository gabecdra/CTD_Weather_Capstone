import pandas as pd
import re
import os

df = pd.read_csv('data/raw_weather.csv')

# Preview the first few records and check the data types
print("Raw Data Preview:")
print(df.head())
print(df.info())

# Clean city names (remove '*' indicating DST)
df['City'] = df['City'].str.replace('*', '', regex=False).str.strip()


# Clean temperature strings (remove '°F' and any whitespace)
def extract_temp_int(temp_str):
    if pd.isna(temp_str):
        return None
    # Find first number (including negative sign)
    match = re.search(r'-?\d+', str(temp_str))
    if match:
        return int(match.group(0))
    return None

# Extract temperature as integer (Fahrenheit)
df['Temperature_F'] = df['Temperature'].apply(extract_temp_int)
df['Temperature_F'] = df['Temperature_F'].astype('Int64') 

# Drop the original 'Temperature' column as we now have 'Temperature_F'
df.drop(columns=['Temperature'], inplace=True)


# Split 'Condition' into 'Weather_Type' and 'Temperature_Desc'
def split_condition(condition):
    if pd.isna(condition) or condition == "N/A":
        return "N/A", "N/A"
    
     # Remove trailing period
    condition = condition.rstrip('.')
    
    # Split on periods
    parts = [p.strip() for p in condition.split('.') if p.strip()]
    
    # List of common temperature descriptions for 
    temp_descriptions = [
        'Extremely hot', 'Very hot', 'Hot',
        'Warm', 'Pleasantly warm', 'Mild',
        'Cool', 'Refreshingly cool', 'Cold',
        'Freezing', 'Chilly'
    ]
    # IF Only 1 description, check if it's a temperature description or weather type
    if len(parts) == 1:
        is_temp = any(temp in parts[0] for temp in temp_descriptions)
        if is_temp:
            return "No weather data", parts[0]
        else:
            return parts[0], ""
    
    # Check if last part is temperature 
    last_part = parts[-1]
    is_temp_desc = any(temp in last_part for temp in temp_descriptions)
    
    if is_temp_desc:
        weather_type = ". ".join(parts[:-1])
        return weather_type, last_part
    else:
        return ". ".join(parts), ""
# Apply
df[['Weather_Type', 'Temperature_Desc']] = df['Condition'].apply(
    lambda x: pd.Series(split_condition(x))
)

df.drop(columns=['Condition'], inplace=True)

df = df.sort_values(by='City').reset_index(drop=True)

# Final preview of cleaned data
print("\nCleaned Data Preview:")
print(df.head())
print(df.info())
