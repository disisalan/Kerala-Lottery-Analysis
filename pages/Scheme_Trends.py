import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import itertools

st.title("Scheme Wise Analysis: Big Wins & Small Wins")
st.write("This is a scheme wise analysis of the data. Refer to `About the data` page to know more about each scheme .Select a scheme to analyze both Big Wins and Small Wins data using the radio buttons below:")

# Define available schemes and their corresponding code (Series prefix)
schemes = {
    "Win Win (W)": "W",
    "Akshaya (AK)": "AK",
    "Stree Shakti (SS)": "SS",
    "Karunya Plus (KN)": "KN",
    "Nirmal (NR)": "NR",
    "Karunya (KR)": "KR",
    "Fifty Fifty (FF)": "FF"
}
selected_scheme_name = st.radio("Select a Scheme:", list(schemes.keys()))
selected_scheme_code = schemes[selected_scheme_name]

# Load CSV files for Big Wins and Small Wins
bigwins_df = pd.read_csv("Assets/Csvfiles/BigWins_final.csv")
smallwins_df = pd.read_csv("Assets/Csvfiles/SmallWins.csv")

# Filter datasets based on the scheme code (matching the prefix in the Series column)
bigwins_scheme = bigwins_df[bigwins_df["Series"].str.startswith(selected_scheme_code)].copy()
smallwins_scheme = smallwins_df[smallwins_df["Series"].str.startswith(selected_scheme_code)].copy()

########################################
# BIG WINS ANALYSIS
########################################
st.write(f"## 1.Big Wins Analysis for {selected_scheme_name}")
st.markdown("""
For each lottery scheme, we calculate the frequency of digits in the winning numbers. This analysis examines the occurrence of each digit (0-9) across the different positions in the winning number for each scheme. By comparing these distributions, we can identify patterns or anomalies unique to each scheme.
""")
st.markdown(
    '<div style="background-color: #c9fac5; padding: 10px; border-radius: 5px;">'
    '<strong>Insight:</strong> The digit frequency does not indicate a favourable probablity to any number or range of numbers.'
    '</div>', unsafe_allow_html=True)
# 1. Frequency of digits at each position (6-digit winning numbers)
bigwins_scheme["WinningNumber"] = bigwins_scheme["Number"].astype(str).str.zfill(6)
# Create a DataFrame to store digit frequencies for positions 1 to 6
freq_big = pd.DataFrame(0, index=[str(d) for d in range(10)],
                        columns=[f"Position {i}" for i in range(1, 7)])
for num in bigwins_scheme["WinningNumber"]:
    for i, digit in enumerate(num):
        freq_big.loc[digit, f"Position {i+1}"] += 1

st.write("#### Digit Frequency Distribution in Winning Numbers (Big Wins)")
st.dataframe(freq_big)

# Create subplots for each of the 6 digit positions using Plotly
fig_big = make_subplots(rows=2, cols=3, subplot_titles=list(freq_big.columns))
positions = list(freq_big.columns)
for i, pos in enumerate(positions):
    row = i // 3 + 1
    col = i % 3 + 1
    fig_big.add_trace(
        go.Bar(x=freq_big.index, y=freq_big[pos], marker_color="dodgerblue"),
        row=row, col=col
    )
    fig_big.update_xaxes(title_text="Digit", row=row, col=col)
    fig_big.update_yaxes(title_text="Count", row=row, col=col)
fig_big.update_layout(title_text="Digit Frequency by Position (Big Wins)", height=600, width=900)
st.plotly_chart(fig_big, use_container_width=True)

# 2. Top 10 winning locations for this scheme
top_locations_big = bigwins_scheme["Place"].value_counts().reset_index()
top_locations_big.columns = ["Place", "Win Count"]

st.write("#### Top 10 Winning Locations (Big Wins)")
st.markdown("""
This analysis identifies the top 10 locations that have won the most prizes in the Big Wins dataset. The win counts are calculated by counting the number of winning entries for each location, and the results are visualized using a horizontal bar chart to highlight the locations with the highest frequency of wins.
""")
st.markdown(
    '<div style="background-color: #c9fac5; padding: 10px; border-radius: 5px;">'
    '<strong>Insight:</strong> This is again highly correspondes to the sales of tickets in these areas but since no data is available , no concrete statement can be made.'
    '</div><br> ', unsafe_allow_html=True)
st.dataframe(top_locations_big.head(10))

# Horizontal bar chart for top 10 winning locations using Plotly Express
fig_loc_big = px.bar(
    top_locations_big.head(10),
    x="Win Count",
    y="Place",
    orientation="h",
    color="Win Count",
    color_continuous_scale=px.colors.sequential.Plasma,
    title="Top 10 Winning Locations in Big Wins"
)
fig_loc_big.update_layout(yaxis={'categoryorder': 'total ascending'},
                          xaxis_title="Win Count", yaxis_title="Place")
st.plotly_chart(fig_loc_big, use_container_width=True)

# 3. Predicted Combinations Check for Big Wins (64 combinations)
st.write("#### Predicted Combinations Check (Big Wins)")
st.markdown("""
Based on the digit frequency distribution above, the top 2 digits for each of the 6 positions are selected to predict 64 possible combinations. This analysis generates all potential 6-digit numbers based on these frequent digits and then checks which of these predicted combinations have actually won in the dataset.
""")

# Get the top 2 digits for each position and display them
likely_digits_big = []
for pos in freq_big.columns:
    top_two = freq_big[pos].nlargest(2).index.tolist()
    st.write(f"**{pos}:** {top_two}")
    likely_digits_big.append(top_two)

# Generate all possible combinations (2^6 = 64)
predicted_combinations_big = [''.join(comb) for comb in itertools.product(*likely_digits_big)]
predicted_big_str = ", ".join(predicted_combinations_big)
st.markdown(f'<p style="color: green;">{predicted_big_str}</p>', unsafe_allow_html=True)

# Check which of these predicted combinations have won in Big Wins
winning_matches_big = bigwins_scheme[bigwins_scheme["WinningNumber"].isin(predicted_combinations_big)]
st.write("#### Matching Winning Entries (Big Wins)")
if not winning_matches_big.empty:
    st.write("The following entries match one of the predicted combinations:")
    st.dataframe(winning_matches_big[["Date", "Series", "Amount", "Number"]])
else:
    st.write("None of the predicted combinations have won in Big Wins.")

########################################
# SMALL WINS ANALYSIS
########################################
st.write(f"## 2.Small Wins Analysis for {selected_scheme_name}")
st.markdown("""
In this section, we focus on the within the Small Wins dataset. We analyze the most frequently drawn winning numbers and calculate the average prize amount for each number. This helps us identify which numbers are drawn most often and understand the associated prize trends.
""")
# 1. Most winning numbers and their respective average prices
small_win_stats = smallwins_scheme.groupby("Number").agg(
    Win_Count=('Number', 'count'),
    Avg_Amount=('Amount', 'mean')
).reset_index().sort_values("Win_Count", ascending=False)

st.write("#### Most Winning Numbers and Their Respective Average Prices (Small Wins)")
st.markdown("""
In this section, we analyze the Small Wins dataset to identify the winning numbers that appear most frequently. For each winning number, we calculate its frequency as well as the average prize amount awarded. This analysis provides insights into which numbers are drawn more often and how the prize distribution varies across these numbers.
""")
st.markdown(
    '<div style="background-color: #c9fac5; padding: 10px; border-radius: 5px;">'
    '<strong>Insight:</strong> Even though some numbers are more favourable this is clearly not enough evidence as we saw in the number trends section.'
    '</div><br> ', unsafe_allow_html=True)

st.dataframe(small_win_stats.head(10))

# 2. Frequency of digits at each position (4-digit winning numbers)
smallwins_scheme["WinningNumber"] = smallwins_scheme["Number"].astype(str).str.zfill(4)
freq_small = pd.DataFrame(0, index=[str(d) for d in range(10)],
                           columns=[f"Position {i}" for i in range(1, 5)])
for num in smallwins_scheme["WinningNumber"]:
    for i, digit in enumerate(num):
        freq_small.loc[digit, f"Position {i+1}"] += 1

st.write("#### Digit Frequency Distribution in Winning Numbers (Small Wins)")
st.markdown("""
In this section, we analyze the frequency distribution of digits in the winning numbers from the Small Wins dataset. Each winning number is represented as a 4-digit string, and we calculate the occurrence of each digit (0-9) for every position (first through fourth). This helps reveal any underlying biases or patterns in the lottery draws.
""")
st.markdown(
    '<div style="background-color: #c9fac5; padding: 10px; border-radius: 5px;">'
    '<strong>Insight:</strong> While digit frequency might fluctuate a little , it is not enought to establish a pattern , moreover a higher frequent number doesn\'t gaurantee a higher win amount.'
    '</div><br> ', unsafe_allow_html=True)

st.dataframe(freq_small)

# Create subplots for 4-digit positions using Plotly
fig_small = make_subplots(rows=1, cols=4, subplot_titles=list(freq_small.columns))
for i, pos in enumerate(freq_small.columns):
    fig_small.add_trace(
        go.Bar(x=freq_small.index, y=freq_small[pos], marker_color="coral"),
        row=1, col=i+1
    )
    fig_small.update_xaxes(title_text="Digit", row=1, col=i+1)
    fig_small.update_yaxes(title_text="Count", row=1, col=i+1)
fig_small.update_layout(title_text="Digit Frequency by Position (Small Wins)", height=400, width=1000)
st.plotly_chart(fig_small, use_container_width=True)

# 3. Predicted Combinations Check for Small Wins (16 combinations)
st.write("#### Predicted Combinations Check (Small Wins)")
st.write("For Small Wins (4-digit numbers), the top 2 digits for each position are used to predict 16 possible combinations.")

likely_digits_small = []
for pos in freq_small.columns:
    top_two_small = freq_small[pos].nlargest(2).index.tolist()
    st.write(f"**{pos}:** {top_two_small}")
    likely_digits_small.append(top_two_small)

predicted_combinations_small = [''.join(comb) for comb in itertools.product(*likely_digits_small)]
predicted_small_str = ", ".join(predicted_combinations_small)
st.markdown(f'<p style="color: green;">{predicted_small_str}</p>', unsafe_allow_html=True)

# Check which predicted combinations appear in Small Wins and calculate win count and total amount
matching_entries = smallwins_scheme[smallwins_scheme["WinningNumber"].isin(predicted_combinations_small)]
st.write("#### Predicted Combinations Win Count and Total Amount (Small Wins)")
if not matching_entries.empty:
    df_matching_small = matching_entries.groupby("WinningNumber").agg(
         Win_Count=("WinningNumber", "count"),
         Total_Amount=("Amount", "sum")
    ).reset_index().rename(columns={"WinningNumber": "Predicted Combination"})
    st.dataframe(df_matching_small)
else:
    st.write("None of the predicted combinations have won in Small Wins.")
