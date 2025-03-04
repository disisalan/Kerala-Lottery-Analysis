import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import itertools

st.title("Time Frame Based Analysis")

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

st.header(f"Time Frame: {selected_time_frame}")

######################################
# Big Wins Analysis for Selected Time Frame
######################################
st.subheader("Big Wins Analysis")

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

# Plot frequency per position
fig_big_tf, axs_big_tf = plt.subplots(2, 3, figsize=(18, 10))
axs_big_tf = axs_big_tf.flatten()
for idx, pos in enumerate(freq_big_tf.columns):
    axs_big_tf[idx].bar(freq_big_tf.index, freq_big_tf[pos], color="dodgerblue")
    axs_big_tf[idx].set_title(f"Frequency at {pos}")
    axs_big_tf[idx].set_xlabel("Digit")
    axs_big_tf[idx].set_ylabel("Count")
plt.tight_layout()
st.pyplot(fig_big_tf)

# 2. Most probable combination: select the digit with the highest frequency at each position
most_probable_big = "".join([freq_big_tf[col].idxmax() for col in freq_big_tf.columns])
st.write(f"**Most Probable Combination (Big Wins):** {most_probable_big}")

matching_most_prob_big = bigwins_tf[bigwins_tf["WinningNumber"] == most_probable_big]
if not matching_most_prob_big.empty:
    st.write("**Entries where the most probable combination has won:**")
    st.dataframe(matching_most_prob_big[["Date", "Series", "Amount", "Number", "Place"]])
else:
    st.write("The most probable combination has not won in Big Wins for this time frame.")

# 3. Top 10 winning locations for this time frame (Bar Chart Only)
location_counts = bigwins_tf["Place"].value_counts().reset_index()
location_counts.columns = ["Place", "Win Count"]
top10_locations = location_counts.head(10)
fig_loc, ax_loc = plt.subplots(figsize=(10, 6))
ax_loc.barh(top10_locations["Place"], top10_locations["Win Count"], color="mediumslateblue")
ax_loc.set_xlabel("Win Count")
ax_loc.set_ylabel("Place")
ax_loc.set_title("Top 10 Winning Locations (Big Wins)")
ax_loc.invert_yaxis()
st.pyplot(fig_loc)

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
st.subheader("Small Wins Analysis")

# Create a 4-digit WinningNumber column
smallwins_tf["WinningNumber"] = smallwins_tf["Number"].astype(str).str.zfill(4)

# 1. Top 20 winning numbers with win count and total amount
small_number_stats = smallwins_tf.groupby("WinningNumber").agg(
    Win_Count=("WinningNumber", "count"),
    Total_Amount=("Amount", "sum")
).reset_index().sort_values("Win_Count", ascending=False)
st.write("**Top 20 Winning Numbers (Small Wins):**")
st.dataframe(small_number_stats.head(20))

# 2. Frequency of digits for each of the 4 positions
freq_small_tf = pd.DataFrame(0, index=[str(d) for d in range(10)],
                             columns=[f"Position {i}" for i in range(1, 5)])
for num in smallwins_tf["WinningNumber"]:
    for i, digit in enumerate(num):
        freq_small_tf.loc[digit, f"Position {i+1}"] += 1
st.write("**Digit Frequency Distribution (Small Wins)**")
st.dataframe(freq_small_tf)

# Plot frequency per position for small wins
fig_small_tf, axs_small_tf = plt.subplots(1, 4, figsize=(20, 5))
for idx, pos in enumerate(freq_small_tf.columns):
    axs_small_tf[idx].bar(freq_small_tf.index, freq_small_tf[pos], color="coral")
    axs_small_tf[idx].set_title(f"Frequency at {pos}")
    axs_small_tf[idx].set_xlabel("Digit")
    axs_small_tf[idx].set_ylabel("Count")
st.pyplot(fig_small_tf)

# 3. Predicted Combinations Check for Small Wins (16 combinations)
# Use the top 2 digits for each position
likely_digits_small_tf = []
for pos in freq_small_tf.columns:
    top_two_small = freq_small_tf[pos].nlargest(2).index.tolist()
    likely_digits_small_tf.append(top_two_small)
predicted_combinations_small_tf = [''.join(comb) for comb in itertools.product(*likely_digits_small_tf)]
# Display predicted combinations as little green text separated by commas
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
    st.dataframe(df_matching_small_tf)
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
