import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import itertools

st.title("Dynamic Amount Based Analysis")

# Unique prices as given
unique_prices = [100, 200, 500, 1000, 2000, 5000, 100000, 500000, 1000000, 7000000, 7500000, 8000000, 10000000]
selected_amount = st.radio("Select a Winning Amount:", unique_prices)

# Load CSV files for Big Wins and Small Wins
bigwins_df = pd.read_csv("Assets/Csvfiles/BigWins_final.csv")
smallwins_df = pd.read_csv("Assets/Csvfiles/SmallWins.csv")

# For amounts up to 5000 use Small Wins analysis; otherwise use Big Wins
if selected_amount <= 5000:
    st.header(f"Small Wins Analysis for Amount: {selected_amount}")
    # Filter the small wins data by the selected amount
    df = smallwins_df[smallwins_df["Amount"] == selected_amount].copy()
    
    if df.empty:
        st.write("No data available for this amount in Small Wins.")
    else:
        # --- Top 50 Winning Numbers ---
        # Calculate frequency of each winning number
        freq = df["Number"].value_counts().reset_index()
        freq.columns = ["Number", "Frequency"]
        top_50 = freq.head(50)
        
        # Split the top 50 into two lists of 25 each
        list1 = top_50.head(25)
        list2 = top_50.tail(25)
        
        st.subheader("Top 50 Winning Numbers and Their Frequencies")
        col1, col2 = st.columns(2)
        with col1:
            st.write("List 1 (Top 25):")
            st.dataframe(list1)
        with col2:
            st.write("List 2 (Next 25):")
            st.dataframe(list2)
        
        # --- Digit-wise Analysis for Small Wins ---
        # Ensure winning numbers are 4-digit strings (pad with zeros if necessary)
        df["WinningNumber"] = df["Number"].astype(str).str.zfill(4)
        
        # Build a digit frequency DataFrame for each of the 4 positions
        digit_freq = pd.DataFrame(0, index=[str(d) for d in range(10)],
                                  columns=[f"Position {i}" for i in range(1, 5)])
        for num in df["WinningNumber"]:
            for i, digit in enumerate(num):
                digit_freq.loc[digit, f"Position {i+1}"] += 1
        
        st.subheader("Digit Frequency Distribution (Small Wins)")
        st.dataframe(digit_freq)
        
        # Display the most frequent digit for each position
        most_freq = {}
        for pos in digit_freq.columns:
            most_freq[pos] = digit_freq[pos].idxmax()
        st.write("Most Frequent Digit at Each Position:")
        st.write(most_freq)
        
        # Draw bar charts for each digit position using Plotly
        fig_small = make_subplots(rows=1, cols=4, subplot_titles=list(digit_freq.columns))
        for i, pos in enumerate(digit_freq.columns):
            fig_small.add_trace(
                go.Bar(x=digit_freq.index, y=digit_freq[pos], marker_color="coral"),
                row=1, col=i+1
            )
            fig_small.update_xaxes(title_text="Digit", row=1, col=i+1)
            fig_small.update_yaxes(title_text="Count", row=1, col=i+1)
        fig_small.update_layout(title_text="Digit Frequency by Position (Small Wins)", height=400, width=1000)
        st.plotly_chart(fig_small, use_container_width=True)

else:
    st.header(f"Big Wins Analysis for Amount: {selected_amount}")
    # Filter the big wins data by the selected amount
    df = bigwins_df[bigwins_df["Amount"] == selected_amount].copy()
    
    if df.empty:
        st.write("No data available for this amount in Big Wins.")
    else:
        # --- Top 10 Winning Numbers ---
        freq = df["Number"].value_counts().reset_index()
        freq.columns = ["Number", "Frequency"]
        top_10 = freq.head(10)
        st.subheader("Top 10 Winning Numbers and Their Frequencies")
        st.dataframe(top_10)
        
        # --- Digit-wise Analysis for Big Wins ---
        # Ensure winning numbers are 6-digit strings
        df["WinningNumber"] = df["Number"].astype(str).str.zfill(6)
        
        # Build a digit frequency DataFrame for each of the 6 positions
        digit_freq = pd.DataFrame(0, index=[str(d) for d in range(10)],
                                  columns=[f"Position {i}" for i in range(1, 7)])
        for num in df["WinningNumber"]:
            for i, digit in enumerate(num):
                digit_freq.loc[digit, f"Position {i+1}"] += 1
        
        st.subheader("Digit Frequency Distribution (Big Wins)")
        st.dataframe(digit_freq)
        
        # Display the most frequent digit for each position
        most_freq = {}
        for pos in digit_freq.columns:
            most_freq[pos] = digit_freq[pos].idxmax()
        st.write("Most Frequent Digit at Each Position:")
        st.write(most_freq)
        
        # Draw bar charts for each digit position using Plotly
        fig_big = make_subplots(rows=2, cols=3, subplot_titles=list(digit_freq.columns))
        for i, pos in enumerate(digit_freq.columns):
            row = i // 3 + 1
            col = i % 3 + 1
            fig_big.add_trace(
                go.Bar(x=digit_freq.index, y=digit_freq[pos], marker_color="dodgerblue"),
                row=row, col=col
            )
            fig_big.update_xaxes(title_text="Digit", row=row, col=col)
            fig_big.update_yaxes(title_text="Count", row=row, col=col)
        fig_big.update_layout(title_text="Digit Frequency by Position (Big Wins)", height=600, width=900)
        st.plotly_chart(fig_big, use_container_width=True)
        
        # --- Predicted Combinations Based on Digit Frequency ---
        st.subheader("Predicted Combinations Check (Big Wins)")
        likely_digits = []
        for pos in digit_freq.columns:
            top_two = digit_freq[pos].nlargest(2).index.tolist()
            st.write(f"**{pos}:** {top_two}")
            likely_digits.append(top_two)
        # Generate 64 predicted combinations (2^6)
        predicted_combinations = [''.join(comb) for comb in itertools.product(*likely_digits)]
        predicted_str = ", ".join(predicted_combinations)
        st.markdown(f'<p style="color: green;">{predicted_str}</p>', unsafe_allow_html=True)
        
        # Check which predicted combinations actually won
        winning_matches = df[df["WinningNumber"].isin(predicted_combinations)]
        st.subheader("Matching Winning Entries (Big Wins)")
        if not winning_matches.empty:
            st.write("The following entries match one of the predicted combinations:")
            st.dataframe(winning_matches[["Date", "Series", "Amount", "Number"]])
        else:
            st.write("None of the predicted combinations have won.")
        
        # --- Top 10 Locations to Win that Price ---
        st.subheader("Top 10 Winning Locations (Big Wins)")
        loc_counts = df["Place"].value_counts().reset_index()
        loc_counts.columns = ["Place", "Win Count"]
        top_locations = loc_counts.head(10)
        st.dataframe(top_locations)
        fig_loc = px.bar(
            top_locations,
            x="Win Count",
            y="Place",
            orientation="h",
            color="Win Count",
            color_continuous_scale=px.colors.sequential.Plasma,
            title="Top 10 Winning Locations (Big Wins)"
        )
        fig_loc.update_layout(yaxis={'categoryorder': 'total ascending'},
                              xaxis_title="Win Count",
                              yaxis_title="Place")
        st.plotly_chart(fig_loc, use_container_width=True)
