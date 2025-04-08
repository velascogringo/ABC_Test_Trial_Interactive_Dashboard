# ABC Test Trial Interactive Dashboard (Streamlit App Deployment)

## Table of Contents

- [Introduction](#introduction)
- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Usage](#usage)
- [Contributing](#contributing)

## Introduction 
This repository contains the source code for ABC Test Trial Interactive Dashboard built with Streamlit. The application provides an interactive, real-time overview of clinical trial performance metrics, allowing users to monitor trial participant status, manage and resolve data queries, track safety and SAE (Serious Adverse Events) data, evaluate CRF (Case Report Form) data entry status & assess subject level data cleaning progress.

📌 **DISCLAIMER: The data used in this dashboard is manually generated or anonymized and does NOT represent actual clinical trial data. This dashboard was created solely for educational and demonstration purposes.**

## About
The **ABC Test Trial Interactive Dashboard** is designed to support sponsors, clinical research associates (CRAs), data managers, and trial coordinators in gaining real-time insights into the quality, completeness, and integrity of clinical trial data. 

This interactive tool facilitates efficient tracking of:
- **Participant progress and status**
- **Case Report Form (CRF) completion**
- **Query management and resolution**
- **Serious Adverse Event (SAE) reconciliation**
- **Data cleaning activities**

By **centralizing critical data review functions into a single platform**, the dashboard ensures **data integrity**, promotes **protocol compliance**, and enhances **operational efficiency throughout the lifecycle of a clinical study**.

## Features

- **Holistic View of Study Status**  
  Provides a comprehensive, study-wide perspective on participant progress, data quality, and site performance across all regions and trial phases.

- **Downloadable Data Visuals**  
  Users can download or export datasets from each visual or table, enabling offline review, documentation, and reporting.

- **Interactive and Real-Time Insights**  
  Visuals automatically update with the latest uploaded data, allowing stakeholders to make informed decisions quickly and efficiently.

- **Dynamic Query Management**  
  Tracks the status of open, answered, and closed queries to support timely and complete resolution of data issues. Provides insights into site response times, identifies top recurring queries, highlights aging 
  or overdue queries, and displays query distribution across sites and subjects. Also includes metrics for the number of active/open queries to help prioritize data cleaning efforts.
  
- **CRF Completion and Data Entry Tracking**  
  Monitors the status of case report forms (CRFs), highlighting missing, incomplete, or unverified entries.

- **SAE and Vendor Reconciliation**  
  Verifies consistency between Serious Adverse Events (SAEs) in EDC and Safety team  to ensure regulatory compliance and data integrity.

- **User-Friendly Navigation**  
  Intuitive sidebar navigation and section-based layout make it easy to explore different aspects of the clinical trial.

- **Supports Protocol Compliance and Database Lock Readiness**  
  Helps identify subjects ready for lock and sites needing further attention, improving trial close-out planning.



## Tech Stack
- Python: Programming language used for data manipulation, analysis, and visualization.

- Streamlit: Web application framework used for building interactive data dashboards.

- Pandas: Data manipulation library used for data preprocessing and analysis.

- NumPy: Library used for numerical computing and array operations.

- Matplotlib: Visualization library used for creating static plots and charts.

- Plotly: Interactive visualization library used for creating interactive plots and dashboards.


## Usage

To access the ABC Test Trial Interactive Dashboard application, simply visit the deployed Streamlit web app at:

https://abc-test-trial-interactive-dashboard.streamlit.app/

**Note: If the application has not been used for a while, it may go to sleep. If prompted to wake the application, please do so kindly wait for the app to load completely.**

## Contributing

Contributions are welcome! If you'd like to contribute, please feel free to fork the repository, make your changes, and submit a pull request. For major changes, please open an issue first to discuss the proposed modifications.
