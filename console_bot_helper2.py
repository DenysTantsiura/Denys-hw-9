'''Task 9
Bot. A console bot helper that will recognize commands entered 
from the keyboard and respond accordingly.
The bot accepts commands:
"hello", replies to the console "How can I help you?"
"add ...". With this command, the bot saves a new contact in memory (in the dictionary, for example). Instead of ... the user enters the name and phone number, necessarily with a space.
"change ..." With this command, the bot stores the new phone number of the existing contact in memory. Instead of ... the user enters the name and phone number, necessarily with a space.
"phone ...." With this command, the bot outputs the phone number for the specified contact to the console. Instead of ... the user enters the name of the contact whose number should be displayed.
"show all". With this command, the bot outputs all saved contacts with phone numbers to the console.
"good bye", "close", "exit" by any of these commands, the bot ends its work after outputting "Good bye!" to the console.'''

from genericpath import isdir
import os
import pickle


cont_dict = {}


def input_error(handler):
    '''User error handler
    incoming: handler (function)
    return: result(str) or exception_function'''
    # global cont_dict

    # => user input command items in the list
    def exception_function(user_command):
        if handler.__name__ == "h_showall":
            if not cont_dict:
                return "No contact records available\n"
        if handler.__name__ == "h_phone":
            if not cont_dict:
                return "No contact records available\n"
            if len(user_command) < 2:
                return "Give me a name too, please\n"
            if user_command[1][0].isdigit():
                return "A name cannot begin with a number!\n"
            elif not user_command[1][0].isalpha():
                return "The name can only begin with Latin characters!\n"
        if handler.__name__ == "h_change":
            if not cont_dict:
                return "No contact records available. You can add records\n"
        number_separators = '+ ()-0123456789'
        if handler.__name__ == "h_change" or handler.__name__ == "h_add":
            if len(user_command) < 3:
                return "Give me name and phone please\n"
            if user_command[1][0].isdigit():
                return "A name cannot begin with a number!\n"
            elif not user_command[1][0].isalpha():
                return "The name can only begin with Latin characters!\n"
            if len([i for i in user_command[2] if i in number_separators]) != len(user_command[2]):
                return "The number contains invalid characters\n"

        try:
            result = handler(user_command)

        except KeyError as error:
            return f"An incorrect name was entered ({error})"

        except ValueError as error:
            return f"I don't know such commands ({error})"

        except IndexError as error:
            return f"No values in database ({error})"

        except Exception as error:
            return f"Something went wrong ({error})"

        if result is None:
            return "No contact record available"

        return result

    return exception_function


def helper_try_open_file(path_file: str) -> str:
    '''Checks if the database file exists and checks if the filename is free if not
    incoming: path_file is name of file
    return: name of file'''
    stored_dict = {}
    if os.path.isdir(path_file):
        while os.path.exists(path_file):
            path_file = "new_one_" + path_file

    if not os.path.isfile(path_file):
        with open(path_file, "ab") as words_file:
            pickle.dump(stored_dict, words_file)

    return path_file


@input_error
def h_phone(user_command: list) -> str:
    '''"phone ...." With this command, the bot outputs the phone number for the specified 
    contact to the console. Instead of ... the user enters the name of the contact 
    whose number should be displayed.
    incoming: list of user command (name of user)
    return: phone number of user'''
    # global cont_dict
    return cont_dict.get(user_command[1])


@input_error
def h_change(user_command: list) -> str:  # list of str
    '''"change ..." With this command, the bot stores the new phone number 
    of the existing contact in memory. Instead of ... the user enters 
    the name and phone number, necessarily with a space.
    incoming: list of user command (name of user)
    return: string'''
    # global cont_dict
    name = user_command[1]
    phone = user_command[2]
    cont_dict.pop(name, None)
    cont_dict.update({name: phone})
    with open(helper_opener()[1], "wb") as db_file:
        pickle.dump(cont_dict, db_file)

    return "The record has been changed\n"


@input_error
def h_add(user_command: list) -> str:
    '''"add ...". With this command, the bot saves 
    a new contact in memory (in the dictionary, for 
    example). Instead of ... the user enters the name 
    and phone number, necessarily with a space.
    incoming: list of user command (name of user)
    return: string'''
    # global cont_dict
    name = user_command[1]
    phone = user_command[2]
    cont_dict.update({name: phone})
    with open(helper_opener()[1], "wb") as db_file:
        pickle.dump(cont_dict, db_file)
    return "The record added\n"


def h_exit(_=None) -> str:
    return "Good bye!"


@input_error
def h_showall(_=None) -> str:
    '''"show all". With this command, the bot outputs all saved 
    contacts with phone numbers to the console.
    incoming: not_matter: any
    return: string of all users'''
    global cont_dict
    cont_dict = helper_opener()[0]
    all_list = ""
    for name, phone in cont_dict.items():
        all_list += f"{name} phone: {phone}\n"

    return all_list


def helper_opener() -> tuple:
    '''loads a list of users from a file
    incoming: None
    return: list of user dictionary and new path file(database)'''
    path_file = 'ABook.bdata'
    new_path_file = helper_try_open_file(path_file)

    with open(new_path_file, 'rb') as f:
        stored_dict = pickle.load(f)

    return (stored_dict, new_path_file)


def main_handler(user_command: list):
    '''All possible bot commands
    incoming: user command
    return: function according to the command'''
    all_command = {"hello": h_hello,
                   "add": h_add,
                   "change": h_change,
                   "phone": h_phone,
                   "showall": h_showall,
                   "goodbye": h_exit,
                   "close": h_exit,
                   "exit": h_exit}

    if all_command.get(user_command[0], "It is unclear") != "It is unclear":
        return all_command.get(user_command[0])(user_command)
    return "It is unclear"


def h_hello(_=None) -> str:
    return "How can I help you?\n"


def parser(user_input: str) -> list:
    '''Command parser. The part responsible for parsing 
    strings entered by the user, extracting keywords and 
    command modifiers from the string.
    incoming: string from user
    return: list of comands'''
    return user_input.strip().lower().replace("good bye", "goodbye").replace("show all", "showall").split(" ")


def main():
    global cont_dict
    # load contact dict if it available:
    cont_dict = helper_opener()[0]
    while True:
        user_command = input()
        user_request = parser(user_command)
        bot_answer = main_handler(user_request)
        print(bot_answer)
        if bot_answer == "Good bye!":
            break

    exit()


if __name__ == "__main__":
    exit(main())
