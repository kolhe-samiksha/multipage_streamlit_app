import streamlit as st 
from streamlit_option_menu import option_menu
import numpy as np 
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt 
from minio import Minio
from PIL import Image, ImageOps
from io import BytesIO
import plotly.express as px
import hydralit_components as hc
import utils as ut
import os
import requests
import streamlit.components.v1 as components
import uuid
import os
os.system("pip install pandas pmdarima statsmodels minio")
import statsmodels.api as sm

response = requests.get(url='https://katonic.ai/favicon.ico')
im = Image.open(BytesIO(response.content))

st.set_page_config(
    page_title='Multi-Touch-Attribution-markov-chain', 
    page_icon = im, 
    layout = 'wide', 
    initial_sidebar_state = 'auto'
)

ACCESS_KEY = "DNPD2SAYLBELJ423HCNU"
SECRET_KEY = "zF7F6W93HS8vt+JKen4U17+zhcHiwH47AMuO3ap0"
PUBLIC_BUCKET = "shared-storage"

# client = Minio(
#         endpoint="minio-server.default.svc.cluster.local:9000",
#         access_key=ACCESS_KEY,
#         secret_key=SECRET_KEY,
#         secure=False,
#     )

# usr_journey_path = "/multi_touch_attribution/usr_journey_attribution_data.csv"
# usr_attribution_path = "/multi_touch_attribution/usr_attribution_data.csv"
# transition_prob_matrix = "/multi_touch_attribution/transition_matrix.csv"
# channel_performance_across_methods = "/multi_touch_attribution/channel_performance_across_methods.csv"
# markov_chain_rm_data = "/multi_touch_attribution/markov_chain_attribution_update.csv"

# client.fget_object(
#         PUBLIC_BUCKET,
#         usr_journey_path,
#         "data/usr_journey_attribution_data.csv",
#     )

# client.fget_object(
#         PUBLIC_BUCKET,
#         usr_attribution_path,
#         "data/usr_attribution_data.csv",
#     )

# client.fget_object(
#         PUBLIC_BUCKET,
#         transition_prob_matrix,
#         "data/transition_matrix.csv",
#     )

# client.fget_object(
#         PUBLIC_BUCKET,
#         channel_performance_across_methods,
#         "data/channel_performance_across_methods.csv",
#     )

# client.fget_object(
#         PUBLIC_BUCKET,
#         markov_chain_rm_data,
#         "data/markov_chain_rm_data.csv",
#     )


def app():

    menu_data = [
            {'icon': "🚀", 'label':"Load_data-katonic-connectors"},
            {'icon':"🔃",'label':"data-preparation",'submenu':[{'icon': "fa fa-paperclip", 'label':"User_Journey"},{'icon': "fa fa-paperclip", 'label':"Heuristic_attribution"}]},
            {'icon': "💻", 'label':"markov-chain-model",'submenu':[{'icon': "fa fa-paperclip", 'label':"Markov-chain-attribution"},{'icon': "fa fa-paperclip", 'label':"heuristic v/s data-driven"}]},
            {'icon': "far fa-chart-bar", 'label':"Spend_optimisation",'submenu':[{'icon': "fa fa-paperclip", 'label':"about"},{'icon': "fa fa-paperclip", 'label':"View-campaign-performance"},{'icon': "fa fa-paperclip", 'label':"Budget-allocation"}]},
    ]

    over_theme = {'txc_inactive': '#FFFFFF'}
    menu_id = hc.nav_bar(menu_definition=menu_data,home_name='Home',override_theme=over_theme)

    if menu_id=="Home":

        st.title("Multi-Touch-Attribution")

        st.write("Inside the Home")

        st.write("""
        Behind the growth of every consumer-facing product is the **acquisition and retention of an engaged user base**. 
        When it comes to acquisition, the goal is to attract high quality users as cost effectively as possible. With marketing dollars dispersed across a wide array of campaigns, channels, and creatives, however, measuring effectiveness is a challenge. 
        In other words, it's difficult to know how to assign credit where credit is due. """)

        st.write("""Multi-touch attribution is a method of marketing measurement that accounts for all the touchpoints on the customer journey and designates a certain amount of credit to each channel so that marketers can see the value that each touchpoint has on driving a conversion.""")

        st.write("""
        #### Heuristic based approach
        """)

        st.write("""
        heuristic methods are rule-based and consist of both single-touch and multi-touch approaches:
        1. **Single-touch**: Single-touch methods, such as first-touch and last-touch, assign credit to the first channel, or the last channel, associated with a conversion.

        2. **Multi-touch**: Multi-touch methods, such as linear and time-decay, assign credit to multiple channels associated with a conversion.
        """)

        st.write("""
        #### Data-driven approach
        data-driven methods determine assignment using probabilities and statistics. Examples of data-driven methods include **Markov Chains and SHAP**.  
        """)

        st.write("""
        #### 
        
        """)

    st.write("Outside Hello")

    if menu_id=="Load_data-katonic-connectors":
        st.write("Load_data")
        st.title("Load_data using Katonic Connectors")
        st.write("##### Loaded the data residing inside **AWS S3** bucket to the katonic **file-manager** using katonic connectors")
        st.write("""
            just by providing Source as IAM access key, secrete key, bucket name and object name 

            Destination as a katonic_file manager access and secrete key, bucket_name:private/public
        """)

        st.write("""
            Loaded data from AWS S3 to Katonic-filemanager
        """)

        img1 = Image.open('image/katonic_connectors.png')
        st.image(img1)

    st.write("Outside Load_data")

    if menu_id=="data-preparation":
        st.write("xsdea")

    if menu_id=="User_Journey":
        st.title("Users Journey🚀")

        st.write("""
        A user journey is defined as a series of steps that represent how you want users to interact with your app. It involves the analysis of how users are interacting with the app to identify the weakest points in the path to conversion.
        Mapping the user journey from the time of download and their first session is important for your app’s growth 
        """)

        st.write("##### A buyer's journey spans through many devices and touchpoints before resulting in a conversion. In order to optimize campaigns and create more personalized consumer experiences, marketers need to understand which touchpoints and messages a consumer came in contact with that resulted in a positive action.")

        st.write("---")

        st.write("""

        ##### Points can be drawn up by understanding users journey map: 

        - Where the audience interacts with the product. This can be a company website, ads on third-party resources, social media, etc. 
        - How various audience segments interact with your app. 
        - What stages does the user go through before buying and what goals they have.
        
        """)
        img1 = Image.open('image/user_journey.jpg')
        st.image(img1,width=500)

        st.write("User_data_before")

        usr_journ_data = pd.read_csv("data/usr_journey_attribution_data.csv")
        if st.button("User_journey_data"):
            st.write("User_data_inside")
            st.dataframe(usr_journ_data[:1000])

    if menu_id=="Heuristic_attribution":
        st.title("Heuristic approach for user attribution")

        st.write("""
            ###### Heuristic means a practical method of achieving a goal, that is not necessarily optimal, but is good enough for now. Heuristic methods are used when figuring out the optimal way to do something is too costly,
            ###### The heuristic attribution models are all based on where in the customer journey you are.. 
        """)
        st.write("---")
        st.write("""
        There are two main types of methods (or models) used to divide the revenue across channels.""")

        st.write("""
        1. **First Touch Attribution**: This model assigns 100% of the opportunity value to the first (oldest) interaction with the customer.
        First touch is helpful when you want to know which channels are most likely to bring new leads. 
        """)

        st.write("""
        2. **Last Touch Attribution**: This model assigns 100% of the opportunity value to the most recent interaction with the customer. Basically, the last campaign that the prospect interacted with gets all the credit.
        Use last touch to figure out which campaigns / channels are your best deal closers. 
        """)

        usr_attr_data = pd.read_csv("data/usr_attribution_data.csv")
        if st.button("Heuristic_attribution_analysis"):
            st.write("heuristic_inside")
            st.dataframe(usr_attr_data[1000])

            # cnt_plot = sns.catplot(x='channel',y='attribution_percent',hue='attribution_model',data=usr_attr_data, kind='bar', aspect=2).set_xticklabels(rotation=15)
            # st.pyplot(cnt_plot)

            #df = px.data.tips()
            fig = px.histogram(usr_attr_data, x="channel", y="attribution_percent",
                            color='attribution_model', barmode='group',
                            height=700)

            st.plotly_chart(fig,use_container_width=True)

    if menu_id=="Dashboard-analysis":
        st.write("INNJXFSFV")

    if menu_id=="Markov-chain-attribution":
        st.title("Markov-chain-attribution modelling")

        st.write("""##### Markov chaining is the process/illustration of predicting the future event based on some previous conditions/event.""")
        st.write("---")
        st.write("""
        Three steps to calculate attribution using Markov chains:
        1. **Transition probability matrix**: A transition probability matrix is a matrix that contains the probabilities associated with moving from one state to another state. This is calculated using the data from all available customer journeys.

        2. **Total conversion probability**: on average, the likelihood that a given user will experience a conversion event.

        3. **Removal effect per channel**: difference between the total conversion probability (with all channels) and the conversion probability when the conversion is set to 0%.
        """)

        trans_data = pd.read_csv('data/transition_matrix.csv')
        markov_chain_data = pd.read_csv("data/markov_chain_rm_data.csv")
        if st.button("Transition_Matrix"):
            st.write("##### Transition Probability Matrix")
            st.dataframe(trans_data)
            st.write("---")
            st.write("##### Total Conversion Probability")
            st.success("0.03760307804217135")
            st.write("---")
            st.write("##### Removal Effect per channel probability")
            st.dataframe(markov_chain_data)

    st.write("Heuristic_data_driev")

    if menu_id=="heuristic v/s data-driven":
        st.title("Heuristic v/s Data-driven")
        st.write("""
        **the multi-touch models are more accurate**, since you’re not betting all your money on a single channel. 
        
        It’s only fair to say all the interactions your lead had with your company contributed to some extent to the conversion, 
        
        so to credit only the first one, the last one, or some other one in the middle may seem simplistic and reductionist.
        """)

        new_df = pd.read_csv('data/channel_performance_across_methods.csv')
        new_df = new_df.drop('Unnamed: 0',axis=1)
        if st.button("channel_performance"):
            st.dataframe(new_df) 

            fig = px.histogram(new_df, x="channel", y="attribution_percent",
                                color='attribution_model', barmode='group',
                                height=700)

            st.plotly_chart(fig,use_container_width=True)

    if menu_id=="about":
        st.title("Spend Optimisation")
        st.write("The goal of multi-touch attribution is to understand where to allocate your **marketing spend**. When marketers can understand the role that certain touchpoints played in a conversion, they can more effectively devote funds to similar touchpoints in future media plans and divert funds from ineffective channels.")

    st.write("Before user_journey")
    usr_journey_attribution_data = pd.read_csv('data/usr_journey_attribution_data.csv')
    st.table(usr_journey_attribution_data)

    base_conversion_rate = pd.read_csv('data/conversion_data.csv')

    base_conversion_rate['interaction_type'] = base_conversion_rate['interaction_type'].map({
        0: 'Impression',
        1: 'Conversion'
    })

    if menu_id=="View-campaign-performance":
        st.title("Campaign Performance")

        cc1,cc2 = st.columns([1,1])

        with cc1:
            # img1 = Image.open('image/base_conversion_rate.png')
            # st.image(img1,width=325)

            fig = px.pie(base_conversion_rate, values='count', names='interaction_type')

            fig.update_layout(title='Interaction Types')

            st.plotly_chart(fig)

            st.write("---")

            img2 = Image.open('image/conversions_by_date.png')
            st.image(img2,width=600)

        with cc2:
            img3 = Image.open('image/channel_performance.png')
            st.image(img3,width=700)

            st.write("---")

            img4 = Image.open('image/channel_cost_per_aquisition.png')
            st.image(img4,width=700)

    if menu_id=="Budget-allocation":
        st.title("Budget-allocation-optimisation")

        st.write("###### data-driven approach using Markov chain for efficient budget allocation across all channels.")

        st.write("1. Current Spending: Initial campaign assumption to assign same credit across all channels.")
        st.write("2. Proposed Spending: The markov chain conversion probability values.")
        img5 = Image.open('image/spend_optimisation_per_channel.png')
        st.image(img5,use_column_width=True)
