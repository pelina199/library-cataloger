import pandas as pd


print("LIBRARY CATALOGER")
actions = ['New entry', 'Display the catalog', 'Search the catalog', 'Delete entry']
running = True


def choose_action():
    global running
    print('\n-----------------------------------------------------------------------------------------------')
    i = 1
    for item in actions:
        print(str(i) + '.', item)
        i += 1
    action_index = input('   Choose action number or type "quit" to exit: ')

    if action_index == 'quit':
        running = False
    elif action_index.isnumeric() and 0 < int(action_index) <= len(actions):
        return int(action_index) - 1
    else:
        return choose_action()


# put df in alphabetical order with indices starting from 1
def sort_df(df, column):
    new_df = df.sort_values(by=column)
    new_idx = [i for i in range(1, len(df.index)+1)]
    new_df.index = new_idx
    return new_df


def delete_entry(df):
    del_choice = input("   Choose entry index to delete or press enter to go back to the menu: ")

    if del_choice.isnumeric() and 0 < int(del_choice) <= len(df.index):
        new_df = df.drop([df.index[int(del_choice) - 1]])
        print("   Deleted entry:")
        print(df.iloc[[int(del_choice) - 1]])
        return new_df
    elif del_choice == '':
        return None
    else:
        print("   No entries found")
        return delete_entry(df)


def capital(phrase):
    return ' '.join(word.capitalize() for word in phrase.split())


while running:

    df1 = pd.read_csv('Collection.csv')
    choice = choose_action()

    # Add entry
    if choice == 0:
        print("\n   New Entry")

        title = capital(input("Title: "))
        author = capital(input("Author: "))
        genre = capital(input("Genre: "))
        publisher = capital(input("Publisher: "))
        year = input("   Publishing year: ")

        new_entry = {'Title': [title], 'Author': [author], 'Genre': [genre], 'Publisher': [publisher], 'Year': [year]}

        entry_df = pd.DataFrame(new_entry)
        entry_df.to_csv('Collection.csv', index=False, mode='a', header=False)
        print('\n' + title + ' by ' + author + ' has been added to the catalog.')

    # Display all the entries
    elif choice == 1:
        print('\n', sort_df(df1, 'Title').to_string())

    # Find entries
    elif choice == 2:
        print('\n   Fill in search fields:')
        search_values = {'Title': '', 'Author': '', 'Genre': '', 'Publisher': '', 'Year': ''}
        fields = 0
        for label in search_values:
            search_values[label] = capital(input(label + ': '))
            if search_values[label] != '':
                fields += 1

        found_all = pd.DataFrame()
        for label, value in search_values.items():
            found_df = df1[df1[label].isin([value])]
            found_all = pd.concat([found_df, found_all])

        grp_df = found_all.groupby(list(found_all.columns))
        if fields > 1:
            result_idx = [idx[0] for idx in grp_df.groups.values() if len(idx) != 1]
        else:
            result_idx = [idx[0] for idx in grp_df.groups.values() if len(idx) == 1]

        if not result_idx:
            print("\n   No results found")
        else:
            print(df1.loc[result_idx])

    # Delete entry
    elif choice == 3:
        sorted_df = sort_df(df1, 'Title')
        print('\n', sorted_df.to_string())
        deleted_df = delete_entry(sorted_df)
        if deleted_df is not None:
            deleted_df.to_csv('Collection.csv', index=False)
        else:
            continue


