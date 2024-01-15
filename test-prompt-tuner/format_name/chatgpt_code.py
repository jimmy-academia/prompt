# Input list of names separated by '\n'
name_list = 'Lydia Manikonda\nMichael E. Houle\nMarinka Zitnik\nMario Alfonso Prado Romero\nMarcin Sydow\nMarco Botta\nMarco Luca Sbodio'

# Split the input string into a list of names
names = name_list.split('\n')

# Process each name and format it with tabs
formatted_names = []
for name in names:
    parts = name.split()
    if len(parts) == 2:  # If there are only two parts (first and last name)
        formatted_names.append(f"{parts[0]}\t\t{parts[1]}")
    elif len(parts) == 3:  # If there are three parts (first, middle, and last name)
        formatted_names.append(f"{parts[0]}\t{parts[1]}\t{parts[2]}")

# Rejoin the formatted names with '\n' to recreate the list
formatted_name_list = '\n'.join(formatted_names)

print(formatted_name_list)
