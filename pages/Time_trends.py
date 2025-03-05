import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import itertools

st.title("Time Frame Based Analysis")
st.markdown("""
In this section, we analyze lottery trends based on specific time periods. Select one of the following time frames to view detailed trends and patterns in both Big Wins and Small Wins:

""")
# Time frame options
time_frames = ["2020-2021", "2022", "2023", "2024-25"]
selected_time_frame = st.radio("Select a Time Frame:", time_frames)

# Load CSV files
bigwins_df = pd.read_csv("Assets/Csvfiles/BigWins_final.csv")
smallwins_df = pd.read_csv("Assets/Csvfiles/SmallWins.csv")

# Convert Date columns to datetime
bigwins_df["Date_dt"] = pd.to_datetime(bigwins_df["Date"], format="%d/%m/%Y", errors="coerce")
smallwins_df["Date_dt"] = pd.to_datetime(smallwins_df["Date"], format="%d/%m/%Y", errors="coerce")

# Function to filter data based on selected time frame
def filter_time_frame(df, col="Date_dt", tf=selected_time_frame):
    if tf == "2020-2021":
        return df[df[col].dt.year.isin([2020, 2021])]
    elif tf == "2022":
        return df[df[col].dt.year == 2022]
    elif tf == "2023":
        return df[df[col].dt.year == 2023]
    elif tf == "2024-25":
        return df[df[col].dt.year.isin([2024, 2025])]
    else:
        return df

# Filter datasets for the selected time frame
bigwins_tf = filter_time_frame(bigwins_df)
smallwins_tf = filter_time_frame(smallwins_df)

st.write(f"## Time Frame: {selected_time_frame}")

######################################
# Big Wins Analysis for Selected Time Frame
######################################
st.write("#### Big Wins Analysis")

# Create a 6-digit WinningNumber column
bigwins_tf["WinningNumber"] = bigwins_tf["Number"].astype(str).str.zfill(6)

# 1. Frequency of digits for each of the 6 positions
freq_big_tf = pd.DataFrame(0, index=[str(d) for d in range(10)],
                           columns=[f"Position {i}" for i in range(1, 7)])
for num in bigwins_tf["WinningNumber"]:
    for i, digit in enumerate(num):
        freq_big_tf.loc[digit, f"Position {i+1}"] += 1

st.write("**Digit Frequency Distribution (Big Wins)**")
st.dataframe(freq_big_tf)

# Plot frequency per position using Plotly subplots (2 rows x 3 cols)
fig_big_tf = make_subplots(rows=2, cols=3, subplot_titles=list(freq_big_tf.columns))
for i, pos in enumerate(freq_big_tf.columns):
    row = i // 3 + 1
    col = i % 3 + 1
    fig_big_tf.add_trace(
        go.Bar(x=freq_big_tf.index, y=freq_big_tf[pos], marker_color="dodgerblue"),
        row=row, col=col
    )
    fig_big_tf.update_xaxes(title_text="Digit", row=row, col=col)
    fig_big_tf.update_yaxes(title_text="Count", row=row, col=col)

fig_big_tf.update_layout(title_text="Digit Frequency by Position (Big Wins)", 
                         margin=dict(l=20, r=20, t=50, b=20))
st.plotly_chart(fig_big_tf, use_container_width=True)

# 2. Most probable combination: select the digit with the highest frequency at each position
most_probable_big = "".join([freq_big_tf[col].idxmax() for col in freq_big_tf.columns])
st.write(f"**Most Probable Combination (Big Wins):** {most_probable_big}")

matching_most_prob_big = bigwins_tf[bigwins_tf["WinningNumber"] == most_probable_big]
if not matching_most_prob_big.empty:
    st.write("**Entries where the most probable combination has won:**")
    st.dataframe(matching_most_prob_big[["Date", "Series", "Amount", "Number", "Place"]])
else:
    st.write("The most probable combination has not won in Big Wins for this time frame.")

# 3. Top 10 winning locations for this time frame (Bar Chart)
location_counts = bigwins_tf["Place"].value_counts().reset_index()
location_counts.columns = ["Place", "Win Count"]
top10_locations = location_counts.head(10)
fig_loc = px.bar(
    top10_locations,
    x="Win Count",
    y="Place",
    orientation="h",
    color="Win Count",
    color_continuous_scale=px.colors.sequential.Plasma,
    title="Top 10 Winning Locations (Big Wins)"
)
fig_loc.update_layout(yaxis={'categoryorder': 'total ascending'},
                      xaxis_title="Win Count", yaxis_title="Place",
                      margin=dict(l=20, r=20, t=50, b=20))
st.plotly_chart(fig_loc, use_container_width=True)

# 4. Most frequent winning number and its details
winning_number_stats = bigwins_tf.groupby("WinningNumber").agg(
    Win_Count=("WinningNumber", "count"),
    Total_Amount=("Amount", "sum")
).reset_index().sort_values("Win_Count", ascending=False)
st.write("**Most Frequent Winning Numbers (Big Wins):**")
st.dataframe(winning_number_stats.head(10))

######################################
# Small Wins Analysis for Selected Time Frame
######################################
st.write("#### Small Wins Analysis")

# Create a 4-digit WinningNumber column
smallwins_tf["WinningNumber"] = smallwins_tf["Number"].astype(str).str.zfill(4)

# 1. Top 20 winning numbers with win count and total amount
small_number_stats = smallwins_tf.groupby("WinningNumber").agg(
    Win_Count=("WinningNumber", "count"),
    Total_Amount=("Amount", "sum")
).reset_index().sort_values("Win_Count", ascending=False)
st.write("**Top 20 Winning Numbers (Small Wins):**")
st.dataframe(small_number_stats.head(20),width=500)

# 2. Frequency of digits for each of the 4 positions
freq_small_tf = pd.DataFrame(0, index=[str(d) for d in range(10)],
                             columns=[f"Position {i}" for i in range(1, 5)])
for num in smallwins_tf["WinningNumber"]:
    for i, digit in enumerate(num):
        freq_small_tf.loc[digit, f"Position {i+1}"] += 1
st.write("**Digit Frequency Distribution (Small Wins)**")
st.dataframe(freq_small_tf)

# Plot frequency per position for small wins using Plotly subplots (1 row x 4 cols)
fig_small_tf = make_subplots(rows=1, cols=4, subplot_titles=list(freq_small_tf.columns))
for i, pos in enumerate(freq_small_tf.columns):
    fig_small_tf.add_trace(
        go.Bar(x=freq_small_tf.index, y=freq_small_tf[pos], marker_color="coral"),
        row=1, col=i+1
    )
    fig_small_tf.update_xaxes(title_text="Digit", row=1, col=i+1)
    fig_small_tf.update_yaxes(title_text="Count", row=1, col=i+1)
fig_small_tf.update_layout(title_text="Digit Frequency by Position (Small Wins)",
                           margin=dict(l=20, r=20, t=50, b=20))
st.plotly_chart(fig_small_tf, use_container_width=True)

# 3. Predicted Combinations Check for Small Wins (16 combinations)
likely_digits_small_tf = []
for pos in freq_small_tf.columns:
    top_two_small = freq_small_tf[pos].nlargest(2).index.tolist()
    likely_digits_small_tf.append(top_two_small)
predicted_combinations_small_tf = [''.join(comb) for comb in itertools.product(*likely_digits_small_tf)]
predicted_small_str_tf = ", ".join(predicted_combinations_small_tf)
st.write("**Predicted 4-Digit Combinations (16 total) for Small Wins:**")
st.markdown(f'<p style="color: green;">{predicted_small_str_tf}</p>', unsafe_allow_html=True)

matching_combinations_small_tf = smallwins_tf[smallwins_tf["WinningNumber"].isin(predicted_combinations_small_tf)]
if not matching_combinations_small_tf.empty:
    df_matching_small_tf = matching_combinations_small_tf.groupby("WinningNumber").agg(
         Win_Count=("WinningNumber", "count"),
         Total_Amount=("Amount", "sum")
    ).reset_index().rename(columns={"WinningNumber": "Predicted Combination"})
    st.write("**Predicted Combinations Win Count and Total Amount (Small Wins):**")
    st.dataframe(df_matching_small_tf,width=500)
else:
    st.write("None of the predicted 16 combinations have won in Small Wins.")

# 4. Check if the most probable combination (for small wins) has won
most_probable_small = "".join([freq_small_tf[col].idxmax() for col in freq_small_tf.columns])
st.write(f"**Most Probable Combination (Small Wins):** {most_probable_small}")
matching_most_prob_small = smallwins_tf[smallwins_tf["WinningNumber"] == most_probable_small]
if not matching_most_prob_small.empty:
    st.write("**Entries where the most probable combination has won (Small Wins):**")
    st.dataframe(matching_most_prob_small[["Date", "Series", "Amount", "Number"]])
else:
    st.write("The most probable combination has not won in Small Wins for this time frame.")
