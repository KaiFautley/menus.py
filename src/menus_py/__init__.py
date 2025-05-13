# menus.py
# Simple menu-related functions with input validation
# Kai Fautley
import warnings as _w

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
        },"simpleChoice":{
            "syntax":"simpleChoice(question,letters,first_only=True)"
        },"yesNo":{
            "syntax":"yesNo(question)",
                "summary":"Calls simpleChoice(question, [\"y\",\"n\"]). Deprecated as of 1.3.0 as\n"
                "simpleChoice supersedes it, though remains present (and functionally identical)\n"
                "for compatibility reasons.",
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

def mainMenu(title,options,return_name=False,return_index=True,layout="  {}. {}"): # layout defaults to match pre-1.3.0 behaviour
    # Full text-based menu, gives a question and asks a user to select from a series of options. Handles most unexpected inputs.

    # check the options list is actually a list and throw an error if not
    if type(options) is not list:
        raise InvalidMenuException(f"Options is of type {type(options).__name__}, not list!") 
    # similar check for the title being a string
    elif type(title) is not str:
        raise InvalidMenuException(f"Title is of type {type(title).__name__}, not str!")
    # check there are actually options to choose from
    elif options == []:
        raise InvalidMenuException("Options cannot be empty")
    # check that the layout is valid
    if layout.count("{}") != 2:
        raise InvalidMenuException("Invalid layout, too little or too many {}'s'")
    
    # create the printed text for the menu
    menu_text = f"{title}\n\n" # title and newlines
    for option in range(len(options)): # for each option, include the option number and name
        menu_text += layout.format(option+1, options[option])+"\n" # use layout to define the style of the options - new in 1.3.0
    menu_text += f"\nEnter an option [1-{option+1}]: " # Prompt for the user
    
    valid = False
    while not valid: # keep going until we get something actually useful out of the user
        # actual user interaction starts here
        choice = input(menu_text).strip() # strip the user input for easier processing
        try:
            choice = int(choice) # attempt to convert `choice` to int is done separately such that the input can be printed in the event of an error at this step
        except ValueError:
            if choice.lower() in [x.lower().strip() for x in options]: # check if they typed out the choice instead of typing the number like they were told to
                valid = True
                choice = [x.lower() for x in options].index(choice.lower()) + 1 # set choice to the integer equivalent of the selected option
            else:
                input(f"'{choice}' is not a valid whole number.")
        else:
            if choice in range(1,len(options)+1): # check the entered number is within range
                valid = True # this is where the loop ends
            else:
                input(f"'{choice}' is not a valid option.") # `input` is used here so that the menu will only come back once the user has pressed Enter
    if return_name: # return the name of the option instead of the number chosen
        return options[choice-1]
    elif return_index: # return the list index
        choice -= 1
    return choice # return the choice as an integer for the program to deal with

def simpleChoice(question,letters,first_only=True):
    # Basic choice of single-letter options - replaces core for yesNo()
    # New in 1.3.0

    # Make sure the question is a string
    if type(question) is not str:
        raise InvalidMenuException(f"Question is of type {type(question).__name__}, not str!")
    # check letter list is valid
    if type(letters) is not list:
        raise InvalidMenuException(f"Letter list is of type {type(letters).__name__}, not list!")
    letters2 = []
    for letter in letters:
        if len(letter) > 1: # This only allows single-letter options
            raise InvalidMenuException(f"Option '{letter}' is too long!")
        if letter.upper() in letters2: # Two occurences of a letter can be confusing
            raise InvalidMenuException(f"Option '{letter}' appears more than once!")
        letters2.append(letter.upper()) # This both ensures the above check works and creates a list of all-capitalised letters
    if letters == []:
        raise InvalidMenuException("List of options cannot be empty!") # Ensures the list actually has options in it
    
    menu_text = f"{question} [{"".join([f"{letters[i]}/" for i in range(len(letters)-1)])}{letters[-1]}]: " # Formats the menu text. It's a bit of a mess, I'll clean it up later.

    valid = False
    while not valid: # keep going until we get something actually useful out of the user
        # actual user interaction starts here
        choice = input(menu_text).strip()
        try: # an exception will be raised if the input is empty, so use a try block to catch that
            if first_only:
                choice = choice[0] # only check the first letter so any unabbreviated forms (e.g. "y" for "yes") will work.
            else:
                choice[0] # try anyway to make sure "Answer cannot be empty!" is triggered
            if choice.upper() in letters2:
                valid = True
            else:
                input(f"{choice} is not an option.")
        except IndexError:
            input("Answer cannot be empty!")
    return choice[0].lower() # return the formatted result

def yesNo(question):
    # Deprecated as of 1.3.0
    _w.warn(DeprecationWarning("This function is deprecated and may be removed in a future version of the module."))
    return simpleChoice(question,["y","n"])


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
