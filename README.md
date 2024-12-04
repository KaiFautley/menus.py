(readme adapted from in-code docs)
# menus.py - Simple menu functions
menus.py is a small module designed to help quickly make simple and effective
text-based menus of various types. It handles erroneous inputs automatically.
## Functions
### mainMenu
&nbsp;&nbsp;Makes the user select one of any number of options
`mainMenu(title,options,return_name=False,return_index=True)`

`title`
&nbsp;&nbsp;The title of the menu
`options`
&nbsp;&nbsp;The list of menu options to display and select from
`return_name`
&nbsp;&nbsp;Returns the name of the option selected
`return_index`
&nbsp;&nbsp;Returns the index of the option in the list of options


### yesNo
&nbsp;&nbsp;Asks the user for a yes/no answer to a question
`yesNo(question)`

`question`
&nbsp;&nbsp;The question to be asked