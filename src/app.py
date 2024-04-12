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

# Function to generate summary statistics for a player
def generate_summary_statistics(player, data, selected_variables):
    st.subheader(f"{player} - Summary")

    if len(selected_variables) > 0:
        # Calculate and display averages for selected variables
        averages = data[selected_variables].mean()
        st.subheader("Averages")
        st.table(averages)

        # Calculate and display totals for selected variables
        totals = data[selected_variables].sum()
        st.subheader("Totals")
        st.table(totals)
    else:
        st.write("No variables selected for summary statistics.")

# Streamlit app
def main():
    # Set custom CSS styles
    st.markdown(
        """
        <style>
        .stButton > button {
            background-color: #1D428A;
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

    # Add a styled header
    st.markdown(
        """
        <div style="background-color: #1D428A; padding: 20px; color: white; text-align: center;">
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
        st.subheader(f"{selected_table} Table")
        
        # Select the x-axis variable
        x_axis = st.selectbox("Select x-axis variable", mj_data.columns)
        
        # Select variables for the y-axis
        y_axis_variables = st.multiselect("Select y-axis variables", mj_data.columns)
        
        if y_axis_variables:
            # Create separate graphs for each player
            for player, data in [("Michael Jordan", mj_data), ("LeBron James", lj_data)]:
                st.subheader(player)
                
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
                    fig = px.line(data, x=x_axis_data, y=y_axis_variables)
                    fig.update_layout(
                        title=f"{player} - {selected_table}",
                        xaxis_title=x_axis,
                        yaxis_title=", ".join(y_axis_variables),
                        legend_title="Variables",
                        hovermode="x",
                        plot_bgcolor="#1D428A",
                        paper_bgcolor="#1D428A",
                        font=dict(color="white"),
                        legend=dict(font=dict(color="white")),
                        xaxis=dict(gridcolor="rgba(255, 255, 255, 0.2)"),
                        yaxis=dict(gridcolor="rgba(255, 255, 255, 0.2)"),
                    )
                    st.plotly_chart(fig)
                elif graph_type == "Bar":
                    fig = go.Figure()
                    for variable in y_axis_variables:
                        fig.add_trace(go.Bar(x=data[x_axis_data], y=data[variable], name=variable))
                    fig.update_layout(
                        title=f"{player} - {selected_table}",
                        xaxis_title=x_axis,
                        yaxis_title="Value",
                        legend_title="Variables",
                        hovermode="x",
                        plot_bgcolor="#1D428A",
                        paper_bgcolor="#1D428A",
                        font=dict(color="white"),
                        legend=dict(font=dict(color="white")),
                        xaxis=dict(gridcolor="rgba(255, 255, 255, 0.2)"),
                        yaxis=dict(gridcolor="rgba(255, 255, 255, 0.2)"),
                    )
                    st.plotly_chart(fig)
                else:
                    fig = px.scatter(data, x=x_axis_data, y=y_axis_variables[0])
                    fig.update_layout(
                        title=f"{player} - {selected_table}",
                        xaxis_title=x_axis,
                        yaxis_title=y_axis_variables[0],
                        hovermode="x",
                        plot_bgcolor="#1D428A",
                        paper_bgcolor="#1D428A",
                        font=dict(color="white"),
                        xaxis=dict(gridcolor="rgba(255, 255, 255, 0.2)"),
                        yaxis=dict(gridcolor="rgba(255, 255, 255, 0.2)"),
                    )
                    st.plotly_chart(fig)
                
                # Generate summary statistics for the player
                generate_summary_statistics(player, data, y_axis_variables)

                # Display individual achievements and notable records/milestones
                if player == "Michael Jordan":
                    st.subheader("Michael Jordan")
                    st.markdown("#### Individual Achievements")
                    st.markdown("1. **Six NBA Finals MVP Awards**: Jordan's unmatched ability to perform in high-stakes games earned him Finals MVP in every championship series he competed in.")
                    st.markdown("2. **Five MVP Awards**: Jordan's excellence was recognized with five MVP titles throughout his career, showcasing his dominance in the league during his playing years.")
                    st.markdown("3. **Defensive Player of the Year (1988)**: This award highlighted Jordan's exceptional defensive skills, making him a complete player who excelled on both ends of the court.")
                    st.markdown("#### Notable Records/Milestones")
                    st.markdown("1. **10 Scoring Titles**: Jordan led the NBA in scoring for ten seasons, a testament to his scoring ability and offensive prowess.")
                    st.markdown("2. **Two Olympic Gold Medals**: His achievements on the international stage include gold medals in 1984 and 1992, the latter with the 'Dream Team,' which is often considered the greatest team assembled in any sport.")
                else:
                    st.subheader("LeBron James")
                    st.markdown("#### Individual Achievements")
                    st.markdown("1. **Four NBA Finals MVP Awards**: LeBron's impact in the finals continues to be profound, with four Finals MVP awards that underscore his crucial role in his teams' successes.")
                    st.markdown("2. **Four MVP Awards**: Recognized as the most valuable player four times, LeBron has been a dominant force throughout his career.")
                    st.markdown("#### Notable Records/Milestones")
                    st.markdown("1. **NBA's All-Time Leading Scorer**: LeBron broke Kareem Abdul-Jabbar's record to become the all-time leading scorer in NBA history, a monumental achievement highlighting his longevity and scoring ability.")
                    st.markdown("2. **All-NBA Selections**: LeBron holds the record for the most All-NBA Team selections, demonstrating his consistency and excellence over a long career.")
                    st.markdown("3. **Two Olympic Gold Medals**: His success isn't just limited to the NBA; LeBron has also been a key player for the USA in the Olympics, securing gold medals in 2008 and 2012.")
        else:
            st.write("Please select variables for the y-axis.")
    else:
        st.write("Please select a table from the dropdown.")

if __name__ == '__main__':
    main()