import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Global Weather Dashboard",
    layout="wide"
)


# DATABASE CONFIGURATION

DB_FILE = 'weather_final.db'
TABLE_NAME = 'weather_final'


# TITLE

st.title("Global Weather Dashboard")
st.write("""
This dashboard shows weather data for capital cities around the world.
""")


# LOAD DATA

conn = sqlite3.connect('weather_final.db')
df = pd.read_sql_query("SELECT * FROM weather_final", conn)
conn.close()


df['Temp_F'] = df['Temperature_F']


# SIDEBAR FILTERS

st.sidebar.header("Filters")

min_temp = int(df['Temp_F'].min())
max_temp = int(df['Temp_F'].max())
temp_range = st.sidebar.slider(
    "Temperature Range (F)",
    min_value=min_temp,
    max_value=max_temp,
    value=(min_temp, max_temp)
)

weather_types = ["All"] + sorted(df['Weather_Type'].dropna().unique().tolist())
selected_weather = st.sidebar.selectbox("Weather Type", weather_types)

temp_descs = ["All"] + sorted(df['Temperature_Desc'].dropna().unique().tolist())
selected_temp_desc = st.sidebar.selectbox("Temperature Description", temp_descs)

city_search = st.sidebar.text_input("Search City", "")

# APPLY FILTERS

filtered_df = df.copy()

filtered_df = filtered_df[
    (filtered_df['Temp_F'] >= temp_range[0]) &
    (filtered_df['Temp_F'] <= temp_range[1])
]

if selected_weather != "All":
    filtered_df = filtered_df[filtered_df['Weather_Type'] == selected_weather]

if selected_temp_desc != "All":
    filtered_df = filtered_df[filtered_df['Temperature_Desc'] == selected_temp_desc]

if city_search:
    filtered_df = filtered_df[
        filtered_df['City'].str.contains(city_search, case=False, na=False)
    ]


# METRICS

st.subheader("Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Cities", len(filtered_df))

with col2:
    avg_temp = filtered_df['Temp_F'].mean() if len(filtered_df) > 0 else 0
    st.metric("Average Temp", f"{avg_temp:.1f} F")

with col3:
    max_temp = filtered_df['Temp_F'].max() if len(filtered_df) > 0 else 0
    st.metric("Hottest", f"{max_temp:.0f} F")

with col4:
    min_temp = filtered_df['Temp_F'].min() if len(filtered_df) > 0 else 0
    st.metric("Coldest", f"{min_temp:.0f} F")

st.divider()


# CHART 1: Top 20 Hottest Cities

st.subheader("Top 20 Hottest Cities")

if len(filtered_df) > 0:
    top_hot = filtered_df.nlargest(20, 'Temp_F')
    fig1 = px.bar(
        top_hot,
        x='City',
        y='Temp_F',
        color='Temp_F',
        color_continuous_scale='Reds',
        labels={'Temp_F': 'Temperature (F)', 'City': 'City'}
    )
    fig1.update_layout(xaxis_tickangle=-45, height=500)
    st.plotly_chart(fig1, width='stretch')
else:
    st.warning("No cities match your filters.")


# CHART 2: Temperature Distribution

st.subheader("Temperature Distribution")

col1, col2 = st.columns(2)

with col1:
    if len(filtered_df) > 0:
        fig2 = px.histogram(
            filtered_df,
            x='Temp_F',
            nbins=30,
            color='Temperature_Desc',
            labels={'Temp_F': 'Temperature (F)', 'count': 'Cities'}
        )
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, width='stretch')

with col2:
    if len(filtered_df) > 0:
        avg_by_weather = (
            filtered_df.groupby('Weather_Type')['Temp_F']
            .mean()
            .reset_index()
            .sort_values('Temp_F', ascending=True)
            .head(10)
        )
        fig3 = px.bar(
            avg_by_weather,
            x='Temp_F',
            y='Weather_Type',
            orientation='h',
            color='Temp_F',
            color_continuous_scale='Viridis',
            labels={'Temp_F': 'Average Temp (F)', 'Weather_Type': 'Weather Type'}
        )
        fig3.update_layout(height=400)
        st.plotly_chart(fig3, width='stretch')


# CHART 3: Weather Type Distribution

st.subheader("Weather and Temperature Type Distribution")

col1, col2 = st.columns(2)

with col1:
    if len(filtered_df) > 0:
        weather_counts = filtered_df['Weather_Type'].value_counts().head(10).reset_index()
        weather_counts.columns = ['Weather_Type', 'Count']
        fig4 = px.pie(
            weather_counts,
            values='Count',
            names='Weather_Type',
            hole=0.4
        )
        fig4.update_layout(height=400)
        st.plotly_chart(fig4, width='stretch')

with col2:
    if len(filtered_df) > 0:
        temp_desc_counts = filtered_df['Temperature_Desc'].value_counts().reset_index()
        temp_desc_counts.columns = ['Temperature_Desc', 'Count']
        fig5 = px.bar(
            temp_desc_counts,
            x='Temperature_Desc',
            y='Count',
            color='Temperature_Desc',
            labels={'Count': 'Cities', 'Temperature_Desc': 'Description'}
        )
        fig5.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig5, width='stretch')


# FOOTER

st.divider()
st.caption("Data source: timeanddate.com | Created by Gabriel Cuadra")