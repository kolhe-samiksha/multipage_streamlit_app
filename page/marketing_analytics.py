import streamlit as st
from streamlit_option_menu import option_menu
import os
import requests
from PIL import Image, ImageOps
from io import BytesIO
import utils as ut
import numpy as np
import time
import pandas as pd
import plotly.express as px
import pickle
import hydralit_components as hc
import plotly.figure_factory as ff
import plotly.graph_objects as go
import matplotlib.pyplot as plt
os.system("python -V")
os.system("pip install pandas minio psycopg2-binary==2.9.3 sqlalchemy==1.4.26")
import json
import pandas as pd
from minio import Minio
from numerize.numerize import numerize
import datetime

ACCESS_KEY = "VI6FS391PPVVLLQOCZM9"
SECRET_KEY = "RQF8OQgomPlTzv+ixaFMN2vKKf4XMLjinHQ8mb9S"
PUBLIC_BUCKET = "shared-storage"

client = Minio(
        endpoint="minio-server.default.svc.cluster.local:9000",
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
        secure=False,
        )

objects = client.list_objects(PUBLIC_BUCKET, prefix="google_analytics_cleaned_data/")

lst = []

def app():
    for obj in objects:
        print(obj.object_name)
        lst.append(obj.object_name)


    for i in lst:
        client_data = i
        client.fget_object(
            PUBLIC_BUCKET,
            client_data,
            f"data/{i}"
            )
            
    with st.sidebar:
        selected = option_menu(
            menu_title = "Main Menu",
            options = ["About","Google Analytics","Facebook Marketing","Analytics Report","Marketing Report"]
        )

    # Google Analytics
    def get_data():
        df = pd.read_csv('data/google_analytics_cleaned_data/devices.csv')
        return df

    ga_df = get_data()
    daily_active_users = pd.read_csv('data/google_analytics_cleaned_data/daily_active_users.csv')
    pages = pd.read_csv('data/google_analytics_cleaned_data/pages.csv')
    traffic_source = pd.read_csv('data/google_analytics_cleaned_data/traffic_sources.csv')
    website_overview = pd.read_csv('data/google_analytics_cleaned_data/website_overview.csv')
    locations = pd.read_csv('data/google_analytics_cleaned_data/locations.csv')
    devices = pd.read_csv('data/google_analytics_cleaned_data/devices.csv')

    if selected == "About":
        st.write("""
            # Analytics & Marketing Report 
            """)
        st.write("##### Google Analytics and Facebook marketing reports can help clients understand the effectiveness of their online marketing efforts and make informed decisions about how to optimize their digital marketing strategies.")
        img1 = Image.open('image/bigstock-189358798.jpeg')
        st.image(img1,use_column_width=True)
        st.write("""###### Google Analytics is a web analytics tool that allows clients to track website traffic, user behavior, and conversion rates. By analyzing the data provided by Google Analytics, clients can understand how users are interacting with their website, which pages are the most popular, how long users are staying on the site, and how often they are converting into customers or leads.""")
        
        st.write("""###### This information can help clients make data-driven decisions about their website content, design, and user experience to improve conversions and engagement.""")
                    
        st.write("###### Facebook marketing reports provide data on the performance of paid social media campaigns, including ad spend, impressions, reach, click-through rates, and conversion rates. Clients can use this information to optimize their ad targeting, ad creative, and budget to improve campaign performance and ROI. Facebook marketing reports can also provide insights into the demographics and interests of users who engage with the client's ads, which can help with audience targeting and content creation.")

        st.write("###### Clients can use this information to optimize their ad targeting, ad creative, and budget to improve campaign performance and ROI.")

        #st.write("###### **Inventory management**: Predictive models can be used to forecast demand for different products, allowing businesses to optimize their inventory levels and minimize stockouts or overstocking.")

        #st.write("###### depending upon the reasons the Types of Attributions are as follows:")
        #st.write("""1. **Voluntary attrition**: when employee leaves the organisation due to personal reasons.""")
        #st.write("""2. **Involuntary attrition**: when the organization ends the employment process due to some internal/market conditions""")
        #st.write("""3. **External attrition**: when an employee leaves an organization to work for another organization.""")
        #st.write("""4. **Internal attrition**: when an employee is given another position within the same organization as a promotion.""")
        
        st.success("Visit Reports to conclude the key factors.")

    if selected == "Google Analytics":
        
        # Define the data for each option
        options_data = {
            "Devices": ga_df,
            "Daily Active Users": daily_active_users,
            "Pages": pages,
            "Traffic Source": traffic_source,
            "Website Overview": website_overview,
            "Locations": locations,
        }

        # Create the expander with the options
        with st.expander("Please Select One to View Data"):
            option = st.selectbox("", list(options_data.keys()))

        # Handle the "Submit" button click
        if st.button("Submit"):
            # Display the data for the selected option
            st.write(options_data[option])

    # Load the logo image
    logo_image = Image.open("image/GAnalytics.svg.png")

    # Create the container
    header_container = st.container()


    if selected == "Analytics Report":
        #st.title('Analytics')
        # Add the logo and title to the container
        #with st.sidebar:
            #user_date = st.date_input("Select your Date",
                                #value = datetime.date(2023, 6, 12),
                                #min_value = datetime.date(2023, 1, 12),
                                #max_value = datetime.date(2024, 1, 12)
                                #)

            #st.write(user_date)



        #df1 = website_overview.query('ga_date == @user_date')

        

        total_impressions = float(website_overview['ga_sessions'].count())
        avg_bounce_rate = float(website_overview['ga_bounceRate'].mean())
        avg_sessions_duration = float(website_overview['ga_avgSessionDuration'].mean())
        

        total1,total2,total3 = st.columns(3)

        with header_container:
            st.image(logo_image, width=50)
            st.title("Analytics")

        with total1:    
            st.image('image/impression.png',use_column_width='Auto')
            st.metric(label = 'Total Sessions', value= numerize(total_impressions))

        with total2:
            st.image('image/tap.png',use_column_width='Auto')
            st.metric(label='Avg Bounce Rate', value=numerize(avg_bounce_rate))

        with total3:
            st.image('image/app_conversion.png',use_column_width='Auto')
            st.metric(label='Avg Session Duration (ms)', value=numerize(avg_sessions_duration))
            

        #st.bar_chart(daily_active_users, x='ga_1dayUsers')
        # Pyplot charts are customizable
        
        Q1,Q2 = st.columns(2)

        with Q1:
            df_traffic = traffic_source.groupby(by = ['ga_medium']).size()
            df_traffic = df_traffic.reset_index()
            fig_traffic_by_medium = px.bar(df_traffic,
                                    x='ga_medium',
                                    y=0,
                                    title='Traffic by Medium')
            fig_traffic_by_medium.update_layout(title = {'x' : 0.5},
                                            plot_bgcolor = "rgba(0,0,0,0)",
                                            xaxis =(dict(showgrid = False)),
                                            yaxis =(dict(showgrid = False)))
            st.plotly_chart(fig_traffic_by_medium,use_container_width=True)


        with Q2:
            df_visitor = website_overview[['ga_date', 'ga_newUsers']]
            df_visitor['ga_date'] = pd.to_datetime(df_visitor['ga_date'])


            fig_visitors_by_date = px.line(website_overview,x='ga_date',
                                            y='ga_newUsers',
                                            title='<b>Daily Visitors</b>')
            fig_visitors_by_date.update_xaxes(rangeslider_visible=True)
            fig_visitors_by_date.update_layout(xaxis_range=['2022-12-30','2023-04-24'],
                                                showlegend = False,
                                                title = {'x' : 0.5},
                                                plot_bgcolor = "rgba(1,0,0,0)",
                                                xaxis =(dict(showgrid = False)),
                                                yaxis =(dict(showgrid = False)),)
            st.plotly_chart(fig_visitors_by_date,use_container_width=True)


        Q3,Q4 = st.columns(2)

        with Q3:
            df4 = traffic_source.groupby(by=['ga_medium']).size().reset_index(name='ga_sessions')
            fig_spend_by_gender = px.pie(df4,names='ga_medium',values='ga_sessions',title='<b>Ad Spend By Gender</b>')
            fig_spend_by_gender.update_layout(title = {'x':0.5}, plot_bgcolor = "rgba(0,0,0,0)")
            st.plotly_chart(fig_spend_by_gender,use_container_width=True)

        with Q4:
            df5 = devices.groupby(by=['ga_deviceCategory']).size().reset_index(name='ga_sessions')
            fig_spend_by_gender = px.pie(df5,names='ga_deviceCategory',values='ga_sessions',title='<b>Traffic by Devices</b>')
            fig_spend_by_gender.update_layout(title = {'x':0.5}, plot_bgcolor = "rgba(0,0,0,0)")
            st.plotly_chart(fig_spend_by_gender,use_container_width=True)

        Q5,Q6 = st.columns(2)

        with Q5:
            df6 = devices.groupby(by=['ga_operatingSystem']).size().reset_index(name='ga_sessions')
            fig_spend_by_gender = px.pie(df6,names='ga_operatingSystem',values='ga_sessions',title='<b>Traffic by OS</b>')
            fig_spend_by_gender.update_layout(title = {'x':0.5}, plot_bgcolor = "rgba(0,0,0,0)")
            st.plotly_chart(fig_spend_by_gender,use_container_width=True)

    # Facebook Marketing
    def get_data():
        df = pd.read_csv('fb_data.csv')
        df['date']= pd.to_datetime(df['date'])
        return df

    df = get_data()

    if selected == "Facebook Marketing":
        st.write("Facebook Data:")
        st.table(df)

    if selected == "Marketing Report":
        #st.write("Facebook Ad Campaign Dashboard:")
        #st.table(df)
        st.title('Campaign Dashboard')

        with st.sidebar:
            Campaign_filter = st.multiselect(label= 'Select The Campaign',
                                        options=df['campaign'].unique(),
                                        default=df['campaign'].unique())

            Age_filter = st.multiselect(label='Select Age Group',
                                    options=df['age'].unique(),
                                    default=df['age'].unique())

            Gender_filter = st.multiselect(label='Select Gender Group',
                                    options=df['gender'].unique(),
                                    default=df['gender'].unique())

        df1 = df.query('campaign == @Campaign_filter & age == @Age_filter & gender == @Gender_filter')

        total_impressions = float(df1['Impressions'].sum())
        total_clicks = float(df1['Clicks'].sum())
        total_spent = float(df1['Spent'].sum())
        total_conversions= float(df1['Total_Conversion'].sum()) 
        total_approved_conversions = float(df1['Approved_Conversion'].sum())

        total1,total2,total3,total4,total5 = st.columns(5)

        with total1:
            st.image('image/impression.png',use_column_width='Auto')
            st.metric(label = 'Total Impressions', value= numerize(total_impressions))
        
        with total2:
            st.image('image/tap.png',use_column_width='Auto')
            st.metric(label='Total Clicks', value=numerize(total_clicks))

        with total3:
            st.image('image/hand.png',use_column_width='Auto')
            st.metric(label= 'Total Spend',value=numerize(total_spent,2))

        with total4:
            st.image('image/conversion.png',use_column_width='Auto')
            st.metric(label='Total Conversions',value=numerize(total_conversions))

        with total5:
            st.image('image/app_conversion.png',use_column_width='Auto')
            st.metric(label='Approved Conversions',value=numerize(total_approved_conversions))

        Q1,Q2 = st.columns(2)

        with Q1:
            df3 = df1.groupby(by = ['campaign']).sum()[['Impressions','Clicks']].reset_index()
            df3['CTR'] =round(df3['Clicks']/df3['Impressions'] *100,3)
            fig_CTR_by_campaign = px.bar(df3,
                                    x='campaign',
                                    y='CTR',
                                    title='<b>Click Through Rate</b>')
            fig_CTR_by_campaign.update_layout(title = {'x' : 0.5},
                                            plot_bgcolor = "rgba(0,0,0,0)",
                                            xaxis =(dict(showgrid = False)),
                                            yaxis =(dict(showgrid = False)))
            st.plotly_chart(fig_CTR_by_campaign,use_container_width=True)

        with Q2:
            fig_impressions_per_day = px.line(df1,x='date',
                                            y=['Impressions'],
                                            color='campaign',
                                            title='<b>Daily Impressions By Campaign</b>')
            fig_impressions_per_day.update_xaxes(rangeslider_visible=True)
            fig_impressions_per_day.update_layout(xaxis_range=['2021-01-01','2021-01-31'],
                                                showlegend = False,
                                                title = {'x' : 0.5},
                                                plot_bgcolor = "rgba(0,0,0,0)",
                                                xaxis =(dict(showgrid = False)),
                                                yaxis =(dict(showgrid = False)),)
            st.plotly_chart(fig_impressions_per_day,use_container_width=True)

        Q3,Q4 = st.columns(2)

        with Q3:
            df4 = df1.groupby(by='gender').sum()[['Spent']].reset_index()
            fig_spend_by_gender = px.pie(df4,names='gender',values='Spent',title='<b>Ad Spend By Gender</b>')
            fig_spend_by_gender.update_layout(title = {'x':0.5}, plot_bgcolor = "rgba(0,0,0,0)")
            st.plotly_chart(fig_spend_by_gender,use_container_width=True)

        with Q4:
            df5 = df1.groupby(by='age').sum()[['Spent','Total_Conversion']].reset_index()
            df5['CPC'] = round(df5['Spent']/df5['Total_Conversion'],2)
            fig_CPC_by_age = px.bar(df5,x = 'age',y='CPC',title='<b>Cost Per Conversion By Age Demographic</b>')
            fig_CPC_by_age.update_layout(title = {'x':0.5},xaxis =(dict(showgrid = False)),yaxis =(dict(showgrid = False)), plot_bgcolor = "rgba(0,0,0,0)")
            st.plotly_chart(fig_CPC_by_age,use_container_width=True)
