# validin
Console input validator for python, allows for any condition to be checked in a clean and consice syntax


## Docs (temporary):
```
from validin import get_input
import validin.validators as valid
```

Use get_input to get valid user input

Example get_input() use:
- name = get_input("What's your name? ", valid.IsLetters())
- age = get_input("How old are you? ", valid.IsNaturalNumGreaterThan(18))


Input Validators:
- IsNaturalNum
- IsNaturalNumLessThan
- IsLetters
- IsLettersAndSymbols
- IsAlphanumeric
- IsAlphanumericAndSymbols
- IsOption

To create a new validator, 
    create a NewValidator() class with the condition and invalid input message wanted.
For a validator with more advanced functionality (such as dynamic invalid input messages), 
    create an InputValidator subclass (see the docs)