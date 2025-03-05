import streamlit as st
import pandas as pd

st.title("About the Data")

st.subheader("Data Source")
st.markdown("""
The lottery results are drawn daily at **3:00 PM** and published on the official government website shortly after the draw. The website organizes each lottery scheme into two sections: **Old** and **New**. For this analysis, data was collected from the **New** section for results between **March 2021** and **August 2023**.

Since the results were available only in PDF format, over **1000 PDFs** were scraped to compile a comprehensive dataset of more than **400,000 records**, with each record representing an individual win.
""", unsafe_allow_html=True)

st.write('''**The scripts used for scrapping the sites and pdfs have been published on the Github Repo of this project and are free to use. Given you can understand it lol !!!** \n
All the generated data set for each scheme , combined data sets and the original pdfs used are all avilable on both the Github Repo and Kaggle.
''')

st.subheader("Data Cleaning and Mining")
st.write("After downloading the pdfs each pdf was then read to extract information like draw date , Series , Scheme , Each price and all its wins .Since it was easier to go scheme by scheme first all the Individual Scheme dataset were made and then combined to make the final dataset referred to as **Big Wins** and **Small Wins**.")

st.write("**1. Big Wins Dataset**")
st.write("""
This dataset includes information about the top prize winners where the entire ticket number and series must match to win.

**Columns:**
- **Date** – The date of the lottery draw
- **Series** – The ticket Scheme identifier
- **Serial** – The Series of the Number
- **Number** – The full 6-digit winning number
- **Amount** – The prize amount for that entry
- **Location** – The place where the ticket was sold
- **SN (Serial + Number)** – A combined field of the ticket's serial and number
""")
# Load the datasets
bigwins_df = pd.read_csv("Assets/Csvfiles/BigWins_final.csv")



st.write("Big Wins - First 10 Entries")
st.dataframe(bigwins_df.head(10), use_container_width=True)

st.write("**2. Small Wins Dataset**")
st.write("""
This dataset records winners where only the last four digits of the ticket number need to match.

**Columns:**
- **Date** – The date of the lottery draw
- **Series** – The ticket series identifier
- **Number** – The last four digits of the winning number
- **Amount** – The prize amount for that entry

By analyzing these datasets, I aim to uncover whether certain number patterns occur more frequently, how prize distribution varies across locations, and whether there are any unexpected irregularities in the draws.
""")
st.caption("The Zeroes before the whole numbers are not shown in the df  i.e 0028 is represented as 28 , look at eg 1")
smallwins_df = pd.read_csv("Assets/Csvfiles/SmallWins.csv")
st.write("Small Wins - First 10 Entries")
st.dataframe(smallwins_df.head(10), use_container_width=True)