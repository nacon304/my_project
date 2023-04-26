# # Laptop Tổng hợp
# import json

# with open('outputFull.json', 'r', encoding = 'utf-8') as f:
#     data = json.load(f)

# new_data = []
# cnt = 0
# for item in data:
#     cnt += 1
#     new_item =  {
#                     'Type': 'Laptop', 
#                     'Name': item['Name'],
#                     'Price': item['Price'],
#                     'Imgs': item['Imgs'],
#                     'ProductID': cnt,
#                     'Desc': [
#                         {
#                             'CPU': item['CPU'],
#                             'OCung': item['OCung'],
#                             'RAM': item['RAM'],
#                             'Card': item['Card'],
#                             'ManHinh': item['ManHinh'],
#                             'HDH': item['HDH'],
#                             'KT&KL': item['KT&KL']
#                         }
#                     ]
#                 }
#     new_data.append(new_item)

# with open('LaptopTongHop.json', 'w', encoding = 'utf-8') as f:
#     json.dump(new_data, f, indent = 4, ensure_ascii = False)

# Laptop Cụ thể
import json

with open('outputFull.json', 'r', encoding = 'utf-8') as f:
    data = json.load(f)

new_data = []
cnt = 0
for item in data:
    cnt += 1
    new_item =  {
                    'Url': item['Url'], 
                    'Name': item['Name'],
                    'Price': item['Price'],
                    'Original Price': 0, 
                    'WebsiteID': 3,
                }
    new_data.append(new_item)

with open('LaptopCuThe.json', 'w', encoding = 'utf-8') as f:
    json.dump(new_data, f, indent = 4, ensure_ascii = False)
