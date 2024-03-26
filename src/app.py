import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to the database file
database_path = os.path.join(current_dir, '..', 'databases', 'nba_stats.db')

# Connect to the SQLite database
conn = sqlite3.connect(database_path)

# Function to retrieve table names from the database
def get_table_names():
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_names = [row[0] for row in cursor.fetchall()]
    return table_names

# Function to retrieve data from a specific table for both players
def get_table_data(table_name):
    mj_table_name = f"mj_{table_name}"
    lj_table_name = f"lj_{table_name}"
    
    mj_data = pd.read_sql_query(f"SELECT * FROM {mj_table_name}", conn)
    lj_data = pd.read_sql_query(f"SELECT * FROM {lj_table_name}", conn)
    
    return mj_data, lj_data

# Function to convert the x-axis variable to a datetime format
def convert_to_datetime(value):
    if isinstance(value, str) and '-' in value:
        year = value.split('-')[0]
        return pd.to_datetime(year, format='%Y')
    else:
        return pd.to_datetime(value)

# Streamlit app
def main():
    st.title("NBA Player Stats Dashboard")
    
    # Get the list of table names from the database
    table_names = get_table_names()
    
    # Simplify table names for display
    display_names = [name.split('_', 1)[1].replace('_', ' ') for name in table_names if name.startswith('mj_')]
    
    # Select a table from the dropdown
    selected_table = st.selectbox("Select a table", [""] + display_names)
    
    if selected_table:
        # Retrieve data for the selected table
        mj_data, lj_data = get_table_data(selected_table.replace(' ', '_'))
        
        # Display the graphs for both players
        st.subheader(f"{selected_table} Table")
        
        # Select the x-axis variable
        x_axis = st.selectbox("Select x-axis variable", mj_data.columns)
        
        # Select the type of graph
        graph_type = st.selectbox("Select graph type", ["Line", "Bar", "Scatter"])
        
        # Select variables for the graph
        variables = st.multiselect("Select variables", mj_data.columns)
        
        if variables:
            # Create separate graphs for each player
            for player, data in [("Michael Jordan", mj_data), ("LeBron James", lj_data)]:
                st.subheader(player)
                
                # Convert x-axis variable to datetime
                data[x_axis] = data[x_axis].apply(convert_to_datetime)
                
                if graph_type == "Line":
                    fig = px.line(data, x=x_axis, y=variables)
                    st.plotly_chart(fig)
                elif graph_type == "Bar":
                    fig = px.bar(data, x=x_axis, y=variables)
                    st.plotly_chart(fig)
                else:
                    fig = px.scatter(data, x=variables[0], y=variables[1])
                    st.plotly_chart(fig)
        else:
            st.write("Please select variables to plot.")
    else:
        st.write("Please select a table from the dropdown.")

if __name__ == '__main__':
    main()