SELECT smiles_table.id, smiles_table.value smiles_string
FROM text_key_values smiles_table
WHERE smiles_table.key == "Smiles";