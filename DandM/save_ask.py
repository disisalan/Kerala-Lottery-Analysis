import re
import csv

# Input text
text = """
 Prize Rs :7000000/- 1) AW 228007 (PALAKKAD)\n
"""

# Updated regex pattern
# Matches the optional index (e.g., "1)") followed by ticket and location


pattern = r"(?:\d+\)\s*)?(\w{2} \d{6})\s{1,2}\(([\w\s]+)\)"
prize_pattern = r"Prize[ -]Rs :(\d+)/-"

# Extract prize amount
prize_match = re.search(prize_pattern, text)
prize_amount = prize_match.group(1) if prize_match else "Unknown"
print(prize_amount)

# Extract ticket numbers and locations
matches = re.findall(pattern, text)
print(matches)
# Prepare data for CSV
csv_data = [["Prize Amount", "Ticket Number", "Location"]]
for ticket, location in matches:
    csv_data.append([prize_amount, ticket, location])

# # Write data to CSV
# csv_file = "lottery_results.csv"
# with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
#     writer = csv.writer(file)
#     writer.writerows(csv_data)

# print(f"Data has been written to {csv_file}")
