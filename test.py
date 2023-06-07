import requests

# Perform GET request and load response as JSON object
response = requests.get('https://coderbyte.com/api/challenges/json/age-counting')
data = response.json()['data']

# Split string into list of items
items = data.split(', ')

ckeys = [item.split('=')[1] for item in items if item.startswith('key=')]
ages = [int(item.split('=')[1]) for item in items if item.startswith('age=')]
   
count = 0     
for x in ages:
    if x>=50:
        count += 1
        
print(count)