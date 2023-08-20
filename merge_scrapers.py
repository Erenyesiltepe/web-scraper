function_name = "scrape"  # Add more function names if needed
dict_list = []

for file_name in ["file1", "file2", "file3"]:  # Add more file names as needed
    module = __import__("scrapers_py"+file_name)
    func = getattr(module, function_name)
    dict_list.append(func())

merged_dict = {}
for dictionary in dict_list:
    merged_dict.update(dictionary)
