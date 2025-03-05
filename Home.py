
import streamlit as st
import streamlit as st

# App Title
st.title("Kerala Lottery Data Analysis")




st.header("Inspiration")
st.write("""
Lotteries have fascinated people for decades, offering a mix of luck and probability. 
During my recent visit to Kerala, I noticed how people approached buying lottery tickets. 
Many believed that numbers with repeating digits were less likely to win, despite the fact that all numbers should have an equal probability of being drawn. 
""")
st.header("Aim")

st.write("""
This observation sparked my curiosity. I wanted to analyze historical lottery data to see if there were any patterns, biases, or trends in the results.
The goal of this project is to analyze whether certain numbers are drawn more or less frequently than expected, as well as explore **trends related to prize distribution, locations, and winning amounts.**
""")



st.subheader("Understanding Kerala Lotteries")

st.markdown("""
Kerala, often called "God's Own Country," launched its government-run paper lottery system in 1967. Conceived to generate revenue and support the needy, the first lottery ticket was issued in January 1968. Today, Kerala State Lotteries are known for their transparency and reliability.

For the top three prizes, you must match both the serial and the full winning number. Prizes from fourth to eighth are won by matching only the last four digits.
""", unsafe_allow_html=True)

st.markdown("---")

# Weekly Lotteries Section
st.subheader("📅 Weekly Lotteries")
st.markdown("""
<div style="font-size: 16px;">
Kerala holds a lottery draw <span style="font-weight: bold;">every day</span> at <span style="font-weight: bold;">3:00 PM</span> in Thiruvananthapuram. Each day features a different lottery with its own ticket price and first prize:
</div>
""", unsafe_allow_html=True)

st.markdown("""
- <strong>Monday (Win Win):</strong> Ticket <strong>Rs 40</strong>; First Prize <strong>Rs 75,00,000</strong>  
- <strong>Tuesday (Sthree Shakthi):</strong> Ticket <strong>Rs 40</strong>; First Prize <strong>Rs 75,00,000</strong> 
- <strong>Wednesday (Fifty Fifty):</strong> Ticket <strong>Rs 50</strong>; First Prize <strong>Rs 1,00,00,000</strong>  
- <strong>Thursday (Karunya Plus):</strong> Ticket <strong>Rs 40</strong>; First Prize <strong>Rs 80,00,000</strong> 
- <strong>Friday (Nirmal):</strong> Ticket <strong>Rs 40</strong>; First Prize <strong>Rs 70,00,000</strong> 
- <strong>Saturday (Karunya):</strong> Ticket <strong>Rs 40</strong>; First Prize <strong>Rs 80,00,000</strong>  
- <strong>Sunday (Akshaya):</strong> Ticket <strong>Rs 40</strong>; First Prize <strong>Rs 70,00,000</strong> 
""", unsafe_allow_html=True)



