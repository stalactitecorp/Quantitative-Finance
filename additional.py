import sys
from format_list import format_list
from contact import parse_file
from contact import find_potential_zombies
from contact import file_exists




def zombie_spreader(contacts_dic):

    """Return the zombies that have only come into contact
    with potential zombies.

    Args:
        contacts_dic (dic): each entry is a sick person's name and their list
        of contacts.

    Returns:
        list: contains the names zombie spreaders.
    """
    values = list(contacts_dic.values())
    keys = list(contacts_dic.keys())
    zombie_spreader_list = []
    for i in range(len(contacts_dic)):
        if set(values[i]).issubset(set(list(find_potential_zombies(contacts_dic)))):
            zombie_spreader_list.append(keys[i])
    return sorted(zombie_spreader_list)

def regular_zombie(contacts_dic):
    """Return the zombies that have come into contact
    with both potential zombies and people who are sick.

    Args:
        contacts_dic (dic): each entry is a sick person's name and their list
        of contacts.

    Returns:
        list: contains the names regular zombies.
    """
    values = list(contacts_dic.values())
    keys = list(contacts_dic.keys())
    spreader_predator = zombie_spreader(contacts_dic) + zombie_predator(contacts_dic)
    regular = sorted([x for x in keys if x not in spreader_predator])
    return regular

def zombie_predator(contacts_dic):
    """Return the zombies that have come into contact
    with people who are sick.

    Args:
        contacts_dic (dic): each entry is a sick person's name and their list
        of contacts.

    Returns:
        list: contains the names predator zombies.
    """
    predator_list = []
    return auxiliary_zombie_predator(contacts_dic, predator_list)

def auxiliary_zombie_predator(contacts_dic, predator_list, count = 0):
    values = list(contacts_dic.values())
    keys = list(contacts_dic.keys())
    if count == len(contacts_dic):
        return sorted(list(set(predator_list)))
    else:
        if all(x in keys for x in values[count]):
            predator_list.append(keys[count])
        count += 1
        return auxiliary_zombie_predator(contacts_dic, predator_list, count)






def main():

    """Main logic for the program.
    """
    filename = ""
    # Get the file name from the command line or ask the user for a file name
    args = sys.argv[1:]
    if len(args) == 0:
        filename = input("Please enter the name of the file: ")
    elif len(args) == 1:
        filename = args[0]
    else:
        print("""\n\nUsage\n\tTo run the program type:
        \tpython contact.py infile
        where infile is the name of the file containing the data.\n""")
        sys.exit()


    #Check that the file exists
    if not file_exists(filename):
        print("File does not exist, ending program.")
        sys.exit()

    #Create contacts dictionary from the file
    contacts_dic = parse_file(filename)

    #Spreader Zombies
    if zombie_spreader(contacts_dic) == []:
        print("Spreader Zombies: (None)")
    else:
        print(f"Spreader Zombies: {format_list(zombie_spreader(contacts_dic))}")

    #Regular Zombies
    if regular_zombie(contacts_dic) == []:
        print("Regular Zombies: (None)")
    else:
        print(f"Regular Zombies: {format_list(regular_zombie(contacts_dic))}")
    
    #Predator Zombies
    if zombie_spreader(contacts_dic) == []:
        print("Zombie Predators: (None)")
    else:
        print(f"Zombie Predators: {format_list(zombie_predator(contacts_dic))}")

if __name__ == "__main__":
        main()





