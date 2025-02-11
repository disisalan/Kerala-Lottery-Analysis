import os
import requests
# Define the base URL and parameters
base_url = "https://result.keralalotteries.com/viewlotisresult.php?drawserial="
number_list=['74804', '74797', '74791', '74784', '74777', '74770', '74763', '74756', '74749', '74742', '74735', '74728', '74721', '74714', '74707', '74700', '74693', '74686', '74680', '74673', '74666', '74660', '74653', '74646', '74639', '74633', '74626', '74619', '74612', '74605', '74598', '74591', '74584', '74577', '74570', '74563', '74556', '74549', '74542', '74535', '74529', '74522', '74515', '74508', '74501', '74494', '74487', '74480', '74473', '74466', '74459', '74452', '74445', '74438', '74432', '74425', '74400', '74393', '74386', '74379', '74372', '74365', '74358', '74351', '74344', '74337', '74330', '74323', '74316', '74309', '74302', '74296', '74289', '74282', '74275', '74262', '74248', '74241', '74234', '74227', '74220', '74213', '74206', '74199', '74192', '74185', '74178', '74171', '74162', '74155', '74148', '74142', '74135', '74128', '74121', '74114', '74107', '74093', '74086', '74079', '74071', '74064', '74057', '74050', '74044', '74037', '74030', '74023', '74016', '74009', '74002', '73995', '73988', '73981', '73974', '73967', '73960', '73953', '73946', '73939', '73932', '73925', '73919', '73912', '73906', '73899', '73892', '73885', '73879', '73872', '73865', '73858', '73850', '73843', '73836', '73829', '73822', '73815', '73808', '73799', '73792', '73784', '73778', '73772', '73760', '73752', '73745', '73750', '73080', '73073', '73067', '73054', '73048', '73042', '73036', '73030', '73025', '73019', '73013', '73007', '73001', '72995', '72989', '72983', '72977', '72901', '72894', '72888', '72777', '72673', '72671', '72649', '72643', '72637', '72632', '72625', '72619', '72599', '72594', '72568', '72563', '72558', '72544', '72498', '72492', '72485', '72440', '72199', '72193', '72187', '72181', '72134', '72123', '72118', '72112', '72106', '72101', '72096', '72084', '72076', '72039', '72031', '72026', '72021']
name_start = 453

# Directory to save PDFs
save_dir = "/Users/alanksijo/Desktop/Projects/a/Pdfs/StreeS"
os.makedirs(save_dir, exist_ok=True)

# Function to download a PDF
def download_pdf(serial_number, file_name):
    url = f"{base_url}{serial_number}"
    print(f"Downloading: {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Save the PDF
        file_path = os.path.join(save_dir, file_name)
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"Saved to: {file_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")

# Loop to download PDFs
current_serial = number_list[0]
current_name_number = name_start

for number in number_list:
    file_name = f"SS-{current_name_number}.pdf"
    download_pdf(number, file_name)
    current_name_number -= 1
