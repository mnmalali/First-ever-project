def main():
    while True:
        # Main Menu Display
        print("==============================")
        print("Renting Games Store Management System")
        print("1. Print games info")
        print("2. Search a game")
        print("3. Add new game")
        print("4. Remove a game")
        print("5. Borrow a game")
        print("6. Return a game")
        print("7. Exit")
        print("==============================")
        # get users choice of action
        game_choice = input("Enter your choice: ")
        # decides the action the user wants to perform
        if game_choice == "1":
            Printgamesinfo()
        elif game_choice == "2":
            main_search()
        elif game_choice == '3':
            main_of_adding_game()
        elif game_choice == "4":
            removeGame()
        elif game_choice == "5":
            Borrowagame()
        elif game_choice == "6":
            Returnagame()
        elif game_choice == "7":
            print("This program is terminating, Goodbye.")
            break
        else:
            print("Invalid option. Please enter a valid option (1-7).")


def Printgamesinfo():
    with open("GamesInfo.txt", "r") as Gamesinfofile:
        game_count = 0
        for _ in Gamesinfofile:
            game_count += 1
        print(f"Total Games: {game_count}")

        Gamesinfofile.seek(0)
        for line in Gamesinfofile:
            print("---------------------------------------------------------------------")
            serial_number, title, platforms, price, available_copies, borrowed_copies = line.strip().split(',')
            num_platforms = len(platforms.split(':'))
            total_copies = int(available_copies) + int(borrowed_copies)
            print(f"Serial #                 {serial_number}")
            print(f"Title: {title}")
            print(f"Number of Platforms: {num_platforms}")
            print(f"Price: {price}")
            print(f"Total Copies: {total_copies}")
            print("")


def search_title():  # This function allows the user search a game by its title
    user_input = input("Enter the title to find matched records: ")  # user to input a title.
    found = False
    with open('GamesInfo.txt', 'r') as file:  # opens the 'GamesInfo.txt' file in read mode
        for line in file:
            record = line.strip().split(',')
            serial_number, title, platforms, price, available_copies, borrowed_copies = record
            if user_input.lower() in title.lower():
                found = True
                print("Serial#:", serial_number)
                print('Title:', title)
                print('Platforms:')
                platforms = record[2].split(':')
                for plat in platforms:
                    print('\t\t-', plat)
                print('Price:', price)
                print('Copies in the store :', int(available_copies) - int(borrowed_copies))
                print('Borrowed copies', borrowed_copies)

    if not found:
        print("No match found.")


def search_platform():
    # Searches for records based on the platform name
    platform = input("Enter the platform name to find matched records: ")
    found = False

    with open('GamesInfo.txt', 'r') as file:  # opens the 'GamesInfo.txt' file in read mode
        for line in file:
            record = line.strip().split(',')
            serial_number, title, platforms, price, available_copies, borrowed_copies = record

            # Check if the entered platform is in the list of platforms for the current record
            if platform.lower() in platforms.lower():
                found = True
                print("Serial#:", serial_number)
                print('Title:', title)
                print('Platforms:')

                # Split the platforms string into a list and print each platform
                platform_list = platforms.split(':')
                for p in platform_list:
                    print('\t\t-', p.strip())

                print('Price:', price)
                print('Copies in the store:', int(available_copies) - int(borrowed_copies))
                print('Borrowed copies:', borrowed_copies)
                print('\n'+'--------------------------------------------------------------')

    if not found:
        print(f"No records found for platform: {platform}")


def main_search():
    # This part of the code asks the user to enter a choice ('t' for title search, 'p' for platform search)
    choice = input('Enter (t) to search by title, (p) to search by platform name: ')
    # used lower function incase user inputs capital letter
    if choice.lower() == 't':
        search_title()
        return
    elif choice.lower() == 'p':
        search_platform()
        return
    else:
        print("Invalid choice")
        return



# function for validating the users input
def validate_input(serial_number, title, platforms, platforms_added, price, available_copies):
    # a list for the error message:
    error_message = []

    # chech if serial number is a 7-digit number
    if len(serial_number) != 7 or not serial_number.isdigit():
        error_message.append("Error: serial number must be a 7-digit number")

    # open the gameinfo file
    with open('Gamesinfo.txt', 'r') as Gamesfile:
        for line in Gamesfile:
            if serial_number in line:
                error_message.append("Error: Serial number is already used.")

    # check the title is not empty
    if title == '':
        error_message.append("Error: title should not be empty")

    # check both the price and available copies
    try:
        # Try to convert price to number
        price = float(price)  # Convert 'price' to a float number

        # Check if the values are correct positive numbers
        if price <= 0:
            raise ValueError  # If not, raise a ValueError
    except ValueError:
        error_message.append("Error: price should be a valid float number.")

    try:
        # try to convert available copies to numbers
        available_copies = int(available_copies)  # Convert 'available_copies' to integer
        if available_copies <= 0:
            raise ValueError
    except ValueError:
        error_message.append("Error: number of copies should be a valid int number")

    # check if atleast one platform is added
    if platforms_added != True:
        error_message.append("Error: names of all platforms should not be empty")

    # check if any errors happend
    if error_message:
        return False, error_message
    else:
        return True, "Input is valid."  # returns true if all input is valid


def add_game(serial_number, title, platforms, price, available_copies):
    borrowed_copies = 0
    with open('Gamesinfo.txt', 'a') as file:
        file.write(f"{serial_number},{title},{platforms},{price},{available_copies},{borrowed_copies}\n")


# this program allows the user to add a game to the Gamesinfo file if the input is valid
def main_of_adding_game():
    while True:
        serial_number = input('enter a 7-digit serial number: ')
        title = input('enter game title: ')

        # for entering multiple platforms
        platforms = ''
        iteration = 1
        platforms_added = False  # variable to check if platforms are correctly added (flag)
        for i in range(1):
            platform = input(f'enter name of platform{iteration}:')
            platforms += platform + ':'

        while platform != 'q':
            iteration += 1
            platform = input(f'Enter name of platform{iteration}  (Enter q to finish): ')
            if platform == 'q':
                break
            else:
                if platform == '':
                    platforms_added = False
                elif '::' in platforms: # this is the part to add
                    platforms_added = False
                else:
                    platforms_added = True

            platforms += platform + ':'

        platforms = platforms.rstrip(': ')

        price = input('enter game price: ')

        available_copies = input('enter the number of  copies: ')

        # calls the validate input function and whatever it returns is stored in is_valid and massage
        is_valid, massages = validate_input(serial_number, title, platforms, platforms_added, price, available_copies)

        if is_valid == True:
            add_game(serial_number, title, platforms, price, available_copies)
            print('New Game Has Been Added Successfully')
        else:
            print("Invalid input. Please correct the following issues:")

            for massage in massages:
                print(massage)  # print error massages

        return


def removeGame():
    serial_number = input('enter the serial number of the game of you want to delete: ')
    found = False  # creat a bool vriable to use it as a flag

    with open("Gamesinfo.txt", 'r') as Gamesinfo:
        lines = Gamesinfo.readlines()  # save the information that is inside the file in a list

        # read the file and add each line to a list
        for line in lines:
            gameline = line.rstrip().split(',')

            # check if the serial number exist
            if gameline[0] == serial_number:
                found = True
                game_title = gameline[1]  # gets the title of the game
                # diplay the games info
                print('Matched records:')
                print(f'serial#:    {gameline[0]}')
                print(f'Title:  {gameline[1]}')

                # for diplaying the platforms in vertical order
                print('Platforms:')
                platforms = gameline[2].split(':')
                for platform in platforms:
                    print(f'\t\t-{platform}')

                print(f'Price:  {gameline[3]}')
                print(f'Copies in the store {gameline[4]}')
                print(f'Borrowed copies {gameline[5]}')
                print('\n' + '----------------------------------')

                cond = input(f'Deleting the game  {game_title} are you sure? (yes/no): ')
                if cond == 'y' or cond == 'Y' or cond == 'yes' or cond == 'YES':
                    borrowed_copies = int(gameline[5])
                    # check the number of borrowed copies
                    if borrowed_copies == 0:
                        with open('Gamesinfo.txt', 'w') as Gamesinfo:
                            lines.remove(line)

                            for line in lines:
                                Gamesinfo.write(line)

                        print(f'{game_title} game was removed successfully :) ')
                        return

                    else:
                        print('Game cannot be removed: borrowed copies must be 0')
                        return

                else:
                    print('operation cancelled')
                    return

    # display the error message of the game not found
    if not found:
        print('ERROR: The given serial number is not valid :( .')
        return


def Borrowagame():
    serial_borrowed = input("Enter the serial number of the game you want to borrow: ")  # input from user
    if not len(serial_borrowed) == 7:  # checks if the serial number has 7 digits
        print("serial number should be 7 digits")
        return
    with open("GamesInfo.txt", "r") as borowedGamesInfo_check:
        games_info = borowedGamesInfo_check.read()
        if serial_borrowed not in games_info:  # file is put into one string and checks if serial number is in the string
            print("No matched serial number")
            return
        borowedGamesInfo_check.seek(0)  # to ensure no error occurs it begins from first line once again
        for line in borowedGamesInfo_check:
            serial_number, title, platforms, price, available_copies, borrowed_copies = line.split(",")
            serial_number = serial_number.strip()
            if serial_borrowed == serial_number:
                if available_copies == "0":  # checks if there are any available copies
                    print("There are no available copies")
                    return
    id_borrowed = input("Enter your id to borrow the game: ")  # takes id input from user
    id_count = 0
    input_formatted = serial_borrowed + "," + id_borrowed

    with open("BorrowedInfo.txt", "r") as borrowedInfo_check:
        for line in borrowedInfo_check:
            if id_borrowed in line:  # counts how many games the user with the id has borrowed
                id_count += 1
            if input_formatted in line:  # checks if the id and serial number have a match in the file, if there is you are not allowed to borrow again
                print("You have already borrowed this game.")
                return

    if id_count >= 3:  # checks how many times this user has already borrowed games
        print("You can only borrow 3 games at a time")
        return
    with open("BorrowedInfo.txt", "a") as borrowed_file:
        borrowed_file.write("\n" + serial_borrowed + "," + id_borrowed)  # appends new record of borrowed game into the file
        print("The game has been borrowed successfully")

    with open("GamesInfo.txt", "r") as gamesinfofile:  # changes the number of available copies and borrowed copies
        list_check = gamesinfofile.readlines()
        list_append = []
        for line in list_check:
            linesplit = line.split(',')
            serial_number, title, platforms, price, available_copies, borrowed_copies = linesplit
            if serial_borrowed == serial_number:  # changes the attributes of the game borrowed
                available_copies = str(int(available_copies) - 1)
                borrowed_copies = str(int(borrowed_copies) + 1)
            list_append.append(f"{serial_number},{title},{platforms},{price},{available_copies},{borrowed_copies}")
        with open("GamesInfo.txt", "w") as gamesinfoappend:
            for line in list_append:  # writes new and updated information back into file
                gamesinfoappend.write(line.strip() + "\n")
        return


def Returnagame():
    serial_return = input("Enter the serial number of the game you want to return: ").strip()  # input from user
    id_return = input("Enter your id to return the game: ").strip()
    listborrowappend = []
    formatted_input = serial_return + "," + id_return  # same format as in file
    with open("BorrowedInfo.txt", "r") as returninfo_check:
        list_check_return = returninfo_check.readlines()
        list_check_return2 = [line.rstrip() for line in list_check_return]  # removes \n from end of each line
        if formatted_input not in list_check_return2:  # looks for an exact match in file
            print("Error: no matched record found in borrowedinfo.txt")
            return
        for line in list_check_return:
            serial_number, idofreturnfile = line.strip().split(",")
            lineformatted = serial_number + "," + idofreturnfile
            if serial_return == serial_number and id_return == idofreturnfile:  # line is not added to new list if matched, so it is essentially removed
                continue
            else:
                listborrowappend.append(lineformatted)
    with open("BorrowedInfo.txt", "w") as borrowedinfappend:
        for line in listborrowappend:  # writes borrowed games back into file without the game returned
            borrowedinfappend.write(line.strip() + "\n")

    with open("GamesInfo.txt", "r") as gamesinfofile:
        list_check = gamesinfofile.readlines()
        list_append = []
        for line in list_check:  # updates the number available and borrowed games
            serial_number, title, platforms, price, available_copies, borrowed_copies = line.split(",")
            if serial_return == serial_number:
                available_copies = str(int(available_copies) + 1)
                borrowed_copies = str(int(borrowed_copies) - 1)
            list_append.append(f"{serial_number},{title},{platforms},{price},{available_copies},{borrowed_copies}")
        with open("GamesInfo.txt", "w") as gamesinfoappend:
            for line in list_append:  # updated information written back into file
                gamesinfoappend.write(line.strip() + "\n")
            print("Game succesfully returned")
            return


main()


