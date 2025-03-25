#!/bin/bash

# Install required dependencies
pip install streamlit pandas matplotlib plotly

# Run the Streamlit app
echo "Starting MasterFLO.ai Dashboard..."
streamlit run app.py
