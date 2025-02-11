from pypdf import PdfReader

import re
import csv
#works for akshaya ,win-win,karunya , karunya-plus

for i in range(250,454 ):
    try:
        reader = PdfReader(f"Pdfs/StreeS/SS-{i}.pdf")
    except FileNotFoundError:
        print(f"FIle not FOund")

    pdf_info=""
    for i in range(reader.get_num_pages()):
        page=reader.pages[i]
        pdf_info+=page.extract_text()
    reader.close()
    pattern = r"Page\s*\d+.*?Department of State Lotteries\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2}"
    pattern2=r"Page\s*\d+IT Support : NIC Kerala\d{2}/\d{2}/\d{4}"
    p3=r"Page\s*\d+IT Support : NIC Kerala\d{2}/\d{2}/\d{4}"
    p4=r"\d{2}:\d{2}:\d{2}"

    # Remove the matching part
    cleaned_text = re.sub(pattern, "", pdf_info)
    cleaned_text=re.sub(pattern2,"",cleaned_text)
    cleaned_text=re.sub(p3,"",cleaned_text)
    cleaned_text=re.sub(p4,"",cleaned_text)
    delimiters = ["1st", "Cons","Consolation","2nd","3rd","4th","5th","6th","7th","8th","FOR","The"]

    # Create a regex pattern by joining the delimiters
    pattern = r'\b(' + '|'.join(delimiters) + r')\b'

    # Use re.split() with the constructed pattern
    result = re.split(pattern, cleaned_text)
    ak_pattern = r"[AKFNRSWI]{1,3}-\d+"  # Matches 'AK-' followed by one or more digits
    date_pattern = r"\d{2}/\d{2}/\d{4}"  # Matches dates in DD/MM/YYYY format
    ak=re.search(ak_pattern,result[0]).group()
    date=re.search(date_pattern,result[0]).group()
    list=[]

    for res in result:

        if res[1]=='P':
            list.append(res)
    Final_list=[]
    Final_list.append(list[-1])
    Final_list.append(list[-2])
    Final_list.append(list[-3])
    Final_list.append(list[-4])
    Final_list.append(list[-5])
    Final_list.append(list[-6])
    print(Final_list)
    csv_data = []
    for win in Final_list:
        final_prize_pattern = r"\d{4}"
        prize_pattern = r"Prize[ -]Rs :(\d+)/-"

    # # Extract prize amount
        prize_match = re.search(prize_pattern, win)
        win=re.sub(prize_pattern,"",win)
        prize_amount = prize_match.group(1) if prize_match else "Unknown"
        # Extract ticket numbers and locations
        matches = re.findall(final_prize_pattern, win)
        # Prepare data for CSV
        for ticket in matches:
            csv_data.append([date,ak,prize_amount, ticket])
    csv_file = "StreeS_smallwins.csv"
    with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)
    file.close()
