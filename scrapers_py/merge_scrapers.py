# import importlib

# function_name = "scrape"  # Add more function names if needed
# event_list = []

# for file_name in ["ankara.py", "cankaya.py", "odtü.py","hacettepe.py"]:  # Add more file names as needed
#     #module = __import__(file_name,)
#     print(file_name)
#     module = importlib.import_module(file_name)
#     func = getattr(module, function_name)
#     event_list.append(func())

# merged_list = []
# for event in event_list:
#     merged_list.extend(event)

# for event in merged_list:
#     print(event)
import scrapers_py.ankara as a
import scrapers_py.cankaya as ca
import scrapers_py.hacettepe as ht
import scrapers_py.odtü as od

merged_list=[]
merged_list.extend(a.scrape())
merged_list.extend(ca.scrape())
merged_list.extend(ht.scrape())
merged_list.extend(od.scrape())

for a in merged_list:
    print(a)