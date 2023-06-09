import streamlit as st

# Define the multipage class to manage the multiple apps in our program 
class MultiPage: 
    """Framework for combining multiple streamlit applications."""

    def __init__(self) -> None:
        """Constructor class to generate a list which will store all our applications as an instance variable."""
        self.page = []
    
    def add_page(self, title, func) -> None: 
        """Class Method to Add pages to the project
        Args:
            title ([str]): The title of page which we are adding to the list of apps 
            
            func: Python function to render this page in Streamlit
        """

        self.page.append(
            {
                "title": title, 
                "function": func
            }
        )

    def run(self):
        # Drodown to select the page to run  
        page = st.sidebar.selectbox(
            'App Navigation', 
            self.page, 
            format_func=lambda page: page.get('title', "")
        )

        # run the app function 
        page.get('function')()