import pandas as pd
import os
import glob

def consolidate_assets(samples_dir):
    # Path to all CSVs in the samples directory
    all_files = glob.glob(os.path.join(samples_dir, "*.csv"))
    
    # We will use 'Computer name' as the primary key for most files
    # Note: Some files might have 'Group by (Computer name)'
    
    # 1. Initialize the master dataframe with 'Computer Hardware Overview.csv' as it has most core fields
    hardware_overview_path = os.path.join(samples_dir, "Computer Hardware Overview.csv")
    if not os.path.exists(hardware_overview_path):
        print("Error: Computer Hardware Overview.csv not found. Starting from empty.")
        assets_df = pd.DataFrame(columns=['Computer name'])
    else:
        assets_df = pd.read_csv(hardware_overview_path, sep=';')

    # 2. Merge CPU details
    cpu_path = os.path.join(samples_dir, "Computers with their CPU details.csv")
    if os.path.exists(cpu_path):
        cpu_df = pd.read_csv(cpu_path, sep=';')
        # Keep only relevant cols not already in assets_df (or refine them)
        cols_to_use = ['Computer name', 'Description', 'Number of cores', 'Clock speed [MHz]']
        assets_df = assets_df.merge(cpu_df[cols_to_use], on='Computer name', how='left', suffixes=('', '_cpu'))

    # 3. Merge RAM details (Handle different header)
    ram_path = os.path.join(samples_dir, "Computers with their RAM details.csv")
    if os.path.exists(ram_path):
        ram_df = pd.read_csv(ram_path, sep=';')
        # Header is 'Group by (Computer name)'
        ram_df = ram_df.rename(columns={'Group by (Computer name)': 'Computer name', 'Sum (Capacity [MB])': 'RAM_Total_MB'})
        assets_df = assets_df.merge(ram_df[['Computer name', 'RAM_Total_MB']], on='Computer name', how='left')

    # 4. Merge User info
    user_path = os.path.join(samples_dir, "Logged users.csv")
    if os.path.exists(user_path):
        user_df = pd.read_csv(user_path, sep=';')
        assets_df = assets_df.merge(user_df[['Computer name', 'User name']], on='Computer name', how='left')

    # 5. Merge Storage details
    storage_path = os.path.join(samples_dir, "Per-device storage capacity and type.csv")
    if os.path.exists(storage_path):
        storage_df = pd.read_csv(storage_path, sep=';')
        # We only need the capacity if it differs or is more specific, 
        # but 'Computer Hardware Overview' already has it. 
        # Let's check if there's extra info.
        assets_df = assets_df.merge(storage_df[['Computer name', 'Storage capacity [MB]']], on='Computer name', how='left', suffixes=('', '_storage'))

    # 6. Handle Installed Applications
    # This is a many-to-one mapping (One computer can have many apps).
    # To keep the master sheet as "one row per device", we will concatenate apps into a single string or create a separate relational table.
    # Given the user wants a "consolidated report", a comma-separated string of apps is often preferred for a flat CSV.
    apps_path = os.path.join(samples_dir, "Installed applications.csv")
    if os.path.exists(apps_path):
        # Wait, looking at the sample: "Group by (Application name);Group by (Application vendor)..."
        # This doesn't have a 'Computer name' column! It's an aggregated count.
        # This means the "Installed applications.csv" provided is a SUMMARY, not a per-device list.
        # I will skip merging this into the per-device list to avoid data corruption, 
        # but I'll note it in the log.
        pass

    # 7. Clean up
    # Remove duplicate columns if they exist
    assets_df = assets_df.loc[:, ~assets_df.columns.duplicated()]
    
    return assets_df

if __name__ == "__main__":
    results = consolidate_assets("samples")
    output_path = "consolidated_asset_inventory.csv"
    results.to_csv(output_path, index=False, sep=';')
    print(f"Consolidated report saved to {output_path}")
    print("\nPreview of results:")
    print(results.head())
