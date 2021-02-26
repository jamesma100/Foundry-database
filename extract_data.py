import json
import sqlite3
import pandas as pd

#connection to database
sql_connect = sqlite3.connect('g4mp2-gdb9.db')
cursor = sql_connect.cursor()

#SQL query
#NOTE: remove LIMIT 10 to get all key_value_pairs
query = "SELECT id, key_value_pairs FROM systems LIMIT 10;"
results = cursor.execute(query).fetchall()

#append values in list
df = pd.read_sql_query(query, sql_connect)
results = list()
for value in df['key_value_pairs']:
  results.append(value)

#write values into json
with open('results.json', 'w') as outfile:
  outfile.write("{\n\"key_value_pairs\":[\n")
  for i in range(len(results) - 1):
    outfile.write(results[i])
    outfile.write(",\n")
  outfile.write(results[-1])
  outfile.write("]}")

#open json file
with open('results.json', 'r') as infile:
  data = json.load(infile)

#dictionary for SMILES string
smiles_data = dict()
for i in range(len(data['key_value_pairs'])):
  smiles_data[i] = data['key_value_pairs'][0]['Smiles']

# Initial work to modify the g4mp2_data.json file
# with open('g4mp2_data.json', 'r') as infile:
#   data = infile.read()

# data = data.replace("\n", ",\n")
# with open('g4mp2_data_modified.json', 'w') as outfile:
#   outfile.write("{\n\"data\":[\n")
#   outfile.write(data)
#   outfile.write("]}")

#open json file
with open('g4mp2_data_modified.json', 'r') as infile:
  data = json.load(infile)
  data = data['data']

#dictionary for SMILES string
homo_lumo_data = dict()
for i in range(len(data)):
  homo_lumo_data[i] = dict()
  homo_lumo_data[i]['homo'] = data[i]['homo']
  homo_lumo_data[i]['lumo'] = data[i]['lumo']
  homo_lumo_data[i]['index'] = data[i]['index']

for i in range(10):
  print(homo_lumo_data[i])


sql_connect.close()
