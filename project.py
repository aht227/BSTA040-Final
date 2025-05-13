>>> import streamlit as st #imports streamlit to build web app
... import pandas as pd #import pandas to work with data
... import numpy as np #import numpy for calculations
... 
... #Function to load the ILI data
... def load_data():
...     df = pd.read_csv("ilidata.csv") #reads ILI dataset into a dataframe
...     df = df.dropna(subset=["ili", "state"])  # removes missing values
...     df = df.sort_values(by="epiweek") #sorts data by specific epi week
...     df["weeks"] = range(len(df))  # Add a weeks column
...     return df
... 
... df = load_data() #calls the function and stores data
... 
... #Add a title to app
... st.title("Influenza-Like Illness (ILI) Over Time by State")
... 
... #Dropdown to select a state 
... states = sorted(df["state"].unique()) #gets a sorted list of unique states
... selected_state = st.selectbox("Choose a state:", states) #creates dropdown
... 
... #Filter data for that state
... df_state = df[df["state"] == selected_state]
... 
... #Line chart of ILI percentage
... st.subheader(f"%ILI over time in {selected_state.upper()}") #adds a subheader
... st.line_chart(df_state.set_index("weeks")["ili"]) #Plots %ILI vs week number
... 
... #Summary statistics
... st.subheader("Descriptive Statistics of %ILI") #adds a subheader
... mean_ili = np.mean(df_state["ili"]) #Calculates mean of %ILI
... median_ili = np.median(df_state["ili"]) #Calculates median of %ILI
... std_ili = np.std(df_state["ili"]) #Calculates standard deviation
... 
... st.write(f"Mean ILI: {mean_ili:.2f}") #Shows mean to two decimal places
... st.write(f"Median ILI: {median_ili:.2f}") #Shows median
