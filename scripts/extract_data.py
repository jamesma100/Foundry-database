import json
import sqlite3
import pandas as pd

"""
Place in same folder:
  g4mp2-gdb9.db from https://petreldata.net/mdf/detail/narayananbadri_g4mp2gdb9_database_v1.1/ with GLobus Connect
  g4mp2_data.json by opening g4mp2_data.json.gz from https://github.com/jamesma100/foundry-database/tree/main/raw or https://github.com/globus-labs/solvation-energy-ml/blob/master/data/output/g4mp2_data.json.gz

"""

#connection to database
# sql_connect = sqlite3.connect('g4mp2-gdb9.db')
# cursor = sql_connect.cursor()
"""
extraction of key_value_pairs from systems table in g4mp2-gdb9.db
puts data into results.json so that it can be parsed as list of dictionaries
"""

#SQL query
#NOTE: remove LIMIT 10 to get all key_value_pairs
# query = "SELECT id, key_value_pairs FROM systems LIMIT 10;"
# results = cursor.execute(query).fetchall()

#append values in list
# df = pd.read_sql_query(query, sql_connect)
# results = list()
# for value in df['key_value_pairs']:
#   results.append(value)

#write values into json
# with open('results.json', 'w') as outfile:
#   outfile.write("{\n\"key_value_pairs\":[\n")
#   for i in range(len(results) - 1):
#     outfile.write(results[i])
#     outfile.write(",\n")
#   outfile.write(results[-1])
#   outfile.write("]}")

#open json file
# with open('results.json', 'r') as infile:
#   data = json.load(infile)

#the list of dictionaries
# full_data = data['key_value_pairs']


"""
Extracts data from g4mp2_data.json as string
Modifies and rewrites data into g4mp2_data_modified.json so that it can be parsed as list of dictionaries
"""
# with open('g4mp2_data.json', 'r') as infile:
#   data = infile.read()

# data = data.replace("\n", ",\n")
# with open('g4mp2_data_modified.json', 'w') as outfile:
#   outfile.write("{\n\"data\":[\n")
#   outfile.write(data)
#   outfile.write("]}")

#open json file
# with open('g4mp2_data_modified.json', 'r') as infile:
#   data = json.load(infile)
#   data = data['data']

#sql_connect.close()


"""
Execute these lines to create and begin insertion of the relevant data into MergedDB database
data has all the SMILES + everything else
homo_lumo has homo + lumo properties + everything else without relevant names for key names
"""
# conn = sqlite3.connect('MergedDB.db')
# c = conn.cursor()


## run this line if the table already exists
# c.execute("DROP TABLE data")
# columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in full_data[0].keys())
# query = "CREATE TABLE data ( %s, PRIMARY KEY (gdbID));" % columns
# c.execute(query)
# for observation in full_data:
#   values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in observation.values())
#   query = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('data', columns, values)
#   c.execute(query)
# conn.commit()

## run this line if the table already exists
# c.execute("DROP TABLE homo_lumo")
# columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in data[0].keys())
# query = "CREATE TABLE homo_lumo ( %s, PRIMARY KEY (`index`), FOREIGN KEY (`index`) REFERENCES data(gdbID));" % columns
# c.execute(query)

# for observation in data:
#   values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in observation.values())
#   query = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('homo_lumo', columns, values)
#   c.execute(query)
# conn.commit()

# conn.close()

"""
An example query in python which merges data and homo_lumo table on primary key gdbID
This gets us the Smiles string, the homo, and the lumo in one dataframe
DataFrame is then pushed to merged_data.csv for storage
"""
conn = sqlite3.connect('MergedDB.db')
c = conn.cursor()

query = "SELECT gdbID, Smiles, homo, lumo FROM data, homo_lumo WHERE data.gdbID = homo_lumo.`index` ORDER BY gdbID"
df = pd.read_sql_query(query, conn)
df.to_csv ('./merged_data.csv', index = False, header=True)


conn.close()