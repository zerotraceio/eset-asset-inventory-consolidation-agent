import streamlit as st
import pandas as pd
from consolidator import consolidate_assets, generate_report_csv
import io

st.set_page_config(page_title="ESET Asset Inventory Dashboard", layout="wide")

st.title("🛡️ ESET Asset Inventory Consolidation")
st.markdown("""
Upload the **detailed per-device** ESET Protect Cloud reports to generate a single, comprehensive asset inventory.
""")

# 1. File Uploads
st.sidebar.header("Upload Reports")
uploaded_files = {}

# Updated list of expected files to reflect the a detailed per-device approach
expected_files = [
    "Computer Hardware Overview.csv",
    "Computers with their CPU details.csv",
    "Computers with their RAM details.csv",
    "Logged users.csv",
    "Per-device storage capacity and type.csv",
    "Operating Systems.csv",
    "Static group name.csv",
    "Computer last connection per device.csv",
    "Installed applications per device.csv"
]

for file_name in expected_files:
    uploaded_file = st.sidebar.file_uploader(f"Upload {file_name}", type=["csv"])
    if uploaded_file:
        # Read as string to pass to our consolidator
        content = uploaded_file.getvalue().decode("utf-8-sig")
        uploaded_files[file_name] = content

# 2. Processing
if st.button("Generate Unified Report"):
    if not uploaded_files:
        st.error("Please upload at least one CSV file first.")
    else:
        with st.spinner("Consolidating data..."):
            # Get consolidated data (dict)
            assets_data = consolidate_assets(uploaded_files)
            
            if not assets_data:
                st.error("No matching asset data found. Please check your CSV formats.")
            else:
                # Result as DataFrame for preview
                df = pd.DataFrame(assets_data.values())
                st.success(f"Successfully consolidated {len(df)} devices!")
                
                # Display Results
                st.subheader("Comprehensive Asset Preview")
                st.dataframe(df, use_container_width=True)
                
                # Generate CSV report for download
                csv_report = generate_report_csv(assets_data)
                
                st.download_button(
                    label="📥 Download Comprehensive Report (.csv)",
                    data=csv_report,
                    file_name="consolidated_asset_inventory.csv",
                    mime="text/csv"
                )
                
                # Option to "Print" via a nice table
                st.markdown("---")
                st.subheader("Print-Ready Report")
                st.markdown("You can use your browser's print function (Ctrl+P) to print this table.")
                st.table(df.head(100)) 
