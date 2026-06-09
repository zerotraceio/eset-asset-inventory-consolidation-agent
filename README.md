# ESET Asset Inventory Consolidation Agent

A specialized tool designed to overcome the fragmentation of asset reporting in ESET Protect Cloud. This agent allows IT administrators and MSPs to upload multiple fragmented CSV exports and consolidate them into a single, comprehensive asset inventory report.

## 🎯 Core Objective
Transform multiple ESET reports into a unified "Golden Record" per device, eliminating the need for manual merging or complex external scripts.

## ✨ Key Features
- **Multi-Source Merge**: Consolidates hardware, software, user, and connection data using `Computer Name` as the primary key.
- **Comprehensive Coverage**: Captures OS version, CPU specs, RAM, Storage, Logged Users, Static Groups, and a consolidated list of Installed Applications.
- **Interactive Dashboard**: A Streamlit-based UI for effortless file uploads and real-time data preview.
- **Exportable Reports**: Generate a print-ready table or download a consolidated CSV for use in other management tools.

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Virtual Environment (recommended)

### Setup Steps
1. **Clone the repository** (or download the folder).
2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # OR .venv\\Scripts\\activate # Windows
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Launch the dashboard**:
   ```bash
   streamlit run app.py
   ```

## 📊 Supported Reports
The tool expects the following ESET Protect Cloud exports (Detailed/Per-Device view):
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
