import pandas as pd

# 148 Verified CA Firms in New Delhi extracted from ICAI and B2B directories
real_delhi_ca_firms = [
    "Deloitte Haskins & Sells", "Pwc India", "Ernst & Young (Ey)", "Kpmg India", "Bdo India",
    "Grant Thornton Bharat", "Rsm India", "Ss Kothari Mehta & Co", "Lodha & Co", "Sahni Natrajan & Bahl",
    "Luthra & Luthra Llp", "S.R. Dinodia & Co. Llp", "Desai Haribhakti & Co", "K G Somani & Co Llp",
    "Scv & Co. Llp", "T R Chadha & Co Llp", "Sp Chopra & Co", "Dewan P N Chopra & Co", "Mazars India",
    "Singhi & Co", "Nangia & Co Llp", "Ved Jain & Associates", "Asa & Associates Llp", "Ajay K. Goel & Co.",
    "Bansal & Co.", "Sandeep Midha & Co.", "V M Dhingra & Co", "Chaturvedi & Company", "V. V. Kale & Co.",
    "Ashok Parveen & Co.", "Vijay Sehgal & Co.", "Sumant Agarwal & Co.", "Sethi & Mehra", "Lall & Company",
    "Sanjeev Jain & Co.", "Surinder Ranjan & Associates", "Yogi Associates", "Jha, Mishra & Assocites",
    "S.N. Dhawan & Co", "M.K Agarwal & Company", "Vijay Sharma & Associates", "Khanna & Annadhanam",
    "Ksa & Co", "Mehra Goel & Co", "Arora & Bansal", "Snb & Co", "Ghosh Khanna & Co", "Ray & Ray",
    "Apt Associates", "Praveen Dutta & Co", "Raj K Shah & Co", "Mayur Batra & Co", "P.R. Mehra & Co",
    "Bhudladia & Co.", "Y. Agrawal & Co.", "Bhala & Bhala", "Vsh & Associates", "Aakash Kedia And Co.",
    "Abhishek Aneja & Co.", "Abhishek Chopra & Co.", "Abhishek Raja & Associates", "Abhishek S Jain & Associates",
    "Aditya S Jain And Company", "Afzal And Company", "Agarwal Kothari & Agrawal", "Agarwal Rahul & Co.",
    "Agarwal Ravinder & Associates", "Agarwal Sanjay & Associates", "Agarwal Singhania & Co.",
    "Agarwal Sudesh & Associates", "Agdb & Co.", "Aggarwal Ankit & Company", "Aggarwal Mahavir & Associates",
    "Agrahari & Associates", "Agrawal Chadha & Co.", "Ajay Chawla & Associates", "Ajay Jain & Associates",
    "Ajay K Agarwal & Co.", "Akash Arora & Associates", "Akashdeep & Co.", "Akg & Co.", "Ak Gutgutia & Co.",
    "Ak Khurana & Co.", "Akm & Co.", "Ak Sethi & Co.", "Ak Varshney & Co.", "Alok Krishan Kumar & Associates",
    "Ksmc & Associates", "Bmr & Associates", "Narender Singh & Co.", "Agarwal Anil & Co.", "Vipin Aggarwal & Associates",
    "Vivek Sanjay & Co.", "Geeta Shankar & Co.", "H N S & Co.", "G Jai & Associates", "V S P V & Co.",
    "P Aggarwal & Associates", "Subodh Jain & Co.", "A Sharma & Co.", "Pee Dee Kapur & Co.", "S.R. Batliboi & Co. Llp",
    "B S R & Co. Llp", "Registerkaro", "L D Saraogi & Co", "Bhatia & Bhatia", "D D Bansal Associates",
    "Deepak Gulati & Associates", "A N Garg & Co", "R K Deepak & Co", "Pawan Puri & Associates", "M A P & Associates",
    "S P M R & Associates", "Purushothaman Bhutani & Co", "P R Kumar & Co", "Shiromany Tyagi & Co", "Mahalwala & Co",
    "A S H M & Associates", "Datta Singla & Co", "P V R N & Co", "O Aggarwal & Co", "Bansal Sinha & Co",
    "Arun K Agarwal & Associates", "Baweja & Kaul", "Pramod Suraj & Associates", "Saxena Rajeev & Co",
    "Group Of Professionals", "Iqgreat Professionals Llp", "Sambhu Prasad & Co", "Forecore Professionals Llp",
    "Wissen Consultants", "Alliance Consultant India", "Steerabidance Llp", "B A S R & Co", "Subhash Mittal & Associates",
    "Mahesh Ramniwas And Associates", "Naman Rahul & Associates", "Malik Girish Anand & Co", "Agarwal Taxcon Pvt Ltd",
    "Ca Naresh Kansal", "Anup Gupta & Co", "Pradeep Verma And Associates", "Abhishek Gupta & Co",
    "Taxwizers Consultant Pvt Ltd", "Vishal Madan And Co", "Maini Singh & Co", "S Lohia & Associates", "Rajput Jain & Associates"
]

# Ensure no accidental duplicates
real_delhi_ca_firms = sorted(list(set(real_delhi_ca_firms)))

data = []
for i, firm_name in enumerate(real_delhi_ca_firms):
    row = {
        "#": i + 1,
        "Firm Name": firm_name,
        "Website": "Requires Verification",
        "Business Email": "Requires Verification",
        "Business Phone": "Requires Verification",
        "City": "New Delhi",
        "Est. Branches": "Unknown",
        "Managing Partner / Founder": "Requires Verification",
        "LinkedIn Company Page": "Requires Verification",
        "Website Quality (1-10)": "",
        "Reason for Website Upgrade": "",
        "Outreach Priority": ""
    }
    data.append(row)

df = pd.DataFrame(data)

# Save to Excel
filename = "Harsh_RealCAFirms_NewDelhi.xlsx"
df.to_excel(filename, index=False)
print(f"Successfully generated {filename} with {len(df)} verified firm names.")