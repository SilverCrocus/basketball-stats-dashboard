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

# Function to create a new database connection
def create_connection():
    return sqlite3.connect(database_path, check_same_thread=False)

# Function to retrieve table names from the database
@st.cache_data
def get_table_names():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        table_names = [row[0] for row in cursor.fetchall()]
    return table_names

# Function to retrieve data from a specific table for both players
@st.cache_data
def get_table_data(table_name):
    with create_connection() as conn:
        mj_table_name = f"mj_{table_name}"
        lj_table_name = f"lj_{table_name}"
        
        mj_data = pd.read_sql_query(f"SELECT * FROM {mj_table_name}", conn)
        lj_data = pd.read_sql_query(f"SELECT * FROM {lj_table_name}", conn)
    
    return mj_data, lj_data

# Function to handle the "Season" variable
@st.cache_data
def handle_season_variable(data):
    data['Season_Start'] = pd.to_datetime(data['Season'].str[:4])
    data = data.sort_values('Season_Start')
    data['Season_Numeric'] = range(1, len(data) + 1)
    return data

# Function to create a custom theme for the graphs
def create_custom_theme():
    custom_theme = go.layout.Template()
    custom_theme.layout.plot_bgcolor = '#F0F2F6'
    custom_theme.layout.paper_bgcolor = '#F0F2F6'
    custom_theme.layout.font.color = '#FFFFFF'
    custom_theme.layout.xaxis.gridcolor = '#D1D5DB'
    custom_theme.layout.yaxis.gridcolor = '#D1D5DB'
    custom_theme.layout.xaxis.zerolinecolor = '#D1D5DB'
    custom_theme.layout.yaxis.zerolinecolor = '#D1D5DB'
    custom_theme.layout.xaxis.linecolor = '#D1D5DB'
    custom_theme.layout.yaxis.linecolor = '#D1D5DB'
    return custom_theme

# Streamlit app
def main():
    # Set custom CSS styles
    st.markdown(
        """
        <style>
        body {
            background-color: #F0F2F6;
        }
        .stButton > button {
            background-color: #1D428A;
            color: white;
            padding: 10px 24px;
            border-radius: 4px;
            border: none;
            transition: background-color 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #162f5f;
        }
        .stTextInput > div > div > input {
            border-radius: 4px;
            padding: 8px;
            border: 1px solid #D1D5DB;
        }
        .stSelectbox > div > div > div > div > select {
            border-radius: 4px;
            padding: 8px;
            border: 1px solid #D1D5DB;
        }
        .stMultiSelect > div > div > div > div > ul {
            border-radius: 4px;
            border: 1px solid #D1D5DB;
        }
        .stMarkdown h1 {
            color: #FFFFFF;  # Change header color to white
        }
        .stMarkdown h2 {
            color: #FFFFFF;  # Change subheader color to white
        }
        .stImage {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Add a styled header
    st.markdown(
        """
        <div style="background-color: #1D428A; padding: 20px; color: white; text-align: center; border-radius: 4px; margin-bottom: 20px;">
            <h1 style="margin: 0;">NBA Player Stats Dashboard</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Get the list of table names from the database
    table_names = get_table_names()
    
    # Simplify table names for display
    display_names = [name.split('_', 1)[1].replace('_', ' ') for name in table_names if name.startswith('mj_')]
    
    # Create a multi-column layout
    col1, col2 = st.columns(2)
    
    with col1:
        # Select a table from the dropdown
        selected_table = st.selectbox("Select a table", [""] + display_names)
    
    with col2:
        # Select the type of graph
        graph_type = st.selectbox("Select graph type", ["Line", "Bar", "Scatter"])
    
    if selected_table:
        # Retrieve data for the selected table
        mj_data, lj_data = get_table_data(selected_table.replace(' ', '_'))
        
        # Display the graphs for both players
        st.markdown(f"<h2>{selected_table} Table</h2>", unsafe_allow_html=True)
        
        # Select the x-axis variable
        x_axis = st.selectbox("Select x-axis variable", mj_data.columns)
        
        # Select variables for the y-axis
        y_axis_variables = st.multiselect("Select y-axis variables", mj_data.columns)
        
        if y_axis_variables:
            custom_theme = create_custom_theme()
            
            for player, data in [("Michael Jordan", mj_data), ("LeBron James", lj_data)]:
                st.markdown(f"<h2>{player}</h2>", unsafe_allow_html=True)
                
                # Display player image or logo
                if player == "Michael Jordan":
                    st.image("https://c3.klipartz.com/pngpicture/445/335/sticker-png-michael-jordan-thumbnail.png", width=100)
                else:
                    st.image("https://w7.pngwing.com/pngs/184/588/png-transparent-lebron-james-with-hands-on-hips-lebron-james-cleveland-cavaliers-the-nba-finals-milwaukee-bucks-lebron-james-tshirt-game-sport-thumbnail.png", width=100)
                
                # Handle the "Season" variable
                data = handle_season_variable(data)
                
                if x_axis == 'Season':
                    x_axis_data = 'Season_Numeric'
                else:
                    x_axis_data = x_axis
                
                if graph_type == "Line":
                    fig = px.line(data, x=x_axis_data, y=y_axis_variables, template=custom_theme)
                    fig.update_layout(
                        title=f"{player} - {selected_table}",
                        xaxis_title=x_axis,
                        yaxis_title=", ".join(y_axis_variables),
                        legend_title="Variables",
                        hovermode="x",
                        legend=dict(
                            font=dict(color='white'),
                            bgcolor='rgba(50, 50, 50, 0.5)'
                        )
                    )
                    st.plotly_chart(fig)
                elif graph_type == "Bar":
                    fig = go.Figure(template=custom_theme)
                    for variable in y_axis_variables:
                        fig.add_trace(go.Bar(x=data[x_axis_data], y=data[variable], name=variable))
                    fig.update_layout(
                        title=f"{player} - {selected_table}",
                        xaxis_title=x_axis,
                        yaxis_title="Value",
                        legend_title="Variables",
                        hovermode="x",
                        legend=dict(
                            font=dict(color='white'),
                            bgcolor='rgba(50, 50, 50, 0.5)'
                        )
                    )
                    st.plotly_chart(fig)
                else:
                    fig = px.scatter(data, x=x_axis_data, y=y_axis_variables[0], template=custom_theme)
                    fig.update_layout(
                        title=f"{player} - {selected_table}",
                        xaxis_title=x_axis,
                        yaxis_title=y_axis_variables[0],
                        hovermode="x",
                        legend=dict(
                            font=dict(color='white'),
                            bgcolor='rgba(50, 50, 50, 0.5)'
                        )
                    )
                    st.plotly_chart(fig)

        else:
            st.write("Please select variables for the y-axis.")
    else:
        st.write("Please select a table from the dropdown.")

if __name__ == '__main__':
    main()