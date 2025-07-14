import streamlit as st
import pandas as pd
import pymysql
import plotly.express as px

# Database Connection
def create_connection():
    try:
        connection = pymysql.connect(
            host = 'localhost',
            user = 'root',
            password = 'root',
            database = 'Securecheck_db',
            cursorclass = pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        st.error(f"Database Connection Error: {e}")
        return None

# Fetch Data from Database
def fetch_data(query):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                df = pd.DataFrame(result)
                return df
        finally:
            connection.close()
    else:
        return pd.DataFrame()
    
query = "SELECT * FROM Police_Checking"
data = fetch_data(query)

# Streamlit App Title
st.set_page_config(page_title = "Law Enforcement Traffic Checking Stops Records", layout = 'wide')

# Sidebar for Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Project Introduction", "Checking stops charts", "SQL Queries (Simple)", "SQL Queries (Complex)", "Natural Language Custom Prediction Summary", "Created By"])

# Page 1: introduction
if page == "Project Introduction":
    st.title("🚓 Law Enforcement Traffic Checking Stops Records")
    st.image(r"C:\Users\arun prakash\Downloads\gettyimages-53385797-612x612.jpg")
    st.subheader("🚦A Streamlit App for Exploring Traffic Checking Stops Trends by Countries")
    st.write("""
    This project analyzes police checking from different countries using a MYSQL database.
    It provides different charts for Total violations by Countries, Driver races, Stop time and Gender.
             
    **Features:**
    - View the Traffic Checking Stops Records by Countries, date, Gender and races.
    - Generate the different Charts for multiple scenarios.
    - Run predefined SQL queries to explore insights.

    **Database Used:** 'traffic_checking_stops_database.mysql'
    """)
    # ✅ Show dataframe only here
    st.dataframe(data, use_container_width=True)
else:
    print("Project Introduction not found")

#page 2: checking Stops Charts
if page == "Checking stops charts":
    st.title("🚔Checking stops charts")
    st.header("🪟 Exploring Charts")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Total stops by violation", "Total violation by Countries", "Total violation by Driver races", "Total Counts by Search Type", "Distribution of Driver Age by Arrest Status", "Total violation by Country"])

    with tab1:
        if not data.empty and 'violation' in data.columns:
            violation_data = data['violation'].value_counts().reset_index()
            violation_data.columns = ['violation', 'Count']
            fig = px.bar(violation_data, x='violation', y='Count', title="Total stops by Violation (Using Bar chart)", color='violation')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available for Violation chart(Using Bar chart).")    
    with tab2:
        if not data.empty and 'country_name' in data.columns:
            country_data = data['country_name'].value_counts().reset_index()
            country_data.columns = ['country_name', 'Count']
            fig = px.pie(country_data, names='country_name', values='Count', hole=0.4, title="Total violation by Countries (Using Donut Chart)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available for Country chart(Using Donut chart).")
    with tab3:
        if not data.empty and 'driver_race' in data.columns:
            race_data = data['driver_race'].value_counts().reset_index()
            race_data.columns = ['driver_race', 'Count']
            fig = px.pie(race_data, names='driver_race', values='Count', title="Total violation by Driver Race (Using Pie Chart)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available for Driver Race chart(Using Pie chart).")
    with tab4:
        if not data.empty and 'search_type' in data.columns:
             search_data = data['search_type'].value_counts().reset_index()
             search_data.columns = ['search_type', 'Count']
             fig = px.treemap(search_data, path=['search_type'], values='Count', title="Total Counts by Search Type (Using Treemap chart)")
             st.plotly_chart(fig, use_container_width=True)
        else:
             st.warning("No data available for search type(Using Treemap chart).")
    with tab5:
        if not data.empty and 'is_arrested' in data.columns and 'driver_age' in data.columns:
            fig = px.box(data, x='is_arrested', y='driver_age', color='is_arrested', title="Distribution of Driver Age by Arrest Status (Using Box Plot chart)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available for Arrest Status or Driver Age (Using Box Plot chart).")
    with tab6:
        if not data.empty and 'country_name' in data.columns:
            country_data = data['country_name'].value_counts().reset_index()
            country_data.columns = ['country_name', 'Count']
            fig = px.scatter_geo(
                country_data,
                locations='country_name',         
                locationmode='country names',     
                size='Count',                     
                color='country_name',             
                hover_name='country_name',
                title="Total Violations by Country (Using Scatter Geo Chart)")
            fig.update_geos(showcountries=True, projection_type="natural earth")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available for Country chart(Using Scatter Geo chart).")
else:
    print("Checking stops charts not found")

#page 3: SQL Queries (Simple)
if page == "SQL Queries (Simple)":
    st.title("🗓️ SQL Queries (Simple)")
    selected_query = st.selectbox("Choose a Query", [
    "What are the top 10 vehicle_Number involved in drug-related stops?",
    "Which vehicles were most frequently searched?",
    "Which driver age group had the highest arrest rate?",
    "What is the gender distribution of drivers stopped in each country?",
    "Which race and gender combination has the highest search rate?",
    "What time of day sees the most traffic stops?",
    "What is the average stop duration for different violations?",
    "Are stops during the night more likely to lead to arrests?",
    "Which violations are most associated with searches or arrests?",
    "Which violations are most common among younger drivers (<25)?",
    "Is there a violation that rarely results in search or arrest?",
    "Which countries report the highest rate of drug-related stops?",
    "What is the arrest rate by country and violation?",
    "Which country has the most stops with search conducted?"
])
    simple_query = {
    "What are the top 10 vehicle_Number involved in drug-related stops?" : "SELECT vehicle_number, COUNT(*) AS stop_count FROM Police_Checking WHERE drugs_related_stop = 'Yes' GROUP BY vehicle_number ORDER BY stop_count DESC LIMIT 10;",
    "Which vehicles were most frequently searched?" : "SELECT vehicle_number, COUNT(*) AS search_count FROM Police_Checking WHERE search_conducted = 'Yes' GROUP BY vehicle_number ORDER BY search_count DESC LIMIT 10;",
    "Which driver age group had the highest arrest rate?" : "SELECT CASE WHEN driver_age < 18 THEN 'Under 18' WHEN driver_age BETWEEN 18 AND 25 THEN '18-25' WHEN driver_age BETWEEN 26 AND 35 THEN '26-35' WHEN driver_age BETWEEN 36 AND 50 THEN '36-50' WHEN driver_age BETWEEN 51 AND 65 THEN '51-65' ELSE '66+' END AS age_group, COUNT(*) AS total_stops, SUM(CASE WHEN is_arrested = 'Yes' THEN 1 ELSE 0 END) AS total_arrests, ROUND(SUM(CASE WHEN is_arrested = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS arrest_rate_percentage FROM Police_Checking WHERE driver_age IS NOT NULL GROUP BY age_group ORDER BY arrest_rate_percentage DESC;",
    "What is the gender distribution of drivers stopped in each country?" : "SELECT country_name, driver_gender, COUNT(*) AS stop_count FROM Police_Checking WHERE country_name IS NOT NULL AND driver_gender IS NOT NULL GROUP BY country_name, driver_gender ORDER BY country_name, driver_gender;",
    "Which race and gender combination has the highest search rate?" : "SELECT driver_race, driver_gender, COUNT(*) AS total_stops, SUM(search_conducted = 'Yes') AS total_searches, ROUND(100.0 * SUM(search_conducted = 'Yes') / COUNT(*), 2) AS search_rate_percentage FROM Police_Checking WHERE driver_race IS NOT NULL AND driver_gender IS NOT NULL GROUP BY driver_race, driver_gender ORDER BY search_rate_percentage DESC LIMIT 1;",
    "What time of day sees the most traffic stops?" : "SELECT HOUR(stop_time) AS stop_hour, COUNT(*) AS stop_count FROM Police_Checking WHERE stop_time IS NOT NULL GROUP BY stop_hour ORDER BY stop_count DESC LIMIT 1;",
    "What is the average stop duration for different violations?" : "SELECT violation, AVG(stop_duration) AS average_duration FROM Police_Checking WHERE stop_duration IS NOT NULL GROUP BY violation;",
    "Are stops during the night more likely to lead to arrests?" : "SELECT CASE WHEN stop_time BETWEEN '06:00:00' AND '19:59:59' THEN 'Day' ELSE 'Night' END AS time_period, AVG(is_arrested = 'Yes') AS arrest_rate FROM Police_Checking WHERE stop_time IS NOT NULL AND is_arrested IS NOT NULL GROUP BY time_period;",
    "Which violations are most associated with searches or arrests?" : "SELECT violation, COUNT(*) AS total FROM Police_Checking WHERE search_conducted = 'Yes' OR is_arrested = 'Yes' GROUP BY violation ORDER BY total DESC;",
    "Which violations are most common among younger drivers (<25)?" : "SELECT violation, COUNT(*) AS total FROM Police_Checking WHERE driver_age < 25 GROUP BY violation ORDER BY total DESC;",
    "Is there a violation that rarely results in search or arrest?" : "SELECT violation, COUNT(*) AS total_stops, SUM(search_conducted = 'Yes' OR is_arrested = 'Yes') AS search_or_arrest_count FROM Police_Checking GROUP BY violation ORDER BY search_or_arrest_count ASC LIMIT 1;",
    "Which countries report the highest rate of drug-related stops?" : "SELECT country_name, ROUND(SUM(drugs_related_stop = 'Yes') * 100.0 / COUNT(*), 2) AS drug_stop_rate FROM Police_Checking GROUP BY country_name ORDER BY drug_stop_rate DESC;",
    "What is the arrest rate by country and violation?" : "SELECT country_name, violation, ROUND(SUM(is_arrested = 'Yes') * 100.0 / COUNT(*), 2) AS arrest_rate FROM Police_Checking GROUP BY country_name, violation ORDER BY arrest_rate DESC;",
    "Which country has the most stops with search conducted?" : "SELECT country_name, COUNT(*) AS search_count FROM Police_Checking WHERE search_conducted = 'Yes' GROUP BY country_name ORDER BY search_count DESC LIMIT 1;",
}
    
    if st.button("Run Query"):
        result = fetch_data(simple_query[selected_query])
        if not result.empty:
            st.write(result)
        else:
            st.warning("No results found for the selected query.")
else:
    print("SQL Queries (Simple) was not found")

#page 4: SQL Queries (Complex)
if page == "SQL Queries (Complex)":
    st.title("🗓️ SQL Queries (Complex)")
    selected_query = st.selectbox("Choose a Query", [
    "Yearly Breakdown of Stops and Arrests by Country (Using Subquery and Window Functions)",
    "Driver Violation Trends Based on Age and Race (Join with Subquery)",
    "Time Period Analysis of Stops (Joining with Date Functions) , Number of Stops by Year,Month, Hour of the Day",
    "Violations with High Search and Arrest Rates (Window Function)",
    "Driver Demographics by Country (Age, Gender, and Race)",
    "Top 5 Violations with Highest Arrest Rates"
])
    complex_query = {
    "Yearly Breakdown of Stops and Arrests by Country (Using Subquery and Window Functions)" : "SELECT country_name, year, total_stops, total_arrests, ROUND((total_arrests * 100.0) / total_stops, 2) AS arrest_rate_percent, RANK() OVER (PARTITION BY year ORDER BY total_arrests DESC) AS arrest_rank FROM (SELECT country_name, YEAR(stop_date) AS year, COUNT(*) AS total_stops, SUM(CASE WHEN is_arrested = 'Yes' THEN 1 ELSE 0 END) AS total_arrests FROM Police_Checking GROUP BY country_name, YEAR(stop_date)) AS yearly_data;",
    "Driver Violation Trends Based on Age and Race (Join with Subquery)" : "SELECT pc.driver_age, pc.driver_race, pc.violation, COUNT(*) AS total_violations FROM Police_Checking pc INNER JOIN (SELECT driver_age, driver_race FROM Police_Checking GROUP BY driver_age, driver_race) AS demo ON pc.driver_age = demo.driver_age AND pc.driver_race = demo.driver_race GROUP BY pc.driver_age, pc.driver_race, pc.violation ORDER BY total_violations DESC;",
    "Time Period Analysis of Stops (Joining with Date Functions) , Number of Stops by Year,Month, Hour of the Day" : "SELECT YEAR(STR_TO_DATE(stop_date, '%Y-%m-%d')) AS stop_year, MONTH(STR_TO_DATE(stop_date, '%Y-%m-%d')) AS stop_month, HOUR(STR_TO_DATE(stop_time, '%H:%i:%s')) AS stop_hour, COUNT(*) AS total_stops FROM Police_Checking GROUP BY stop_year, stop_month, stop_hour ORDER BY stop_year, stop_month, stop_hour;",
    "Violations with High Search and Arrest Rates (Window Function)" : "SELECT DISTINCT violation, COUNT(*) OVER (PARTITION BY violation) AS total_stops, SUM(CASE WHEN search_conducted='Yes' THEN 1 ELSE 0 END) OVER (PARTITION BY violation) AS total_searches, SUM(CASE WHEN is_arrested='Yes' THEN 1 ELSE 0 END) OVER (PARTITION BY violation) AS total_arrests FROM Police_Checking;",
    "Driver Demographics by Country (Age, Gender, and Race)" : "SELECT country_name, AVG(driver_age) AS avg_age, COUNT(*) AS total_drivers, COUNT(DISTINCT driver_gender) AS gender_variety, COUNT(DISTINCT driver_race) AS race_variety FROM Police_Checking GROUP BY country_name;",
    "Top 5 Violations with Highest Arrest Rates" : "SELECT violation, ROUND(SUM(is_arrested='Yes')*100.0/COUNT(*), 2) AS arrest_rate FROM Police_Checking GROUP BY violation ORDER BY arrest_rate DESC LIMIT 5;",
}
    if st.button("Run Query"):
        result = fetch_data(complex_query[selected_query])
        if not result.empty:
            st.write(result)
        else:
            st.warning("No results found for the selected query.")
else:
    print("SQL Queries (Complex) was not found")

#page 5: Natural Language Custom Prediction Summary
if page == "Natural Language Custom Prediction Summary":
    st.title("🔎 Natural Language Custom Prediction Summary")
    st.markdown("Fill in the details below to get a natural language custom prediction of the stop outcome & violation based on the existing data.")
    st.header("📃 To Find the data in Police_Checking & Predict Outcome and Violation")

# Input form for all fields (Excluding outputs)
    with st.form("new_data_form"):
        stop_date = st.date_input("Stop Date")
        stop_time = st.time_input("Stop Time")
        country_name = st.selectbox("Country Name", ["Canada", "India", "USA"])
        driver_gender = st.selectbox("Driver Gender", ["Male", "Female"])
        driver_age = st.number_input("Driver Age", min_value=16, max_value=100)
        driver_race = st.selectbox("Driver Race", ["Asian", "Black", "Hispanic", "Other", "White"])
        search_conducted = st.selectbox("Was a Search Conducted?", ["0", "1"])
        search_type = st.selectbox("Serach Type", ["Frisk", "Vehicle Search", "Notspecified"])
        drugs_related_stop = st.selectbox("Was it Drug Related?", ["0", "1"])
        stop_duration = st.selectbox("Stop Duration", ["0-15 Min", "16-30 Min", "30+ Min"])
        vehicle_number = st.text_input("Vehicle Number")

        submitted = st.form_submit_button("Predict Stop Outcome & Violation")

        if submitted:
            # filter data for prediction
            filtered_data = data[
                (data['driver_gender'] == driver_gender) &
                (data['driver_age'] == driver_age) &
                (data['search_conducted'] == int(search_conducted)) &
                (data['stop_duration'] == stop_duration) &
                (data['drugs_related_stop'] == int(drugs_related_stop))
            ]

            # Predict stop_outcome & violation
            if not filtered_data.empty:
                predicted_outcome = filtered_data['stop_outcome'].mode()[0]
                predicted_violation = filtered_data['violation'].mode()[0]
            else:
                predicted_outcome = "Warning"  # Default Fallback
                predicted_violation = "Speeding"  # Default Fallback
            
            # Natural Language Predict Summary
            search_text = "A Search was Conducted" if int(search_conducted) else "No search was conducted"
            drug_text = "was drug-related" if int(drugs_related_stop) else "was not drug-related"

            st.markdown(f"""
            👓 **Prediction Summary**
                        
            - **Predicted Outcome:** **{predicted_outcome}** 
            - **Predicted Violation:** **{predicted_violation}**

            📒 A {driver_age}-year old {driver_gender} driver in {country_name} was stopped at {stop_time.strftime('%I:%M %p')} on {stop_date.strftime('%Y-%m-%d')}.
            {search_text}, and the stop {drug_text}.    
            Stop Duration: **{stop_duration}**.        
            Vehicle Number: **{vehicle_number}**.
            """)
else:
    print("Natural Language Custom Prediction Summary was not found")

# page 6: Created By
if page == "Created By":
    st.title("☀️ Creator of this project")
    st.write("""
    **Developed by:**  **P. SHANMUGA PANDIAN**         
    **Skills:**  **Python, SQL, Streamlit, Pandas, Plotly**         
    **Reference by:**  **VINODHINI MAM, GOMATHI MAM & SHADIYA MAM**              
    """)