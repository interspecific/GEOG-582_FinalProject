# author: ben grubbs
# date: 6/09/24
# description: accessing USGS groundwater data from HTML tables and saving locally as CSV files
# USGS data dashboard url: https://dashboard.waterdata.usgs.gov/app/nwd/en/?region=lower48&aoi=default


# import libraries
import pandas as pd
import arcpy

# Define URLs containing HTML tables
Newton = r'https://waterdata.usgs.gov/nwis/monthly?site_no=410428087231501&agency_cd=USGS&por_410428087231501_52464=795094,72019,52464,1976-02,2023-11&referred_module=sw&format=html_table'
LaPorte = r'https://waterdata.usgs.gov/nwis/monthly?referred_module=sw&amp;site_no=412350086512801&amp;por_412350086512801_52551=796137,72019,52551,1984-10,2024-03&amp;format=html_table&amp;date_format=YYYY-MM-DD&amp;rdb_compression=file&amp;submitted_form=parameter_selection_list'

print("Downloading data...")
try:
    # Read HTML table into a list of DataFrames
    dfs_newton = pd.read_html(Newton)
    dfs_laporte = pd.read_html(LaPorte)
    
    # Select the specific DataFrame you are interested in
    df_newton = dfs_newton[2]
    df_laporte = dfs_laporte[2]



  # Transpose the DataFrames
    df_newton = df_newton.set_index(df_newton.columns[0]).transpose().reset_index()
    df_laporte = df_laporte.set_index(df_laporte.columns[0]).transpose().reset_index()

    # drop excess columns
    df_newton = df_newton.drop(df_newton.columns[[0, 1, 38]], axis=1)
    df_laporte = df_laporte.drop(df_laporte.columns[[0, 1, 38]], axis=1)

    # Drop the 13th row
    df_newton = df_newton.drop(df_newton.index[12])
    df_laporte = df_laporte.drop(df_laporte.index[12])

    # Add latitude and longitude columns to each DataFrame
    df_newton['Latitude'] = 41.0745
    df_newton['Longitude'] = -87.4289
    df_laporte['Latitude'] = 41.3972
    df_laporte['Longitude'] = -86.8578

    # Convert 'Latitude' and 'Longitude' columns to numeric
    df_newton['Latitude'] = pd.to_numeric(df_newton['Latitude'], errors='coerce')
    df_newton['Longitude'] = pd.to_numeric(df_newton['Longitude'], errors='coerce')

    df_laporte['Latitude'] = pd.to_numeric(df_laporte['Latitude'], errors='coerce')
    df_laporte['Longitude'] = pd.to_numeric(df_laporte['Longitude'], errors='coerce')

    print("Data downloaded and parsed into dataframe")
    print(df_newton.head()) # print the first few rows
    print(df_laporte.head())
except Exception as e:
    print(f"An error occurred: {e}")

# Specify directory
output_directory = r"C:\Users\benja\OneDrive\Desktop\GEOG-582 Programming\Programming Project\USGS_Tables"


# Define file names
newton_file_name = "Newton.csv"
laporte_file_name = "LaPorte.csv"

# Define output file paths
newton_output_file = output_directory + "\\" + newton_file_name
laporte_output_file = output_directory + "\\" + laporte_file_name

# Export the DataFrames to CSV files
df_newton.to_csv(newton_output_file, index=False)
df_laporte.to_csv(laporte_output_file, index=False)

print(f"Data exported to {newton_output_file} and {laporte_output_file}")


# Verify the structure of the exported CSV files
print("Verifying the structure of the exported CSV files...")
df_newton_check = pd.read_csv(newton_output_file)
df_laporte_check = pd.read_csv(laporte_output_file)
print("Newton CSV file structure:")
print(df_newton_check.head())
print("LaPorte CSV file structure:")
print(df_laporte_check.head())





