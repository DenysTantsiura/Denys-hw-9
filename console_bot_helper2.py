'''Task 9
bot........
.......'''

from genericpath import isdir
import os
import pickle


cont_dict = {}


def input_error(handler):
    '''...
    incoming: 
    return: '''
    global cont_dict

    # => user input command items in the list
    def exception_function(user_command):
        if handler == h_showall:
            if len(cont_dict) == 0:
                return "No contact records available\n"
        if handler == h_phone:
            if len(cont_dict) == 0:
                return "No contact records available\n"
            if not user_command[1]:
                return "Give me a name too, please\n"
            if 48 <= ord(user_command[1][0]) <= 57:
                return "A name cannot begin with a number!\n"
        if handler == h_change:
            if len(cont_dict) == 0:
                return "No contact records available. You can add records\n"
        if handler == h_change or handler == h_add:
            if not user_command[1] or not user_command[2]:
                return "Give me name and phone please\n"
            if 48 <= ord(user_command[1][0]) <= 57:
                return "A name cannot begin with a number!\n"
            if len([i for i in user_command[2] if 48 <= ord(user_command[2][0])] <= 57 or user_command[2][0] == '+') != len(user_command[1]):
                return "The number contains invalid characters\n"
        try:
            result = handler(user_command)
            if result == None:
                result = "No contact record available"
        except KeyError:
            result = f"{ValueError}"

        except ValueError:
            result = f"{ValueError}"

        except IndexError:
            result = "Give me name and phone please"

        return result

    return exception_function


def helper_try_open_file(path_file: str) -> str:
    '''...
    incoming: 
    return: '''
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
    '''...
    incoming: 
    return: '''
    global cont_dict
    return cont_dict.get(user_command[1])


@input_error
def h_change(user_command: list) -> str:  # list of str
    '''...
    incoming: 
    return: '''
    global cont_dict
    name = user_command[1]
    phone = user_command[2]
    cont_dict.pop(name, None)
    cont_dict.update({name: phone})
    with open(helper_opener()[1], "wb") as db_file:
        pickle.dump(cont_dict, db_file)

    return "The record has been changed\n"


@input_error
def h_add(user_command: list) -> str:
    '''...
    incoming: 
    return: '''
    global cont_dict
    name = user_command[1]
    phone = user_command[2]
    cont_dict.update({name: phone})
    with open(helper_opener()[1], "wb") as db_file:
        pickle.dump(cont_dict, db_file)
    return "The record added\n"


def h_exit(not_matter: any) -> str:
    return "Good bye!"


@input_error
def h_showall(not_matter: any) -> str:
    '''...
    incoming: 
    return: '''
    global cont_dict
    cont_dict = helper_opener()[0]
    all_list = ""
    for name, phone in cont_dict.items():
        all_list += f"{name} phone: {phone}" + "\n"

    return all_list


def helper_opener() -> list:
    '''...
    incoming: 
    return: '''
    path_file = 'ABook.bdata'
    new_path_file = helper_try_open_file(path_file)

    with open(new_path_file, 'rb') as f:
        stored_dict = pickle.load(f)

    return [stored_dict, new_path_file]


def main_handler(user_command: list):
    '''...
    incoming: 
    return: '''
    all_command = {"hello": h_hello(user_command),
                   "add": h_add(user_command),
                   "change": h_change(user_command),
                   "phone": h_phone(user_command),
                   "showall": h_showall(user_command),
                   "goodbye": h_exit(user_command),
                   "close": h_exit(user_command),
                   "exit": h_exit(user_command)}

    return all_command.get(user_command[0], "It is unclear")


def h_hello(user_command: any) -> str:
    return "How can I help you?\n"


def parser(user_input: str) -> list:
    '''...
    incoming: 
    return: '''
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
