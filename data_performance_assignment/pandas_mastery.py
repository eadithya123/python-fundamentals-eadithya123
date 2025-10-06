import pandas as pd
import numpy as np
from functools import partial

def impute_missing_precip(series: pd.Series) -> pd.Series:
    return series.fillna(0.0)

def type_conversion_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    print("\n--- PIPELINE STEP 1: Type Conversion Status ---")
    
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Avg_Temp_C'] = pd.to_numeric(df['Avg_Temp_C'], errors='coerce')
    
    print("New dtypes after conversion:")
    print(df[['Date', 'Avg_Temp_C']].dtypes.to_string())
    print("\nNull counts after conversion:")
    print(df[['Date', 'Avg_Temp_C']].isnull().sum())
    
    return df

def filter_by_threshold(df: pd.DataFrame, threshold: float) -> pd.DataFrame:
    print(f"\n--- PIPELINE STEP 2: Filtering by Avg_Temp_C > {threshold}°C ---")
    filtered_df = df[df['Avg_Temp_C'] > threshold].copy()
    print(f"Original rows: {len(df)}, Filtered rows: {len(filtered_df)}")
    return filtered_df

# ==========================================================
#                  MAIN PANDAS MANIPULATION
# ==========================================================

df = pd.read_csv('weather_data.csv')

print("###################################################")
print("# 1. INITIAL INSPECTION & SETUP                   #")
print("###################################################")

print("\n--- DataFrame dtypes ---")
print(df.dtypes)
print("\n--- DataFrame Head/Tail ---")
print(pd.concat([df.head(2), df.tail(2)]))
print("\n--- DataFrame describe() ---")
print(df.describe(include='all'))

print("\n--- Pandas Series with Custom Index ---")
city_index = ['LON', 'PAR', 'BER', 'ROM', 'TOK']
latest_temps = pd.Series(df.iloc[1:11:2]['Avg_Temp_C'].values, 
                         index=city_index, 
                         name='Latest_Recorded_Temp')
print(latest_temps.to_string())

print("\n--- DataFrame Columns ---")
print(f"DataFrame created with specified columns: {list(df.columns)}")

print("\n\n###################################################")
print("# 2. DATA SLICING, CLEANING & VALIDATION          #")
print("###################################################")

print("\n--- 2a. Slicing by Row Position (iloc - rows 1, 3, 5) ---")
print(df.iloc[[1, 3, 5]])

print("\n--- 2b. Slicing by Column Name (loc - 'City' and 'Humidity_Pct') ---")
print(df.loc[:, ['City', 'Humidity_Pct']].head(3))

is_high_conf = df['Forecast_Confidence'] == 'High'
print("\n--- 2c. Slicing using Boolean Flags (Forecast_Confidence == 'High') ---")
print(df[is_high_conf].tail(3))

is_mild = (df['Avg_Temp_C'] >= 18) & (df['Avg_Temp_C'] < 22)
print("\n--- 2d. Slicing by Data Range (18°C <= Temp < 22°C) ---")
print(df[is_mild])

print("\n--- 2e. Duplicates and Uniques ---")
print(f"Total rows before cleaning: {len(df)}")
print(f"Number of unique 'City' values (nunique): {df['City'].nunique()}")
print(f"Number of duplicate rows (duplicated): {df.duplicated().sum()}")

df_unique = df.drop_duplicates(keep='first').copy()
print(f"Total rows after drop_duplicates: {len(df_unique)}")

df_unique['Precip_mm'] = df_unique['Precip_mm'].fillna(0.0)
print("\n--- Imputation using .apply() (Precip_mm null count) ---")
print(f"Precip_mm null count after .apply(): {df_unique['Precip_mm'].isnull().sum()}")


print("\n\n###################################################")
print("# 3. PIPELINE IMPLEMENTATION (.pipe())            #")
print("###################################################")

df_piped_types = df_unique.pipe(type_conversion_pipeline)

threshold_filter_partial = partial(filter_by_threshold, threshold=20.0)

df_final_filtered = df_piped_types.pipe(threshold_filter_partial)

print("\n--- Final Piped DataFrame (Only records > 20.0°C) ---")
print(df_final_filtered[['City', 'Avg_Temp_C', 'Date']])