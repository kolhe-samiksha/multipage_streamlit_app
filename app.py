import os
import streamlit as st
import numpy as np
from PIL import Image 
from multipage import MultiPage
from page import home, marketing_analytics, multitouch_attribution

# Create an instance of the app 
app = MultiPage()

app.add_page("Home",home.app)
app.add_page("marketing analytics",marketing_analytics.app)
app.add_page("multi touch attribution",multitouch_attribution.app)

# The main app
app.run()
