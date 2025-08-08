# covid_dashboard.py

import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# ----------------------------
# 1️⃣ DATA FETCHING
# ----------------------------
@st.cache_data
def get_covid_data():
    url = "https://disease.sh/v3/covid-19/countries"
    response = requests.get(url)
    if response.status_code != 200:
        st.error("Failed to fetch data from API")
        return pd.DataFrame()
    data = response.json()
    return pd.DataFrame(data)

df = get_covid_data()

if df.empty:
    st.stop()

# ----------------------------
# 2️⃣ DATA CLEANING
# ----------------------------
df = df[['country', 'cases', 'todayCases', 'deaths', 'todayDeaths', 'recovered', 'active', 'population']]
df['cases_per_million'] = (df['cases'] / df['population']) * 1_000_000
df['death_rate'] = (df['deaths'] / df['cases']) * 100

# ----------------------------
# 3️⃣ DASHBOARD TITLE
# ----------------------------
st.title("🌍 COVID-19 Data Dashboard")
st.markdown("Live COVID-19 statistics by country, powered by the [disease.sh API](https://disease.sh/).")

# ----------------------------
# 4️⃣ COUNTRY SELECTOR
# ----------------------------
country = st.selectbox("Select a country", df['country'].unique())

# Filter the data for the selected country
country_data = df[df['country'] == country].iloc[0]

# ----------------------------
# 5️⃣ COUNTRY STATISTICS
# ----------------------------
st.subheader(f"📊 COVID-19 Stats for {country}")
st.metric("Total Cases", f"{country_data['cases']:,}")
st.metric("Deaths", f"{country_data['deaths']:,}")
st.metric("Recovered", f"{country_data['recovered']:,}")
st.metric("Active Cases", f"{country_data['active']:,}")
st.metric("Death Rate (%)", f"{country_data['death_rate']:.2f}")
st.metric("Cases per Million", f"{country_data['cases_per_million']:.2f}")

# ----------------------------
# 6️⃣ TOP COUNTRIES CHART
# ----------------------------
st.subheader("Top 10 Countries by Total Cases")
top_countries = df.sort_values(by='cases', ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10,5))
ax.bar(top_countries['country'], top_countries['cases'], color='skyblue')
ax.set_xticklabels(top_countries['country'], rotation=45)
ax.set_title("Top 10 Countries by COVID-19 Cases")
ax.set_xlabel("Country")
ax.set_ylabel("Total Cases")
st.pyplot(fig)

# ----------------------------
# 7️⃣ DATA TABLE
# ----------------------------
st.subheader("Full Data Table")
st.dataframe(df)

# ----------------------------
# 8️⃣ DOWNLOAD OPTION
# ----------------------------
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download Data as CSV", csv, "covid_data.csv", "text/csv")