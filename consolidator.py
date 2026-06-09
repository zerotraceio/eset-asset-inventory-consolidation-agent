import csv
import os

def consolidate_assets(files_dict):
    """
    Consolidates asset data from a dictionary of filenames and their content.
    files_dict: { 'filename': content_string }
    """
    assets = {}

    # --- 1. Core: Hardware Overview ---
    hw_content = files_dict.get("Computer Hardware Overview.csv", "")
    if hw_content:
        reader = csv.DictReader(hw_content.splitlines(), delimiter=';')
        for row in reader:
            name = row.get('Computer name')
            if name:
                assets[name] = row

    # --- 2. CPU Details ---
    cpu_content = files_dict.get("Computers with their CPU details.csv", "")
    if cpu_content:
        reader = csv.DictReader(cpu_content.splitlines(), delimiter=';')
        for row in reader:
            name = row.get('Computer name')
            if name and name in assets:
                assets[name]['CPU Description'] = row.get('Description')
                assets[name]['CPU Clock Speed'] = row.get('Clock speed [MHz]')

    # --- 3. RAM Details ---
    ram_content = files_dict.get("Computers with their RAM details.csv", "")
    if ram_content:
        reader = csv.DictReader(ram_content.splitlines(), delimiter=';')
        for row in reader:
            name = row.get('Group by (Computer name)')
            if name and name in assets:
                assets[name]['RAM Total MB'] = row.get('Sum (Capacity [MB])')

    # --- 4. Logged Users ---
    user_content = files_dict.get("Logged users.csv", "")
    if user_content:
        reader = csv.DictReader(user_content.splitlines(), delimiter=';')
        for row in reader:
            name = row.get('Computer name')
            if name and name in assets:
                assets[name]['Logged User'] = row.get('User name')

    # --- 5. Storage Details ---
    storage_content = files_dict.get("Per-device storage capacity and type.csv", "")
    if storage_content:
        reader = csv.DictReader(storage_content.splitlines(), delimiter=';')
        for row in reader:
            name = row.get('Computer name')
            if name and name in assets:
                assets[name]['Storage capacity [MB]'] = row.get('Storage capacity [MB]')

    # --- 6. Operating Systems ---
    os_content = files_dict.get("Operating Systems.csv", "")
    if os_content:
        reader = csv.DictReader(os_content.splitlines(), delimiter=';')
        for row in reader:
            name = row.get('Computer name')
            if name and name in assets:
                assets[name]['OS Name'] = row.get('OS name')
                assets[name]['OS Version'] = row.get('OS version')
                assets[name]['OS Platform'] = row.get('OS platform')

    # --- 7. Static Group ---
    group_content = files_dict.get("Static group name.csv", "")
    if group_content:
        reader = csv.DictReader(group_content.splitlines(), delimiter=';')
        for row in reader:
            name = row.get('Computer name')
            if name and name in assets:
                assets[name]['Static Group'] = row.get('Static group name')

    # --- 8. Last Connection (NEW) ---
    conn_content = files_dict.get("Computer last connection per device.csv", "")
    if conn_content:
        reader = csv.DictReader(conn_content.splitlines(), delimiter=';')
        for row in reader:
            name = row.get('Computer name')
            if name and name in assets:
                assets[name]['Last Connection'] = row.get('Last connected')

    # --- 9. Installed Applications (NEW) ---
    # This is 1:N (One computer, many apps). We will aggregate them into a single string.
    apps_content = files_dict.get("Installed applications per device.csv", "")
    if apps_content:
        reader = csv.DictReader(apps_content.splitlines(), delimiter=';')
        app_lists = {}
        for row in reader:
            name = row.get('Computer name')
            app_name = row.get('Application name')
            version = row.get('Application version', '')
            if name and app_name:
                app_entry = f"{app_name} (v{version})" if version else app_name
                if name not in app_lists:
                    app_lists[name] = []
                app_lists[name].append(app_entry)
        
        # Merge these lists back into the main assets dict
        for name, apps in app_lists.items():
            if name in assets:
                assets[name]['Installed Applications'] = " | ".join(apps)

    return assets

def generate_report_csv(assets):
    if not assets:
        return ""
    
    all_keys_set = set()
    for device in assets.values():
        all_keys_set.update(device.keys())
    
    # Optimized Column Order for Client Requirement
    preferred = [
        'Computer name', 'Static Group', 'Logged User', 'Last Connection',
        'Device manufacturer', 'Device model', 'Serial number',
        'OS Name', 'OS Version', 'OS Platform',
        'CPU Description', 'CPU Clock Speed', 'Number of cores',
        'RAM Total MB', 'Storage capacity [MB]', 'Installed Applications'
    ]
    sorted_keys = [k for k in preferred if k in all_keys_set]
    remaining = sorted([k for k in all_keys_set if k not in preferred])
    final_keys = sorted_keys + remaining

    import io
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=final_keys, delimiter=';')
    writer.writeheader()
    for device_data in assets.values():
        writer.writerow(device_data)
    
    return output.getvalue()
