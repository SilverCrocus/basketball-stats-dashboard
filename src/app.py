import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Set page title and favicon
st.set_page_config(page_title="NBA Player Stats Dashboard", page_icon=":basketball:")

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

# Function to handle the "Season" variable
def handle_season_variable(data):
    data['Season_Start'] = pd.to_datetime(data['Season'].str[:4])
    data = data.sort_values('Season_Start')
    data['Season_Numeric'] = range(len(data))
    return data

# Streamlit app
def main():
    # Set custom CSS styles
    st.markdown(
        """
        <style>
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 24px;
            border-radius: 4px;
            border: none;
        }
        .stTextInput > div > div > input {
            border-radius: 4px;
            padding: 8px;
        }
        .stSelectbox > div > div > div > div > select {
            border-radius: 4px;
            padding: 8px;
        }
        .stMultiSelect > div > div > div > div > ul {
            border-radius: 4px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

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
        
        # Select variables for the y-axis
        y_axis_variables = st.multiselect("Select y-axis variables", mj_data.columns)
        
        if y_axis_variables:
            # Create separate graphs for each player
            for player, data in [("Michael Jordan", mj_data), ("LeBron James", lj_data)]:
                st.subheader(player)
                
                # Handle the "Season" variable
                data = handle_season_variable(data)
                
                if x_axis == 'Season':
                    x_axis_data = 'Season_Numeric'
                else:
                    x_axis_data = x_axis
                
                if graph_type == "Line":
                    fig = px.line(data, x=x_axis_data, y=y_axis_variables)
                    st.plotly_chart(fig)
                elif graph_type == "Bar":
                    fig = go.Figure()
                    for variable in y_axis_variables:
                        fig.add_trace(go.Bar(x=data[x_axis_data], y=data[variable], name=variable))
                    st.plotly_chart(fig)
                else:
                    fig = px.scatter(data, x=x_axis_data, y=y_axis_variables[0])
                    st.plotly_chart(fig)
        else:
            st.write("Please select variables for the y-axis.")
    else:
        st.write("Please select a table from the dropdown.")

if __name__ == '__main__':
    main()