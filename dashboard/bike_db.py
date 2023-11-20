# import library
from multiprocessing import Value
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import streamlit as st

# membuat helper function

# create_rental_df() digunakan untuk menyiapkan rental_df
def create_rental_df(df):
    rental_df = df.resample(rule='D', on='datetime').agg({
        'total': 'sum'
    })
    rental_df = rental_df.reset_index()
    rental_df.rename(columns={
        'total': 'total_rental'
    }, inplace=True)

    return rental_df

# create_sum_rental_df() untuk menyiapkan sum_rental_df
def create_sum_rental_df(df):
    sum_rental_df = df.groupby('datetime').total.sum().sort_values(ascending=False).reset_index()
    return sum_rental_df

# create_byyear_df() untuk menyiapkan byyear_df
def create_byyear_df(df):
    byyear_df = df.groupby(by=df['datetime'].dt.year).total.sum().sort_values(ascending=False).reset_index()
    byyear_df.rename(columns={
        'datetime': 'year'
    }, inplace=True)
    return byyear_df

# create_bymonth_df() untuk menyiapkan bymonth_df
def create_bymonth_df(df):
    bymonth_df = df.groupby(by=df['datetime'].dt.month).total.sum().reset_index()
    bymonth_df.rename(columns={
        'datetime': 'month'
    }, inplace=True)
    return bymonth_df

# create_weathercond_df() untuk menyiapkan weathercond_df
def create_weathercond_df(df):
    weathercond_df = df.groupby('weather_cond').total.sum().sort_values(ascending=False).reset_index()
    return weathercond_df

# create_weathercond_year_df() untuk menyiapkan weathercond_year_df
def create_weathercond_year_df(df):
    weathercond_year_df = df.groupby(by=[df["datetime"].dt.year,df["weather_cond"]]).total.sum().reset_index()
    weathercond_year_df['datetime'] = weathercond_year_df.datetime.astype('str')
    weathercond_year_df['weather_cond'] = weathercond_year_df.weather_cond.astype('category')
    return weathercond_year_df

# create_weathercond_month_df() untuk menyiapkan weathercond_month_df
def create_weathercond_month_df(df):
    weathercond_month_df = df.groupby(by=[df["datetime"].dt.month,df["weather_cond"]]).total.sum().reset_index()
    weathercond_month_df['datetime'] = weathercond_month_df.datetime.astype('str')
    weathercond_month_df['weather_cond'] = weathercond_month_df.weather_cond.astype('category')
    return weathercond_month_df

# create_weathercond_days_df() untuk menyiapkan weathercond_days_df
def create_weather_days_df(df):
    weather_days_df = df.groupby(by=[df["weekday"], df["weather_cond"]]).total.sum().reset_index()
    weather_days_df['weekday'] = weather_days_df.weekday.astype('category')
    weather_days_df['weather_cond'] = weather_days_df.weather_cond.astype('str')
    return weather_days_df

# create_season_df() untuk menyiapkan season_df
def create_season_df(df):
    season_df = df.groupby('season').total.sum().sort_values(ascending=False).reset_index()
    return season_df

# create_season_year_df() untuk menyiapkan season_year_df
def create_season_year_df(df):
    season_year_df = df.groupby(by=[df["datetime"].dt.year,df["season"]]).total.sum().reset_index()
    season_year_df['datetime'] = season_year_df.datetime.astype('str')
    season_year_df['season'] = season_year_df.season.astype('category')
    return season_year_df

# create_season_days_df() untuk menyiapkan season_days_df
def create_season_days_df(df):
    season_days_df = df.groupby(by=[df["weekday"],df["season"]]).total.sum().reset_index()
    season_days_df['weekday'] = season_days_df.weekday.astype('category')
    season_days_df['season'] = season_days_df.season.astype('str')
    return season_days_df

# create_weather_hour_df() untuk menyiapkan weather_hour_df
def create_weather_hour_df(df):
    weather_hour_df = df.groupby(by=[df["hour"], df['weather_cond']]).total.sum().reset_index()
    weather_hour_df['hour'] = weather_hour_df.hour.astype('category')
    weather_hour_df['weather_cond'] = weather_hour_df.weather_cond.astype('category')
    return weather_hour_df

# create_season_hour_df() untuk menyiapkan season_hour_df
def create_season_hour_df(df):
    season_hour_df = df.groupby(by=[df["hour"], df['season']]).total.sum().reset_index()
    season_hour_df['hour'] = season_hour_df.hour.astype('category')
    season_hour_df['season'] = season_hour_df.season.astype('category')
    return season_hour_df

# create_days_hour_df() untuk menyiapkan days_hour_df
def create_days_hour_df(df):
    days_hour_df = df.groupby(by=[df["hour"], df['weekday']]).total.sum().reset_index()
    days_hour_df['hour'] = days_hour_df.hour.astype('category')
    days_hour_df['weekday'] = days_hour_df.weekday.astype('category')
    return days_hour_df

# create_hour_df() untuk menyiapkan hour_df
def create_hour_df(df):
    hour_df = df.groupby(by='hour').total.sum().reset_index()
    hour_df['hour'] = hour_df.hour.astype('category')
    return hour_df

# create_workingday_df() untuk menyiapkan workingday_df
def create_workingday_df(df):
    workingday_df = df.groupby('workingday').total.sum().reset_index()
    workingday_df['workingday'] = workingday_df.workingday.astype('category')
    return workingday_df

# import dataset
bike_df = pd.read_csv('hour_data.csv')

# format tipe data ke format datetime dan reset index
bike_df.reset_index(inplace=True)
bike_df['datetime'] = pd.to_datetime(bike_df['datetime'])

# membuat komponen filter
min_date = bike_df['datetime'].min()
max_date = bike_df['datetime'].max()

# membuat date input dan memasukanya ke dataframe baru
with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date,max_date]
    )

main_df = bike_df[(bike_df['datetime'] >= str(start_date)) &
                    (bike_df['datetime'] <= str(end_date))]

# Memanggil helper function
rental_df = create_rental_df(main_df)
byyear_df = create_byyear_df(main_df)
bymonth_df = create_bymonth_df(main_df)
days_hour_df = create_days_hour_df(main_df)
hour_df = create_hour_df(main_df)
season_df = create_season_df(main_df)
season_hour_df = create_season_hour_df(main_df)
sum_rental_df = create_sum_rental_df(main_df)
weather_hour_df = create_weather_hour_df(main_df)
weathercond_df = create_weathercond_df(main_df)
workingday_df = create_workingday_df(main_df)
weathercond_year_df = create_weathercond_year_df(main_df)
season_year_df = create_season_year_df(main_df)
weathercond_month_df = create_weathercond_month_df(main_df)
weather_days_df = create_weather_days_df(main_df)
season_days_df = create_season_days_df(main_df)

# membuat visualisasi data

# membuat header dashboard
st.header('Bike Sharing Performance Dashboard')

# membuat subheader daily rental
st.subheader('Daily Bike Rental')

# menampilkan informasi daily rental
total_rental = rental_df.total_rental.sum()
st.metric('Total Rental', value=total_rental)

sns.set_style('whitegrid')
sns.set_context('talk')
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    rental_df["datetime"],
    rental_df["total_rental"],
    marker='o', 
    linewidth=0.5,
    color="blue",
    markersize=2.5
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

# membuat subheader total rental by year
st.subheader('Rental by Year')

sns.set_style('whitegrid')
sns.set_context('talk')
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(data=byyear_df,
            x='year',
            y='total',
            ax=ax,
            palette=['yellow', 'red']
            )

ax.set_xlabel('Tahun', size=20)
ax.bar_label(ax.containers[0], fontsize=20)
ax.tick_params(axis='x', labelsize=23)
ax.tick_params(axis='y', labelsize=16)

st.pyplot(fig)

# membuat subheader total rental by month
st.subheader('Rental by Month')

sns.set_style('whitegrid')
sns.set_context('talk')
fig, ax = plt.subplots(figsize=(20, 10))

sns.barplot(data=bymonth_df,
            x='month',
            y='total',
            ax=ax
            )

ax.set_xlabel('Bulan', size=20)
ax.bar_label(ax.containers[0], fontsize=20)
ax.tick_params(axis='x', labelsize=23)
ax.tick_params(axis='y', labelsize=16)

st.pyplot(fig)

# membuat subheader total rental by cuaca dan musim
st.subheader('Rental by Weather Condition & Season')

col1, col2 = st.columns(2)

with col1:
    sns.set_style('whitegrid')
    sns.set_context('talk')
    fig, ax = plt.subplots(figsize=(30,25))

    sns.barplot(data=weathercond_df,
            x='weather_cond',
            y='total',
            ax=ax
    )

    ax.set_title('Jumlah Sewa Berdasarkan Cuaca', fontsize=65)
    ax.set_ylabel(None)
    ax.set_xlabel('Kondisi Cuaca', size=45)
    ax.bar_label(ax.containers[0], fontsize=45)
    ax.tick_params(axis='x', labelsize=38)
    ax.tick_params(axis='y', labelsize=33)
    st.pyplot(fig)


with col2:
    sns.set_style('whitegrid')
    sns.set_context('talk')
    fig, ax = plt.subplots(figsize=(30,25))

    sns.barplot(data=season_df,
            x='season',
            y='total',
            ax=ax
    )

    ax.set_title('Jumlah Sewa Berdasarkan Musim', fontsize=65)
    ax.set_ylabel(None)
    ax.set_xlabel('Musim (1.Semi; 2.Panas; 3.Gugur; 4.Dingin)', size=45)
    ax.bar_label(ax.containers[0], fontsize=45)
    ax.tick_params(axis='x', labelsize=38)
    ax.tick_params(axis='y', labelsize=33)
    st.pyplot(fig)

col1, col2 = st.columns(2)

with col1:
    sns.set_style('whitegrid')
    sns.set_context('talk')
    fig, ax = plt.subplots(figsize=(30,25))

    sns.barplot(data=weathercond_year_df,
            x='weather_cond',
            y='total',
            hue='datetime',
            ax=ax
    )

    ax.set_title('Jumlah Sewa Berdasarkan Cuaca dan Tahun', fontsize=65)
    ax.set_ylabel(None)
    ax.set_xlabel('Kondisi Cuaca', size=45)
    ax.bar_label(ax.containers[0], fontsize=45)
    ax.bar_label(ax.containers[1], fontsize=45)
    ax.tick_params(axis='x', labelsize=38)
    ax.tick_params(axis='y', labelsize=33)
    st.pyplot(fig)


with col2:
    sns.set_style('whitegrid')
    sns.set_context('talk')
    fig, ax = plt.subplots(figsize=(30,25))

    sns.barplot(data=season_year_df,
            x='season',
            y='total',
            hue='datetime',
            ax=ax
    )

    ax.set_title('Jumlah Sewa Berdasarkan Musim dan Tahun', fontsize=65)
    ax.set_ylabel(None)
    ax.set_xlabel('Musim (1.Semi; 2.Panas; 3.Gugur; 4.Dingin)', size=45)
    ax.bar_label(ax.containers[0], fontsize=45)
    ax.bar_label(ax.containers[1], fontsize=45)
    ax.tick_params(axis='x', labelsize=38)
    ax.tick_params(axis='y', labelsize=33)
    st.pyplot(fig)

# membuat subheader total rental by Bulan dan Hari
st.subheader('Rental Trend by Month, Days, Weather & Season')

col1, col2 = st.columns(2)

with col1:
    sns.set_style('whitegrid')
    sns.set_context('talk')
    fig, ax = plt.subplots(figsize=(30, 20))

    sns.pointplot(data=weathercond_month_df,
                x='datetime',
                y='total',
                hue='weather_cond',
                ax=ax)

    ax.set_title('Total Sewa Berdasarkan Bulan dan Cuaca', fontsize=65)
    ax.set_ylabel(None)
    ax.set_xlabel('Bulan', size=45)
    ax.tick_params(axis='x', labelsize=38)
    ax.tick_params(axis='y', labelsize=33)
    st.pyplot(fig)

with col2:
    sns.set_style('whitegrid')
    sns.set_context('talk')
    fig, ax = plt.subplots(figsize=(30, 20))

    sns.barplot(data=weather_days_df,
              x='total',
              y='weekday',
              hue='weather_cond',
              ax=ax)

    ax.set_title('Total Sewa Berdasarkan Hari dalam seminggu dan Cuaca', fontsize=65)
    ax.set_ylabel('Hari', size=45)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=38)
    ax.tick_params(axis='y', labelsize=33)
    st.pyplot(fig)

sns.set_style('whitegrid')
sns.set_context('talk')
fig, ax = plt.subplots(figsize=(30, 20))

sns.barplot(data=season_days_df,
            x='total',
            y='weekday',
            hue='season',
            ax=ax)

ax.set_title('Jumlah Sewa Berdasarkan Musim dan Hari dalam Seminggu', fontsize=35)
ax.set_ylabel('Hari', size=25)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=28)
ax.tick_params(axis='y', labelsize=23)
st.pyplot(fig)


# membuat subheader rental by jam, hari, cuaca, dan musim
st.subheader('Rental Trend by Hours, Weekdays, Weather & Season')

col1, col2 = st.columns(2)

with col1:
    sns.set_style('whitegrid')
    sns.set_context('talk')
    fig, ax = plt.subplots(figsize=(30, 20))

    sns.pointplot(data=hour_df,
                x='hour',
                y='total',
                ax=ax)

    ax.set_title('Total Penyewaan Sepeda Berdasarkan Jam', fontsize=65)
    ax.set_ylabel(None)
    ax.set_xlabel('Jam', size=45)
    ax.tick_params(axis='x', labelsize=38)
    ax.tick_params(axis='y', labelsize=33)
    st.pyplot(fig)

with col2:
    sns.set_style('whitegrid')
    sns.set_context('talk')
    fig, ax = plt.subplots(figsize=(30, 20))
    
    sns.pointplot(data=weather_hour_df,
              x='hour',
              y='total',
              hue='weather_cond',
              ax=ax)

    ax.set_title('Total Sewa Berdasarkan Jam dan Cuaca', fontsize=65)
    ax.set_ylabel(None)
    ax.set_xlabel('Jam', size=45)
    ax.tick_params(axis='x', labelsize=38)
    ax.tick_params(axis='y', labelsize=33)
    st.pyplot(fig)

col1, col2 = st.columns(2)

with col1:
    sns.set_style('whitegrid')
    sns.set_context('talk')
    fig, ax = plt.subplots(figsize=(30, 20))

    sns.pointplot(data=days_hour_df,
                x='hour',
                y='total',
                hue='weekday',
                ax=ax)

    ax.set_title('Total Penyewaan Sepeda Berdasarkan Jam dan Hari', fontsize=65)
    ax.set_ylabel(None)
    ax.set_xlabel('Jam', size=45)
    ax.tick_params(axis='x', labelsize=38)
    ax.tick_params(axis='y', labelsize=33)
    st.pyplot(fig)

with col2:
    sns.set_style('whitegrid')
    sns.set_context('talk')
    fig, ax = plt.subplots(figsize=(30, 20))
    
    sns.pointplot(data=season_hour_df,
              x='hour',
              y='total',
              hue='season',
              ax=ax)

    ax.set_title('Total Sewa Berdasarkan Jam dan Musim', fontsize=65)
    ax.set_ylabel(None)
    ax.set_xlabel('Jam', size=45)
    ax.tick_params(axis='x', labelsize=38)
    ax.tick_params(axis='y', labelsize=33)
    st.pyplot(fig)

# membuat subheader proporsi total rental berdasar hari libur/kerja
st.subheader('Percentage Total Rental by Workingday')

fig, ax = plt.subplots(figsize=(20, 20))
plt.pie(
        data=workingday_df,
        x='total',
        labels='workingday',
        colors = ('red', 'purple'),
        wedgeprops={'width': 0.65},
        textprops={'color':"black", 'fontsize': 55},
        autopct='%1.1f%%'
    )
ax.set_title('0 = Hari Libur; 1 = Hari Kerja', size=30)
st.pyplot(fig)

# membuat distribusi temperature, kelembapan udara, dan kecepatan angin
st.subheader('Distribution of Temperature, Humidity, & Windspeed')

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(20, 10)) 

# distribusi temperatur 
sns.histplot(data=np.log(main_df['temp']),
            kde=True,
            ax=ax[0])

ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Temperature", loc="center", fontsize=15)
ax[0].tick_params(axis ='y', labelsize=12)
ax[0].tick_params(axis ='x', labelsize=12)

# distribusi kelembapan udara
sns.histplot(data=np.log(main_df['hum']),
            kde=True,
            ax=ax[1])

ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("Humidity", loc="center", fontsize=15)
ax[1].tick_params(axis ='y', labelsize=12)
ax[1].tick_params(axis ='x', labelsize=12)

# distribusi kec. angin
sns.histplot(data=np.log(main_df['windspeed']),
            kde=True,
            ax=ax[2])

ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("Windspeed", loc="center", fontsize=15)
ax[2].tick_params(axis ='y', labelsize=12)
ax[2].tick_params(axis ='x', labelsize=12)

st.pyplot(fig)

# membuat distribusi total rental
st.subheader('Distribution of Total Rental')

stat, p = stats.jarque_bera(main_df['total'])
p_value = 'Normal' if p >= 0.5 else 'Not Normal'

col1, col2 = st.columns(2)
with col1:
    st.metric('P-Value', value=round(p, 4))
with col2:
    st.metric('Distribution Type', value=p_value)

sns.set_style('whitegrid')
sns.set_context('talk')
fig, ax = plt.subplots(figsize=(30, 20))

sns.histplot(data=main_df,
            x='total',
            kde=True,
            ax=ax)

ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis ='y', labelsize=28)
ax.tick_params(axis ='x', labelsize=28)

st.pyplot(fig)

# tes korelasi variabel total vs temp, hum, windspeed
st.subheader('Correlation Test of Total Rental vs Temperature, Humidity, & Windspeed')

# korelasi test
stat1, p1 = stats.spearmanr(main_df.temp, main_df.total)
stat2, p2 = stats.spearmanr(main_df.hum, main_df.total)
stat3, p3 = stats.spearmanr(main_df.windspeed, main_df.total)
p_value1 = 'Not Exist' if p1 >= 0.5 else 'Exist'
p_value2 = 'Not Exist' if p2 >= 0.5 else 'Exist'
p_value3 = 'Not Exist' if p3 >= 0.5 else 'Exist'

col1, col2, col3 = st.columns(3)

with col1:
    st.metric('p-value total vs temperature', value=round(p1, 4))
    st.metric('Correlation', value=p_value1)
with col2:
    st.metric('p-value total vs humidity', value=round(p2, 4))
    st.metric('Correlation', value=p_value2)
with col3:
    st.metric('p-value total vs windspeed', value=round(p3, 4))
    st.metric('Correlation', value=p_value3)

fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(20, 15)) 

# melihat hubungan variabel dependen (total) & variabel independen (temp)
sns.regplot(data=main_df,
            x='temp',
            y='total',
            line_kws=dict(color="r"),
            ax=ax[0])

ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Temperature vs Total", loc="center", fontsize=25)
ax[0].tick_params(axis ='y', labelsize=18)
ax[0].tick_params(axis ='x', labelsize=18)

# melihat hubungan variabel dependen (total) & variabel independen (hum)
sns.regplot(data=main_df,
            x='hum',
            y='total',
            line_kws=dict(color="r"),
            ax=ax[1])

ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("Humidity vs Total", loc="center", fontsize=25)
ax[1].tick_params(axis ='y', labelsize=18)
ax[1].tick_params(axis ='x', labelsize=18)

# melihat hubungan variabel dependen (total) & variabel independen (windspeed)
sns.regplot(data=main_df,
            x='windspeed',
            y='total',
            line_kws=dict(color="r"),
            ax=ax[2])

ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("Windspeed vs Total", loc="center", fontsize=25)
ax[2].tick_params(axis ='y', labelsize=18)
ax[2].tick_params(axis ='x', labelsize=18)

st.pyplot(fig)

# correlation value
st.subheader('Spearman Correlation Value of Total Rental vs Temperature, Humidity, & Windspeed')

fig, ax = plt.subplots(figsize=(30,30))

corr = main_df[['temp',
        'hum', 
        'windspeed', 
        'total']].corr(method='spearman')

sns.heatmap(data=corr,
                annot=True,
                annot_kws={'size': 40})
ax.tick_params(axis='x', labelsize=40)
ax.tick_params(axis='y', labelsize=40)
st.pyplot(fig)

st.caption('Copyright (c) Naufal Ulwan Arrifqy 2023')