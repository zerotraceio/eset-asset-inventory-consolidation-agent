# ESET Asset Inventory Consolidation Agent

A specialized tool designed to overcome the fragmentation of asset reporting in ESET Protect Cloud. This agent allows IT administrators and MSPs to upload multiple fragmented CSV exports and consolidate them into a single, comprehensive asset inventory report.

## 🎯 Core Objective
Transform multiple ESET reports into a unified "Golden Record" per device, eliminating the need for manual merging or complex external scripts.

## ✨ Key Features
- **Multi-Source Merge**: Consolidates hardware, software, user, and connection data using `Computer Name` as the primary key.
- **Comprehensive Coverage**: Captures OS version, CPU specs, RAM, Storage, Logged Users, Static Groups, and a consolidated list of Installed Applications.
- **Interactive Dashboard**: A Streamlit-based UI for effortless file uploads and real-time data preview.
- **Exportable Reports**: Generate a print-ready table or download a consolidated CSV for use in other management tools.
- **Prebuilt Report Templates**: Includes a `.dat` export file that can be imported directly into ESET PROTECT to standardize these reports across multiple client environments.

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Virtual Environment (recommended)

### Setup Steps
1. **Clone the repository**
   ```bash
   git clone https://github.com/zerotraceio/eset-asset-inventory-consolidation-agent.git
   cd eset-asset-inventory-consolidation-agent
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Linux/macOS
   python3 -m venv .venv
   source .venv/bin/activate

   # Windows
   python -m venv .venv
   .venv\\Scripts\\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the dashboard**
   ```bash
   streamlit run app.py
   ```

## 📑 How to Import ESET Report Templates
To ensure the consolidation agent works perfectly, you must use the correct report formats. We have provided a `.dat` file containing the precisely configured templates.

### Steps to import the templates into ESET PROTECT Cloud:
1. Log into your **ESET PROTECT Cloud** console.
2. Navigate to **Reports** in the left-hand menu.
3. Click the **Import** button (located in the top-right toolbar).
4. Select the file: `eset-asset-inventory-consolidation.dat`.
5. Once the import is complete, you will find a new category named **"ESET Asset Inventory Consolidation"** in your reports list.
6. To get the data for this tool, simply run each report within this category and export the results as **CSV**.

## 📊 Supported Reports
The tool expects the following CSV exports (Detailed/Per-Device view) from the imported category:
- `Computer Hardware Overview.csv`
- `Computers with their CPU details.csv`
- `Computers with their RAM details.csv`
- `Logged users.csv`
- `Per-device storage capacity and type.csv`
- `Operating Systems.csv`
- `Static group name.csv`
- `Computer last connection per device.csv`
- `Installed applications per device.csv`

## 📂 Project Structure
- `app.py`: Streamlit frontend.
- `consolidator.py`: Core data processing logic.
- `requirements.txt`: Python dependencies.
- `README.md`: Project documentation.
- `eset-asset-inventory-consolidation.dat`: ESET PROTECT importable template package.
