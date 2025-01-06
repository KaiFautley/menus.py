# menus.py
# Simple menu-related functions with input validation
# Kai Fautley

# printed usage documentation is stored in a dictionary structure
docs = {
    "main_product" : {
        "title":"menus.py - Simple menu functions",
            "summary":"menus.py is a small module designed to help quickly make simple and effective\n"
            "text-based menus of various types. It handles erroneous inputs automatically."
    },"functions":{
        "mainMenu":{
            "syntax":"mainMenu(title,options,return_name=False,return_index=True)",
                "summary":"Makes the user select one of any number of options",
                "usage":{
                    "title":"The title of the menu",
                    "options":"The list of menu options to display and select from",
                    "return_name":"Returns the name of the option selected",
                    "return_index":"Returns the index of the option in the list of options"
                }
        },"yesNo":{
            "syntax":"yesNo(question)",
                "summary":"Asks the user for a yes/no answer to a question",
                "usage":{
                    "question":"The question to be asked"
                }
        }
    }
}

class InvalidMenuException(Exception):
    # Error used if params passed to a menu function are not valid in any way; normally accompanied with a helpful message
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def mainMenu(title,options,return_name=False,return_index=True):
    # Full text-based menu, gives a question and asks a user to select from a series of options. Handles most unexpected inputs.

    # check params - if they're not right, throw an error
    if type(options) != list:
        raise InvalidMenuException(f"Options is of type {type(options).__name__}, not list!") 
    
    elif type(title) != str:
        raise InvalidMenuException(f"Title is of type {type(title).__name__}, not str!")
    
    elif options == []:
        raise InvalidMenuException("Options cannot be empty")
    
    # create the printed text for the menu
    menu_text = f"{title}\n\n"
    for option in range(len(options)): # for each option, include the option number and name
        menu_text += f"  {option+1}. {options[option]}\n"
    menu_text += f"\nEnter an option [1-{option+1}]: "
    
    valid = False
    while not valid: # keep going until we get something actually useful out of the user
        # actual user interaction starts here
        choice = input(menu_text).strip()
        try:
            choice = int(choice) # attempt to convert `choice` to int is done separately such that the input can be printed in the event of an error at this step
        except ValueError:
            if choice.lower() in [x.lower().strip() for x in options]: # check if they typed out the choice instead of typing the number like they were told to
                valid = True
                choice = [x.lower() for x in options].index(choice.lower()) + 1 # convert it back into if they'd ctually done it right
            else:
                input(f"'{choice}' is not a valid whole number.")
        else:
            if choice in range(1,len(options)+1):
                valid = True # this is where the loop ends
            else:
                input(f"'{choice}' is not a valid option.") # `input` is used here so that the menu will only come back once the user has pressed Enter
    if return_name: # return the name of the option instead of the number chosen
        return options[choice-1]
    elif return_index: # return the list index
        choice -= 1
    return choice # return the choice as an integer for the program to deal with

def yesNo(question):
    # Keeps asking a question until Yes or No is entered
    # borrows some code from `menu`, more detailed comments are there

    # error handling
    if type(question) != str:
        raise InvalidMenuException(f"Question is of type {type(question).__name__}, not str!")
    
    menu_text = f"{question} [y/n]: "
    valid = False
    while not valid: # keep going until we get something actually useful out of the user
        # actual user interaction starts here
        choice = input(menu_text)
        try: # an exception will be raised if the input is empty, so use a try block to catch that
            if choice[0].lower() in ["y","n"]: # check if the first letter is "y" or "n", to catch if the user enters "Yes" or "No"
                valid = True
            else:
                input(f"{choice} is not Y or N.")
        except ValueError:
            input("Answer cannot be empty!")
    return choice[0].lower() # return the formatted result


if __name__ == "__main__":
    # print some quick docs
    docprint = f"This module cannot be run on its own, and is meant to be used inside of other applications.\n\n\033[1m\033[4m{docs["main_product"]["title"]}\033[0m\n  {docs["main_product"]["summary"]}\n\n"
    for func_ in docs["functions"]:
        func = docs["functions"][func_]
        docprint += f"\033[1m{func["syntax"]}\033[0m\n  {func["summary"]}\n\n"
        for arg in func["usage"]:
            docprint += f"{arg}\n  {func["usage"][arg]}\n"
        docprint += "\n\n"
    print(docprint)