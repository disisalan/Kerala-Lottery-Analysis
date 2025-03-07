import streamlit as st
import pandas as pd 
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go



st.title("Number Frequency and Patterns")

st.markdown("""

 In this section, we dive into the fascinating world of lottery number patterns. We focus on three key columns from our dataset:

- **Series:** The lottery series identifier (e.g., "AB"), which helps differentiate various lottery schemes.
- **SN:** The complete winning entry (e.g., "AB 123456"), combining the series with the winning number.
- **Numbers:** The 7-digit number part (e.g., "123456"), which we analyze to uncover hidden trends.

By examining these columns, we explore frequency distributions, recurring patterns, and anomalies in the lottery results to provide deeper insights into how these numbers behave over time.
""", unsafe_allow_html=True)

st.write("## 1. Most Common Numbers")
st.markdown("""
Identify the most frequently drawn 7-digit numbers by analyzing **all rows** from the `Number` column in the dataset.
""")
st.markdown(
    '<div style="background-color:#c9fac5; padding:10px; border-radius:5px;">'
    '<strong>Insight:</strong> Even though the frequency of the most repeated number is 3, it is astonishing that even the big wins can have repeated numbers.'
    '</div>', unsafe_allow_html=True)
st.write("#### For Big Wins ")

df_big = pd.read_csv("Assets/Csvfiles/BigWins_final.csv")
# Ensure the winning number is a 7-digit string by zero-padding the 'Number' column if necessary.


df_big["winning_number"] = df_big["Number"].apply(lambda x: str(x).zfill(7))

# Group by winning number to calculate frequency and list the amounts won for each occurrence
common_numbers = df_big.groupby("winning_number").agg(
    Frequency=('winning_number', 'count'),
    Amounts=('Amount', lambda x: list(x))
).reset_index()

# Rename the column for clarity and sort in descending order by frequency
common_numbers = common_numbers.rename(columns={'winning_number': 'Winning Number'})
common_numbers = common_numbers.sort_values("Frequency", ascending=False)

# Display the table
st.write("**Top 10 Most Common 7-Digit Numbers with Amounts:**")
st.dataframe(common_numbers.head(10))


df_small = pd.read_csv("Assets/Csvfiles/SmallWins.csv")
st.write("#### For Small Wins")
st.markdown("""
Identify the most frequently drawn 4-digit numbers by analyzing **all rows** from the `Number` column in the dataset.
""")
st.markdown(
    '<div style="background-color:#c9fac5; padding:10px; border-radius:5px;">'
    '<strong>Insight:</strong> Clearly some numbers are more frequent than other but the difference is small and irrelevant to the position of digits.'
    '</div>', unsafe_allow_html=True)
# Ensure the winning number is a 4-digit string by zero-padding the 'Number' column if necessary.
# Ensure the winning number is a 4-digit string
df_small["winning_number"] = df_small["Number"].apply(lambda x: str(x).zfill(4))

# Calculate the frequency and total amount won for each winning number
winning_stats_small = df_small.groupby("winning_number").agg(
    Frequency=("winning_number", "count"),
    Total_Amount=("Amount", "sum")
).reset_index().rename(columns={"winning_number": "Winning Number"})

# Sort by frequency in descending order and select the top 15
top15_numbers = winning_stats_small.sort_values("Frequency", ascending=False).head(15)

# Display the top 15 winning numbers with total amount won
st.write("**Top 15 Winning Numbers with Total Amount Won:**")
st.dataframe(top15_numbers,width=500)

# Calculate the frequency of each winning number (for top 50 split)
common_numbers_small = df_small["winning_number"].value_counts().reset_index()
common_numbers_small.columns = ["Winning Number", "Frequency"]

# Split the top 50 numbers into two tables (25 each)
common_numbers_small_top50 = common_numbers_small.head(50)
left_table = common_numbers_small_top50.head(25)
right_table = common_numbers_small_top50.iloc[25:50]

# Display tables side by side
col3, col4 = st.columns(2)
with col3:
    st.write("**Top 25 of Top 50 4-Digit Numbers:**")
    st.dataframe(left_table, width=500)
with col4:
    st.write("**Bottom 25 of Top 50 4-Digit Numbers:**")
    st.dataframe(right_table, width=500)

# Calculate totals for pie chart: total frequency for top 50 numbers and for all numbers
top50_total = common_numbers_small_top50["Frequency"].sum()
all_total = common_numbers_small["Frequency"].sum()
others_total = all_total - top50_total

# Create a DataFrame for the pie chart data
pie_data = pd.DataFrame({
    "Category": ["Top 50 Winning Numbers", "Others"],
    "Frequency": [top50_total, others_total]
})

# Use Plotly to create an interactive pie chart
import plotly.express as px
fig = px.pie(
    pie_data,
    names="Category",
    values="Frequency",
    title="Percentage of Top 50 Winning Numbers vs. Others",
    color_discrete_sequence=["skyblue", "lightgrey"],
    hole=0.3  # optional: creates a donut chart effect
)
st.plotly_chart(fig)
st.markdown(
    '<div style="background-color:#c9fac5; padding:10px; border-radius:5px;">'
    '<strong>Insight:</strong> Even the top 50 repeated numbers for the small win make up only very insignificant part of the all winning numbers giving them no real edge. '
    '</div>', unsafe_allow_html=True)

# st.plotly_chart(fig_small)

##################################################################################################

st.write("## 2. Most Common Lottery Series")
st.markdown("""
Analyze which lottery series (e.g., AA, AB, etc.) appear most frequently in the **Big Wins** dataset. This uses the `Series` column.
""")
st.markdown(
    '<div style="background-color:#c9fac5; padding:10px; border-radius:5px;">'
    '<strong>Insight:</strong> There is no clear series that wins more than the other buy a great margin but the top two winning serial belong to the Nirmal Lottery.'
    '</div>', unsafe_allow_html=True)

# Calculate the frequency of each serial
common_serial = df_big["Serial"].value_counts().reset_index()
common_serial.columns = ["Serial", "Frequency"]

# Split the top 50 serials into two tables (25 each)
top50_serial = common_serial.head(50)
left_table = top50_serial.head(25)
right_table = top50_serial.iloc[25:50]

# Display the two tables side by side using columns
col1, col2 = st.columns(2)
with col1:
    st.write("**Top 25 of Top 50 Most Common Serials:**")
    st.dataframe(left_table, width=500)
with col2:
    st.write("**Bottom 25 of Top 50 Most Common Serials:**")
    st.dataframe(right_table, width=500)

# Interactive Plotly bar chart for the top 10 most common serials
top10_serial = common_serial.head(10)
fig_serial = px.bar(
    top10_serial, 
    x="Serial", 
    y="Frequency", 
    title="Top 10 Most Common Lottery Serials",
    labels={"Serial": "Lottery Serial", "Frequency": "Frequency"},
    text="Frequency",
    color="Frequency",
    color_continuous_scale="Blues"
)

fig_serial.update_layout(xaxis_tickangle=-45)  # Rotate x-axis labels
st.plotly_chart(fig_serial)


##################################################################################################








st.write("## 3. Least Common and Never Drawn Numbers")
st.markdown("""
Determine which 7-digit and 4-digit numbers have been drawn the least or have never been drawn by performing a frequency count on the **Number** column.
""")
st.markdown(
    '<div style="background-color:#c9fac5; padding:10px; border-radius:5px;">'
    '<strong>Insight:</strong> It was found that in small wins there is no number that has never been drawn indicating a fair chance to each number.<br> For big wins considering the sample space for a six digit number is very big it was irrelevant to find undrawn numbers.'
    '</div>', unsafe_allow_html=True)


##################################################################################################

st.write("## 4.Repeating Digit Analysis")
st.markdown("""
Investigate if numbers with repeating digits (e.g., 1111111, 2223222) are less common. This analysis filters the `Number` column for patterns with repeating digits.
""")


def max_digit_repeat(num_str):
    """Finds the maximum number of times any digit is repeated in a number."""
    return max([num_str.count(d) for d in set(num_str)])

# ✅ Apply the function to identify repeating numbers for Big Wins
df_big["max_repeat"] = df_big["winning_number"].astype(str).apply(max_digit_repeat)
df_big["is_repeating"] = df_big["max_repeat"] > 1

# ✅ Compute counts
big_repeating_count = df_big["is_repeating"].sum()
big_non_repeating_count = len(df_big) - big_repeating_count

# ✅ Interactive Pie Chart for Big Wins
fig_big_pie = px.pie(
    names=["Repeating", "Non-Repeating"],
    values=[big_repeating_count, big_non_repeating_count],
    title="Big Wins: Repeating vs Non-Repeating",
    color_discrete_sequence=['#ff9999', '#66b3ff']
)
st.plotly_chart(fig_big_pie)
st.markdown(
    '<div style="background-color:#c9fac5; padding:10px; border-radius:5px;">'
    '<strong>Insight:</strong> For big wins the ratio of repeating and non repeating numbers might look concering having an imbalance but this is easily justifiable looking at the much less number of draws compared to small wins.'
    '</div>', unsafe_allow_html=True)
# ✅ Breakdown of repeating digits in Big Wins
big_repeat_groups = (
    df_big[df_big["is_repeating"]]
    .groupby("max_repeat")
    .agg(Count=('max_repeat', 'count'),
         Highest_Amount=('Amount', 'max'))
    .reset_index()
    .sort_values("max_repeat")
)
big_repeat_groups["Proportion (%)"] = (big_repeat_groups["Count"] / big_repeating_count) * 100

st.write("**Big Wins: Repeating Digits Breakdown**")
st.dataframe(big_repeat_groups)

# ✅ Display Top 10 Winning Numbers for max_repeat values 4, 5, and 6
big_group = df_big.groupby("winning_number").agg(
    Frequency=('winning_number', 'count'),
    Highest_Amount=('Amount', 'max'),
    max_repeat=('max_repeat', 'first')
).reset_index()

col1, col2 = st.columns(2)
with col1:
    st.write("**Top 10 Winning Numbers with 4 Repeating Digits:**")
    st.dataframe(big_group[big_group["max_repeat"] == 4].nlargest(10, "Highest_Amount"))

with col2:
    st.write("**Top 10 Winning Numbers with 5 Repeating Digits:**")
    st.dataframe(big_group[big_group["max_repeat"] == 5].nlargest(10, "Highest_Amount"))
st.markdown(
    '<div style="background-color:#c9fac5; padding:10px; border-radius:5px;">'
    '<strong>Insight:</strong> It is intresting to see that many of the big wins has 4 ,5 repeating digits but not six which clearly aligns with the mathematical probablity of getting 6 repeating digits.  '
    '</div>', unsafe_allow_html=True)

# -----------------------------------------------
# ✅ Small Wins Analysis
# -----------------------------------------------
df_small["max_repeat"] = df_small["winning_number"].astype(str).apply(max_digit_repeat)
df_small["is_repeating"] = df_small["max_repeat"] > 1

# ✅ Compute counts
small_repeating_count = df_small["is_repeating"].sum()
small_non_repeating_count = len(df_small) - small_repeating_count

# ✅ Interactive Pie Chart for Small Wins
fig_small_pie = px.pie(
    names=["Repeating", "Non-Repeating"],
    values=[small_repeating_count, small_non_repeating_count],
    title="Small Wins: Repeating vs Non-Repeating",
    color_discrete_sequence=['#ff9999', '#66b3ff']
)
st.plotly_chart(fig_small_pie)



# ✅ Breakdown of repeating digits in Small Wins
small_repeat_groups = (
    df_small[df_small["is_repeating"]]
    .groupby("max_repeat")
    .agg(Count=('max_repeat', 'count'),
         Highest_Amount=('Amount', 'max'))
    .reset_index()
    .sort_values("max_repeat")
)
small_repeat_groups["Proportion (%)"] = (small_repeat_groups["Count"] / small_repeating_count) * 100

st.write("**Small Wins: Repeating Digits Breakdown**")
st.dataframe(small_repeat_groups)
st.markdown(
    '<div style="background-color:#c9fac5; padding:10px; border-radius:5px;">'
    '<strong>Insight:</strong> As noted before there is not a significant difference between repeating and non repeating digits in the small wins considering the range is much smaller compared to big wins. But the data does indicate that non repeating numbers do have a slight edge over repeating numbers.'
    '</div>', unsafe_allow_html=True)

##################################################################################################


st.markdown("## 5.Digit Position Analysis")
st.markdown("""
Examine the frequency of individual digits at each position in the 7-digit number. This analysis inspects each digit position separately using the **Number** column.
""")
st.markdown(
    '<div style="background-color:#c9fac5; padding:10px; border-radius:5px;">'
    '<strong>Insight:</strong> The digit position frequency is also quite normal with only minor deviations for some places but when matched with the data these deviation do not give a solid edge to those repeating digits.(Mentioned below)'
    '</div>', unsafe_allow_html=True)

### Big Wins Analysis
df_big["winning_number"] = df_big["Number"].astype(str).str.zfill(6)
# Create a dictionary to store digit frequencies at each position
digit_counts = {
    pos: df_big["winning_number"].str[pos]
         .value_counts()
         .reindex([str(i) for i in range(10)], fill_value=0)
    for pos in range(6)
}
# Convert to DataFrame
digit_counts_df = pd.DataFrame(digit_counts).T

st.subheader("Digit Frequency at Each Position (Big Wins)")
# Create 2 rows of 3 columns each using st.columns
cols_row1 = st.columns(3)
cols_row2 = st.columns(3)

for pos in range(6):
    fig = px.bar(
        x=[int(d) for d in digit_counts_df.columns],
        y=digit_counts_df.iloc[pos],
        labels={'x': 'Digit (0-9)', 'y': 'Count'},
        title=f"Position {pos + 1}",
        color_discrete_sequence=['skyblue']
    )
    # Display in first row for positions 0-2, and in second row for positions 3-5
    if pos < 3:
        cols_row1[pos].plotly_chart(fig, use_container_width=True)
    else:
        cols_row2[pos - 3].plotly_chart(fig, use_container_width=True)

# Find the most common digit at each position for Big Wins
most_common_digits = digit_counts_df.idxmax(axis=1).to_dict()
st.write("Most likely digit at each position (Big Wins):", most_common_digits)

### Small Wins Analysis
df_small["winning_number"] = df_small["Number"].astype(str).str.zfill(4)
# Create a dictionary to store digit frequencies at each position for Small Wins
digit_counts_small = {
    pos: df_small["winning_number"].str[pos]
         .value_counts()
         .reindex([str(i) for i in range(10)], fill_value=0)
    for pos in range(4)
}
# Convert to DataFrame
digit_counts_small_df = pd.DataFrame(digit_counts_small).T

st.subheader("Digit Frequency at Each Position (Small Wins)")
st.markdown("""
Examine the frequency of individual digits at each position in the 4-digit number. This analysis inspects each digit position separately using the **Number** column.
""")
st.markdown(
    '<div style="background-color:#c9fac5; padding:10px; border-radius:5px;">'
    '<strong>Insight:</strong> Coming to small wins the distribution is much more stable and noraml. Doesn\'t indicate a clear advatange to any number at any position. Even though the number 7029 seems favourable it was not even in the top 50 drawn numbers.'
    '</div>', unsafe_allow_html=True)

cols_small = st.columns(4)
for pos in range(4):
    fig = px.bar(
        x=[int(d) for d in digit_counts_small_df.columns],
        y=digit_counts_small_df.iloc[pos],
        labels={'x': 'Digit (0-9)', 'y': 'Count'},
        title=f"Position {pos + 1}",
        color_discrete_sequence=['lightcoral']
    )
    cols_small[pos].plotly_chart(fig, use_container_width=True)

# Find the most common digit at each position for Small Wins
most_common_digits_small = digit_counts_small_df.idxmax(axis=1).to_dict()
st.write("Most likely digit at each position (Small Wins):", most_common_digits_small)

# Construct the most likely numbers
most_likely_big = "".join(most_common_digits.values())
most_likely_small = "".join(most_common_digits_small.values())

# Filter Big Wins for the most likely number
big_wins_filtered = df_big[df_big["winning_number"] == most_likely_big]

# Filter Small Wins for the most likely number
small_wins_filtered = df_small[df_small["winning_number"] == most_likely_small]

# Display results for Big Wins
st.write("### Most Likely Winning Number in Big Wins")
if not big_wins_filtered.empty:
    st.write(f"The most likely winning number `{most_likely_big}` won `{len(big_wins_filtered)}` times.")
    st.dataframe(big_wins_filtered[["Date", "Amount", "winning_number"]])
else:
    st.write(f"The number `{most_likely_big}` has never won.")

# Display results for Small Wins
st.write("### Most Likely Winning Number in Small Wins")
if not small_wins_filtered.empty:
    st.write(f"The most likely winning number `{most_likely_small}` won `{len(small_wins_filtered)}` times.")
    st.dataframe(small_wins_filtered[["Date", "Amount", "winning_number"]])
else:
    st.write(f"The number `{most_likely_small}` has never won.")
##################################################################################################

st.markdown("### 6. Number Clustering")
st.markdown("""
Check if winning numbers are grouped within specific ranges (e.g., 1000000-2000000 vs. 8000000-9000000) by analyzing the entire range of the **Number** column.
""")
st.markdown(
    '<div style="background-color:#c9fac5; padding:10px; border-radius:5px;">'
    '<strong>Insight:</strong> The range distribution of big wins and small wins do not indicate a significant range that is more probable.'
    '</div>', unsafe_allow_html=True)
df_big["Date"] = pd.to_datetime(df_big["Date"], format="%d/%m/%Y")

# Convert the "Number" column to integers
df_big["winning_number"] = df_big["Number"].astype(int)

# Define bin edges for Big Wins: from 0 to 999999 in steps of 100000
bins_big = dict(start=0, end=1000000, size=100000)

# Define year groups
year_groups = {
    "2020-2021": [2020, 2021],
    "2022": [2022],
    "2023": [2023],
    "2024-2025": [2024, 2025]
}

# Create 2x2 subplot layout for Big Wins
fig_big = make_subplots(rows=2, cols=2, subplot_titles=list(year_groups.keys()))

row = 1
col = 1
for group_name, years in year_groups.items():
    # Filter dataset for the given years
    df_filtered = df_big[df_big["Date"].dt.year.isin(years)]
    
    # Create histogram trace
    hist = go.Histogram(
        x=df_filtered["winning_number"],
        xbins=bins_big,
        marker_color="blue",
        opacity=0.7,
        name=group_name
    )
    fig_big.add_trace(hist, row=row, col=col)
    fig_big.update_xaxes(title_text="Winning Number Ranges", row=row, col=col)
    fig_big.update_yaxes(title_text="Total Wins in Range", row=row, col=col)
    
    # Move to next subplot
    if col == 2:
        row += 1
        col = 1
    else:
        col += 1

fig_big.update_layout(
    title_text="Distribution of Big Wins by Number Range (Split by Year)",
    showlegend=False,
    height=600,
    width=800,
    bargap=0.2,
    template="plotly_white"
)

st.plotly_chart(fig_big)

# ---------------------------
# Small Wins Histogram
# ---------------------------
# Convert the "Date" column to datetime format (assuming format is "DD/MM/YYYY")
df_small["Date"] = pd.to_datetime(df_small["Date"], format="%d/%m/%Y")

# Convert the "Number" column to integers
df_small["winning_number"] = df_small["Number"].astype(int)

# Define bin edges for Small Wins: from 0 to 9999 in steps of 1000
bins_small = dict(start=0, end=10000, size=1000)

# Create 2x2 subplot layout for Small Wins
fig_small = make_subplots(rows=2, cols=2, subplot_titles=list(year_groups.keys()))

row = 1
col = 1
for group_name, years in year_groups.items():
    # Filter dataset for the given years
    df_filtered = df_small[df_small["Date"].dt.year.isin(years)]
    
    # Create histogram trace
    hist = go.Histogram(
        x=df_filtered["winning_number"],
        xbins=bins_small,
        marker_color="red",
        opacity=0.7,
        name=group_name
    )
    fig_small.add_trace(hist, row=row, col=col)
    fig_small.update_xaxes(title_text="Winning Number Ranges", row=row, col=col)
    fig_small.update_yaxes(title_text="Total Wins in Range", row=row, col=col)
    
    # Move to next subplot
    if col == 2:
        row += 1
        col = 1
    else:
        col += 1

fig_small.update_layout(
    title_text="Distribution of Small Wins by Number Range (Split by Year)",
    showlegend=False,
    height=600,
    width=800,
    bargap=0.2,
    template="plotly_white"
)

st.plotly_chart(fig_small)
##################################################################################################
