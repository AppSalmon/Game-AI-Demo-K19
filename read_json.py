import json

# Mở tệp JSON để đọc
with open('data.json', 'r') as file:
	for line in file:
		data = json.loads(line)
		print(data)
		print(data['email'])
