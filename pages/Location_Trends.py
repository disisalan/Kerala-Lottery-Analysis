import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import itertools

# Configure page layout
st.set_page_config(layout="wide")

# Load data
bigwins_df = pd.read_csv("Assets/Csvfiles/BigWins_final.csv")

########################################
# Most Winning Places
########################################
st.title("Location Trends")

st.write("## 1. Most Winning Places")
st.markdown("""
This section displays the top 10 locations that have won the most big prizes, along with the complete list of all locations and their respective number of wins.
- **Top 10 Locations with Most Wins**
- **Complete List of Locations and Their Win Counts**
""")
# Calculate the win count per location
win_counts = bigwins_df["Place"].value_counts().reset_index()
win_counts.columns = ["Place", "Win Count"]

# Top 10 winning locations
top_10 = win_counts.head(10)

st.subheader("Top 10 Locations with Most Wins")
st.dataframe(top_10,width=500)

# Create a horizontal bar chart for the top 10 using Plotly Express
fig_top10 = px.bar(
    top_10,
    x="Win Count",
    y="Place",
    orientation="h",
    color="Win Count",
    color_continuous_scale=px.colors.sequential.Blues,
    title="Top 10 Winning Locations",
)
fig_top10.update_layout(yaxis={'categoryorder': 'total ascending'},
                        xaxis_title="Win Count",
                        yaxis_title="Location")
st.plotly_chart(fig_top10, use_container_width=True)

st.markdown(
    '<div style="background-color: #c9fac5; padding: 10px; border-radius: 5px;">'
    '<strong>Insight:</strong> Ernakulam seems to be the most winning location but that could directly be related to the number of tickets sold in the particular place . Since that data is not public no research could be done for that.'
    '</div>', unsafe_allow_html=True)

st.write("### Complete List of Locations and Their Win Counts")
st.dataframe(win_counts,width=500)
st.markdown(
    '<div style="background-color: #c9fac5; padding: 10px; border-radius: 5px;">'
    '<strong>Insight:</strong> While this might show a clear bias to some locations according to my research these seem to be the areas where the most lotteries are sold and hence the wins are directly proportional to it.'
    '</div>', unsafe_allow_html=True)
########################################
# Least Winning Locations
########################################
st.write("## 2. Least Winning Locations")
st.write(
    "This section displays the locations with the fewest wins along with the maximum winning amount they received and the total win count."
)

st.markdown(
    '<div style="background-color: #c9fac5; padding: 10px; border-radius: 5px;">'
    '<strong>Insight:</strong> Again the analysis might be strongly correlated to the number of ticket sales in each area.'
    '</div>', unsafe_allow_html=True)
# Group data by Place to compute win count and max win amount for each location
least_wins = bigwins_df.groupby("Place").agg({
    "Amount": "max",
    "Place": "count"
}).rename(columns={"Place": "Win Count", "Amount": "Max Win Amount"}).reset_index()

# Sort by win count in ascending order
least_wins = least_wins.sort_values("Win Count", ascending=True)

# Bottom 10 locations by win count
bottom_10 = least_wins.head(10)

# Plot the bottom 10 as a horizontal bar chart
fig_bottom10 = px.bar(
    bottom_10,
    x="Win Count",
    y="Place",
    orientation="h",
    color="Win Count",
    color_continuous_scale=px.colors.sequential.Reds,
    title="Bottom 10 Locations by Win Count",
)
fig_bottom10.update_layout(yaxis={'categoryorder': 'total ascending'},
                           xaxis_title="Win Count",
                           yaxis_title="Location")
st.plotly_chart(fig_bottom10, use_container_width=True)

########################################
# Dynamic Results for a Specific Place
########################################
st.write("## 3. Dynamic Results for a Specific Place")
st.write(
    "Enter a location to see its total wins and the frequency distribution of each digit (0-9) for each of the 6-digit winning numbers from the big wins dataset. By default, data for Ernakulam is shown."
)

# Text input for place with default value "Ernakulam"
place_input = st.text_input("Enter a Place (e.g., THRISSUR):", value="Ernakulam")

# Filter the data for the input place (case-insensitive)
filtered = bigwins_df[bigwins_df["Place"].str.upper() == place_input.strip().upper()].copy()

# Count the wins for the place
win_count = len(filtered)
st.write(f"**Total Wins for {place_input.strip().upper()}:** {win_count}")

# Ensure the winning numbers are 6-digit strings (padding with zeros if needed)
filtered["WinningNumber"] = filtered["Number"].astype(str).str.zfill(6)

# Initialize a DataFrame to store digit frequencies for each of the 6 positions
digit_freq = pd.DataFrame(0, index=[str(d) for d in range(10)],
                          columns=[f"Position {i}" for i in range(1, 7)])

# Calculate frequency counts for each digit in each position
for num in filtered["WinningNumber"]:
    for i, digit in enumerate(num):
        col = f"Position {i+1}"
        digit_freq.loc[digit, col] += 1

st.write("#### Digit Frequency Distribution Table for Each Position (Big Wins)")
st.markdown(
    '<div style="background-color: #c9fac5; padding: 10px; border-radius: 5px;">'
    '<strong>Insight:</strong> Regardless of the area the digit distribution remain the same more or less.'
    '</div>', unsafe_allow_html=True)
st.dataframe(digit_freq)

st.subheader("Digit Frequency Distribution Bar Charts by Position")
st.markdown(
    '<div style="background-color: #c9fac5; padding: 10px; border-radius: 5px;">'
    '<strong>Insight:</strong> While some digits might look favourable to certain places the cases is does not hold when forward tested.'
    '</div>', unsafe_allow_html=True)
# Create subplots for all 6 positions using Plotly
fig_subplots = make_subplots(rows=2, cols=3, subplot_titles=digit_freq.columns)
positions = list(digit_freq.columns)
for i, pos in enumerate(positions):
    row = i // 3 + 1
    col = i % 3 + 1
    fig_subplots.add_trace(
        go.Bar(x=digit_freq.index, y=digit_freq[pos], marker_color="mediumseagreen"),
        row=row, col=col
    )
fig_subplots.update_layout(
    title_text="Digit Frequency Distribution by Position",
    showlegend=False,
    height=600,
    width=900,
    margin=dict(t=100)
)
st.plotly_chart(fig_subplots, use_container_width=True)

########################################
# Most Likely 6-Digit Combinations
########################################
st.subheader("Most Likely 6-Digit Combinations")
st.write(
    "For each of the 6 positions in the winning number, we select the top 2 most frequent digits. Based on these, the following predicted combinations are generated:"
)
st.markdown(
    '<div style="background-color: #c9fac5; padding: 10px; border-radius: 5px;">'
    '<strong>Insight:</strong>These most probable six digit combination only indicate one win which is not significant given the size of the dataset.'
    '</div>', unsafe_allow_html=True)
# For each position, get the top 2 digits by frequency and display them.
likely_digits = []
for pos in digit_freq.columns:
    top_two = digit_freq[pos].nlargest(2).index.tolist()
    st.write(f"**{pos}**: {top_two}")
    likely_digits.append(top_two)

# Generate all possible combinations (2^6 = 64 combinations)
likely_combinations = list(itertools.product(*likely_digits))
likely_combinations_str = [''.join(comb) for comb in likely_combinations]

# Display predicted combinations (one per line)
combinations_output = "\n".join(likely_combinations_str)
st.text_area("Predicted Combinations", value=combinations_output, height=200)

# Check if any of these combinations won in the big wins dataset
bigwins_df["WinningNumber"] = bigwins_df["Number"].astype(str).str.zfill(6)
winning_rows = bigwins_df[bigwins_df["WinningNumber"].isin(likely_combinations_str)]

st.subheader("Predicted Combinations That Actually Won")
if not winning_rows.empty:
    st.write("The following winning numbers match the predicted combinations. Full details are provided below:")
    st.dataframe(winning_rows[["Date", "Series", "Amount", "Number"]])
else:
    st.write("None of the predicted combinations have won in the data.")
