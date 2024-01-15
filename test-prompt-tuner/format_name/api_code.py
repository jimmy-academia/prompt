names = '''Lydia Manikonda
Michael E. Houle
Marinka Zitnik
Mario Alfonso Prado Romero
Marcin Sydow
Marco Botta
Marco Luca Sbodio'''

names_list = names.split('\n')

for name in names_list:
    name_parts = name.split(' ')
    if len(name_parts) == 2:
        print(name_parts[0] + '\t\t' + name_parts[1])
    else:
        print(name_parts[0] + '\t\t' + name_parts[1] + '\t' + name_parts[2])