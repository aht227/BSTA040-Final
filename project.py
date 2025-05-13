import streamlit as st #imports streamlit to build web app
import pandas as pd #import pandas to work with data
import numpy as np #import numpy for calculations
import matplotlib.pyplot as plt
#Function to load the ILI data
def load_data():
    df = pd.read_csv("ilidata.csv") #reads ILI dataset into a dataframe
    df = df.dropna(subset=["ili", "state"])  # removes missing values
    df = df.sort_values(by="epiweek") #sorts data by specific epi week
    df["weeks"] = range(len(df))  # Add a weeks column
    return df
df = load_data() #calls the function and stores data
#Add a title to app
st.title("Influenza-Like Illness (ILI) Over Time by State")
#Dropdown to select a state
states = sorted(df["state"].unique()) #gets a sorted list of unique states
selected_state = st.selectbox("Choose a state:", states) #creates dropdown

#Filter data for that state
df_state = df[df["state"] == selected_state]

#Line chart of ILI percentage
st.subheader(f"%ILI over time in {selected_state.upper()}") #adds a subheader
st.line_chart(df_state.set_index("weeks")["ili"]) #Plots %ILI vs week number

#Summary statistics
st.subheader("Descriptive Statistics of %ILI") #adds a subheader
mean_ili = np.mean(df_state["ili"]) #Calculates mean of %ILI
median_ili = np.median(df_state["ili"]) #Calculates median of %ILI
std_ili = np.std(df_state["ili"]) #Calculates standard deviation
st.write(f"Mean ILI: {mean_ili:.2f}") #Shows mean to two decimal places
st.write(f"Median ILI: {median_ili:.2f}") #Shows median

#Header for Time Series Plot Description
st.subheader("Description: %ILI Over Time")

#Adds a textbox for time series explanation
st.markdown("""
This time series plot shows the weekly percentage of patients with influenza like illness (%ILI) in the selected
state. Peaks in the plot represent flu seasons that occur throughout the year. The x-axis represents weeks since
the beginning of the data and the y-axis shows ILI percentages. The recurring on and off pattern suggests that
the flu follows a seasonal trend and can be modeled over time.
""")

#Create a figure and axis for histgoram of ILI percent
fig, ax = plt.subplots() 
ili_vals = df_state["ili"].dropna() #get ILI values for selected state and remove missing data

#Plot histogram of %ILI with the probability density 
ax.hist(ili_vals, bins=30, density=True, label="Histogram of %ILI")

#Estimate lambda using LLN: lambda hat = 1 / sample mean   
lambda_hat = 1 / np.mean(ili_vals) 

# Generate x values for exponential PDF
x_vals = np.linspace(0, ili_vals.max(), 100) #creates 100 x values from 0 to max ILI value
exp_vals = lambda_hat * np.exp(-lambda_hat * x_vals) #computes the exponential PDF values with estimated lambda hat 

# Overlay exponential PDF
ax.plot(x_vals, exp_vals, color='red', label="Estimated Exponential PDF")
ax.set_xlabel("% ILI") #adds x label
ax.set_ylabel("Density") #adds y label
ax.set_title(f"Histogram of %ILI and Exponential Fit ({selected_state.upper()})") #add title 
ax.legend() #add legend
st.subheader("Histogram of %ILI with Exponential Overlay") #add subheader for the plot 
st.pyplot(fig)# display in Streamlit

#Header for description of histogram and exponential fit  
st.subheader("Description: Histogram of %ILI with Exponential Overlay") 
#Adds a textbox for histogram explanation
st.markdown("""
This histogram displays the %ILI values. Most %ILI values are near zero, indicating that high flu activity is rare.
This histogram uses probability density on the y-axis instead of raw counts. An overlay of the exponential probability
density function (PDF) is done based on the estimated lambda from the Law of Large Numbers. This overlay allows for the
evaluation of how the exponential model fits the observed data.
""")
