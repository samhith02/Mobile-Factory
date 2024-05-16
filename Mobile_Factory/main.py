import os
import json

def csv_to_map(filename):
  data_map = {}
  with open(filename, 'r') as csvfile:
    reader = csvfile.readlines()
    for line in reader:
      a = line.split(',')
      data_map[a[0]] = {'Price': a[1], 'Part': a[2][:-1]}
  return data_map


processed_data = csv_to_map('initial_data.csv')
# types = {
#   'screen': ['A', 'B', 'C'],
#   'camera': ['D', 'E'],
#   'port': ['F', 'G', 'H'],
#   'os': ['I', 'J'],
#   'body': ['K', 'L']
# }

types = [
  ['A', 'B', 'C'],
  ['D', 'E'],
  ['F', 'G', 'H'],
  ['I', 'J'],
  ['K', 'L'],
]


def noDupes(components):
  components.sort()
  for i in range(len(components)):
    if (components[i] in types[i]):
      continue
    else:
      return False
  return True

def processedObject(data, ORDER_ID):
  if len(data['components']) == 5 and noDupes(data['components']):
    total = 0
    for comp in data['components']:
      total += float(processed_data[comp]['Price'])
    return {
      'order_id': ORDER_ID,
      'total': total,
      'parts': [processed_data[comp]['Part'] for comp in data['components']]
    }

def httpPostRequest(data, endpoint):
    file_path = f'./api_endpoint{endpoint}.json'

    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                # empty or invalid JSON
                existing_data = []
    else:
        # file does not exist
        existing_data = []
    
    if len(existing_data) == 0:
      ORDER_ID = 1
    else:
      ORDER_ID = existing_data[-1]['order_id'] + 1

    obj = processedObject(data, ORDER_ID)
    existing_data.append(obj)

    print("Updated data:", existing_data)

    with open(file_path, 'w') as f:
        json.dump(existing_data, f, indent=4)

    print("201\n", obj)


#HTTP POST /order { "components": ['I', 'A', 'D', 'F', 'K'] }
inp = input()
commands = inp.split(' ')
components = []
for x in commands[5:]:
  if len(x) > 2:
    components += x[-3]

if commands[1] == 'POST':
  httpPostRequest({
    'components': components
  }, commands[2])
elif commands[1] == 'GET':
  print('GET')
