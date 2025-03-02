
import streamlit as st
import streamlit as st

# App Title
st.title("Kerala Lottery Data Analysis")




st.header("Introduction")
st.write("""
Lotteries have fascinated people for decades, offering a mix of luck and probability. 
During my recent visit to Kerala, I noticed how people approached buying lottery tickets. 
Many believed that numbers with repeating digits were less likely to win, despite the fact that all numbers should have an equal probability of being drawn. 

This observation sparked my curiosity. I wanted to analyze historical lottery data to see if there were any patterns, biases, or trends in the results.

To investigate this, I scraped over **1,000 PDFs** from official Kerala government sources, compiling a dataset of more than **400,000 entries**. 
The goal of this project is to analyze whether certain numbers are drawn more or less frequently than expected, as well as explore trends related to prize distribution, locations, and winning amounts.
""")

st.header("Understanding the Kerala State Lottery System")
st.write("""
The Kerala State Lottery system is run by the state government and operates different lottery schemes on specific days of the week. 
Each lottery follows a structured format, with tickets sold under different series, and winners are selected through a random draw.

Prizes are categorized based on matching either the full ticket number and series or just a portion of the ticket number. These categories include:

- **Big Wins** – To win, the ticket's full 6-digit number and series must match exactly. This category includes the first, second, and third prize winners.
- **Small Wins** – Only the last four digits of the ticket number need to match the drawn number, making this category more accessible to a larger number of winners.

The lottery system is designed to be random, ensuring fairness in the selection process. However, public perception and buying habits suggest that not all numbers are considered equally desirable by players.
""")

st.header("Data Collection and Structure")
st.write("""
To conduct this analysis, I scraped historical lottery results directly from official government PDFs, which are publicly available. 
After processing the data, I created two structured datasets:
""")

st.subheader("1. Big Wins Dataset")
st.write("""
This dataset includes information about the top prize winners where the entire ticket number and series must match to win.

**Columns:**
- **Date** – The date of the lottery draw
- **Series** – The ticket series identifier
- **Number** – The full 6-digit winning number
- **Amount** – The prize amount for that entry
- **Location** – The place where the ticket was sold
- **SN (Serial + Number)** – A combined field of the ticket's serial and number
""")

st.subheader("2. Small Wins Dataset")
st.write("""
This dataset records winners where only the last four digits of the ticket number need to match.

**Columns:**
- **Date** – The date of the lottery draw
- **Series** – The ticket series identifier
- **Number** – The last four digits of the winning number
- **Amount** – The prize amount for that entry

By analyzing these datasets, I aim to uncover whether certain number patterns occur more frequently, how prize distribution varies across locations, and whether there are any unexpected irregularities in the draws.
""")


