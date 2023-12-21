
Name: D.Karthika
Batch code: DW77DW78

# PhonePe Pulse Data Visualization and Exploration

**Introduction**

PhonePe has become a leader among digital payment platforms, serving millions of users for their daily transactions. Known for its easy-to-use design, fast and secure payment processing, and creative features, PhonePe has gained praise and recognition in the industry. The PhonePe Pulse Data Visualization and Exploration project aims to gather valuable information from PhonePe's GitHub repository, process the data, and present it using an interactive dashboard that's visually appealing. This is accomplished using Python, Streamlit, and Plotly.

**Table of Contents**

1. Key Technologies and Skills
2. Installation
3. Usage
4. Aims of the project

**Key Technologies and Skills**
- json
- Python
- Pandas
- PostgreSQL
- Streamlit
- Plotly

**Installation**

To run this project, you need to install the following packages:

git - [https://git-scm.com/downloads]

import json
import streamlit as st
import pandas as pd
import requests
import psycopg2
import plotly.express as px
import plotly.graph_objects as go

**Usage**

To use this project, follow these steps:
1. Data extraction: '''using the .ipynb'''
2. Run the Streamlit app: ```streamlit run project2.py```
3. Access the app in your browser at ```http://localhost:8501```

**Aim of the project**

1. Data Extraction:
Scripting to clone the repository and collect data.

2. Data Transformation:
Using Python and Pandas to clean and structure the data.

3. Database Insertion:
Storing transformed data in a POSTGRESQL database.

4. Dashboard Creation:
Using Streamlit and Plotly to build an interactive dashboard.

5. Data Retrieval:
Fetching data from the database to dynamically update the dashboard.

