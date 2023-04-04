import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def daily_rent(df):
    data_daily = df.resample(rule='D', on='date').agg({
        'no_index' : 'unique',
        'total' : 'sum'
    })

    data_daily = data_daily.reset_index()
    data_daily.rename(columns={
        'no_index': 'jumlah_sewa',
        'total' : 'total_sewa'}, inplace=True)

    return data_daily

def customer_comparison(df):
    cust_comparison = df.resample(rule='D', on='date').agg({
        'no_index' : 'unique',
        'casual' : 'sum',
        'registered': 'sum'
    })
    
    cust_comparison = cust_comparison.reset_index()
    cust_comparison.rename(columns={
        'no_index' : 'no_rent',
        'casual' : 'total_casual',
        'registered': 'total_registered'},inplace=True)
    
    return cust_comparison

def weekday_rent(df):
    by_weekday = df.groupby(by='weekday').agg({
    'total': 'sum'
    })
    by_weekday = by_weekday.reset_index()
    by_weekday.rename(columns={
        'total' : 'total_rent'
    },inplace=True)

    return by_weekday

def monthly_rent(df):
    by_monthly = df.groupby(by='month').agg({
    'total': 'sum'
    })
    
    by_monthly = by_monthly.reset_index()
    by_monthly.rename(columns={
        'total' : 'total_rent'
    },inplace=True)

    return by_monthly

def season_rent(df):
    by_season = df.groupby("season").total.sum().sort_values(ascending=False).reset_index()

    map_dict = {1:'Musim Semi', 2:'Musim Panas', 3:'Musim Gugur', 4:'Musim Dingin'}
    by_season['musim'] = by_season['season'].map(map_dict)

    return by_season

def workday_rent(df):
    by_workday = df.groupby("workingday").total.sum().sort_values(ascending=False).reset_index()

    map_dict = {0:'Hari Libur', 1:'Hari Kerja'}
    by_workday['hari_kerja'] = by_workday['workingday'].map(map_dict)

    return by_workday

def hourly_rent(df):
    by_hour = df.groupby(by='hour').agg({
    'total': 'sum'
    })
    
    by_hour = by_hour.reset_index()
    by_hour.rename(columns={
        'total' : 'total_rent'
    },inplace=True)

    return by_hour

def data_weather(df):
    by_weather = df.resample(rule='D', on='date').agg({
        'no_index' : 'unique',
        'temp' : 'sum',
        'atemp' : 'sum',
        'humidity' : 'sum',
        'windspeed' : 'sum',
        'total' : 'sum'
    })

    by_weather = by_weather.reset_index()
    by_weather.rename(columns={
        'no_index': 'jumlah',
        'temp' : 'temp',
        'atemp' : 'atemp',
        'humidity' : 'humidity',
        'windspeed' : 'windspeed',
        'total' : 'total_sewa'}, inplace=True)

    return by_weather

bike_day = pd.read_csv("clean_bike_day.csv")
bike_hour = pd.read_csv("clean_bike_hour.csv")

datetime_columns = ["date"]
bike_day.sort_values(by="date", inplace=True)
bike_day.reset_index(inplace=True)

bike_hour.sort_values(by="date", inplace=True)
bike_hour.reset_index(inplace=True)
 
for column in datetime_columns:
    bike_day[column] = pd.to_datetime(bike_day[column])
    bike_hour[column] = pd.to_datetime(bike_hour[column])

min_date = bike_day["date"].min() or bike_hour["date"].min()
max_date = bike_day["date"].max() or bike_hour["date"].max()
 
with st.sidebar:
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = bike_day[(bike_day["date"] >= str(start_date)) & 
                (bike_day["date"] <= str(end_date))]

hour_df = bike_hour[(bike_hour["date"] >= str(start_date)) & 
                (bike_hour["date"] <= str(end_date))]


data_daily_rent = daily_rent(main_df)
data_customer_comparison = customer_comparison(main_df)
data_by_week = weekday_rent(main_df)
data_by_month = monthly_rent(main_df)
data_by_season = season_rent(main_df)
data_by_workday = workday_rent(main_df)
data_hourly_rent = hourly_rent(hour_df)
data_cuaca = data_weather(main_df)

st.header('Dashboard Analisis Rental Sepeda')
st.text("Oleh : Mellania Permata Sylvie")

#Visualisasi data sewa harian
st.subheader('Data Rental Harian')

col1, col2 = st.columns(2)

with col1:
    total_orders = data_daily_rent.jumlah_sewa.count()
    st.metric("Jumlah Rentang Hari", value=total_orders)
 
with col2:
    total_rent = data_daily_rent.total_sewa.sum()
    st.metric("Jumlah Sewa Sepeda", value=total_rent)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    data_daily_rent["date"],
    data_daily_rent["total_sewa"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

#Visualisasi data customer
st.subheader("Data Rental berdasarkan Customer")
col1, col2 = st.columns(2)

with col1:
    total_casual = data_customer_comparison.total_casual.sum()
    st.metric("Total Penyewa biasa (casual)", value=total_casual)
 
with col2:
    total_registered = data_customer_comparison.total_registered.sum()
    st.metric("Total Penyewa Terdaftar (registered)", value=total_registered)

#Visualisasi perbandingan data rental
st.subheader("Perbandingan Jumlah Rental")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    colors = ["#6495ED"]
    sns.barplot(
        y="total_rent", 
        x="weekday",
        data=data_by_week.sort_values(by="total_rent"),
        palette=colors,
        ax=ax
    )
    ax.set_title("Jumlah Sewa Berdasarkan Hari", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    colors = ["#FF7F50"]
    sns.barplot(
        y="total_rent", 
        x="month",
        data=data_by_month.sort_values(by="total_rent"),
        palette=colors,
        ax=ax
    )
    ax.set_title("Jumlah Sewa Berdasarkan Bulan", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.barplot(
        y="total", 
        x="musim",
        data=data_by_season.sort_values(by="total"),
        ax=ax
    )
    ax.set_title("Jumlah Sewa Berdasarkan Musim", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.barplot(
        y="total", 
        x="hari_kerja",
        data=data_by_workday.sort_values(by="total"),
        ax=ax
    )
    ax.set_title("Jumlah Sewa Berdasarkan Hari Kerja atau Tidak", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

st.subheader("Jam Terbaik untuk Menyewa Sepeda")
col1, col2 = st.columns(2)

with col1:
    best_hour = data_hourly_rent.loc[data_hourly_rent.total_rent.idxmax(), 'hour']
    st.metric("Jam dengan jumlah sewa terbanyak", value=best_hour)
 
with col2:
    worst_hour = data_hourly_rent.loc[data_hourly_rent.total_rent.idxmin(), 'hour']
    st.metric("Jam dengan jumlah sewa paling sedikit", value=worst_hour)

fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9"]
sns.barplot(
    y="total_rent",
    x="hour", 
    data=data_hourly_rent,
    palette=colors,
    ax=ax
)
ax.set_title("Number of Customer by States", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

st.subheader("Rata-Rata Perhitungan Cuaca")

col1, col2 = st.columns(2)

with col1:
    total_temp= data_cuaca.temp.mean().round(3)
    st.metric("Jumlah Rata-Rata temperatur (temp)", value=total_temp)
 
with col2:
    total_atemp= data_cuaca.atemp.mean().round(3)
    st.metric("Jumlah Rata-Rata temperatur (atemp)", value=total_atemp)

col1, col2 = st.columns(2)

with col1:
    total_humidity= data_cuaca.humidity.mean().round(3)
    st.metric("Jumlah Rata-Rata Kelembaban (humidity)", value=total_humidity)
 
with col2:
    total_wind= data_cuaca.windspeed.mean().round(3)
    st.metric("Jumlah Rata-Rata Kecepatan Angin (windspeed)", value=total_wind)