"""
This file contains code for the game "Java Class Generator".
Author: DigitalCreativeApkDev
"""

# Importing necessary libraries
import sys
import os


# Creating necessary functions


def clear():
    # type: () -> None
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows System
    else:
        os.system('clear')  # For Linux System


def capitalize_first(string: str) -> str:
    if len(string) == 0:
        return ""
    elif len(string) == 1:
        return string[0].capitalize()
    else:
        return string[0].capitalize() + string[1::]


def generate_attributes(attribute_names: list, attribute_types: list) -> str:
    result: str = ""  # initial value
    for i in range(min(len(attribute_names), len(attribute_types))):
        result += """
    private """ + str(attribute_types[i]) + """ """ + str(attribute_names[i]) + """;
    """

    return result


def generate_constructor(class_name: str, parameters: list, parameter_types: list) -> str:
    parameter_initialization: str = ""  # initial value
    for parameter in parameters:
        parameter_initialization += """
        this.""" + str(parameter) + """ = """ + str(parameter) + """;    
    """

    between_brackets: str = ""  # initial value
    for i in range(len(parameters)):
        between_brackets += str(parameter_types[i]) + " " + str(parameters[i])
        if i < len(parameters) - 1:
            between_brackets += ", "

    result: str = """
    public """ + str(class_name) + """(""" + str(between_brackets) + """){
    """ + str(parameter_initialization) + """
    }
    """

    return result


def generate_getter(attribute_name: str, attribute_type: str) -> str:
    return """
    public """ + str(attribute_type) + """ get""" + capitalize_first(str(attribute_name)) + """() {
        return """ + str(attribute_name) + """;
    }
    """


def generate_setter(attribute_name: str, attribute_type: str) -> str:
    return """
    public void set""" + capitalize_first(str(attribute_name)) + """(""" + str(attribute_type) + """ """ \
           + str(attribute_name) + """){
        this.""" + str(attribute_name) + """ = """ + str(attribute_name) + """;
    """


def generate_method(method_name: str, return_type: str, parameters: list, parameter_types: list) -> str:
    between_brackets: str = ""  # initial value
    for i in range(len(parameters)):
        between_brackets += str(parameter_types[i]) + " " + str(parameters[i])
        if i < len(parameters) - 1:
            between_brackets += ", "

    return """
    public """ + str(return_type) + """ """ + str(method_name) + """(""" + str(between_brackets) + """){
        throw new Exception(\"Method not implemented\");
    }"""


# Creating main function used to run the application.


def main():
    """
    This main function is used to run the application.
    :return: None
    """

    print("Welcome to 'Java Class Generator' by 'DigitalCreativeApkDev'.")
    print("This application allows you to easily generate the template of a Java class you want to write!")
    print("Enter 'Y' for yes.")
    print("Enter anything else for no.")
    continue_using: str = input("Do you want to continue using the application 'Java Class Generator'? ")
    while continue_using == "Y":
        # Clearing the command line window
        clear()

        class_name: str = input("Please enter the name of the class you want to write: ")

        script: str = """
class """ + str(class_name) + """{
        """

        attributes: list = []  # initial value
        attribute_types: list = []  # initial value
        num_attributes: int = int(input("How many attributes do you want in your class (at least 0)? "))
        while num_attributes < 0:
            num_attributes = int(input("Sorry, invalid input! "
                                       "How many attributes do you want in your class (at least 0)? "))

        for i in range(num_attributes):
            attribute_name: str = input("Please enter the name of the attribute you want to add: ")
            while attribute_name in attributes:
                attribute_name = input("Sorry! That attribute is already used! Please enter another name: ")

            attribute_type: str = input("Please enter the type of the attribute '" + str(attribute_name) + "': ")

            attributes.append(attribute_name)
            attribute_types.append(attribute_type)

        script += generate_attributes(attributes, attribute_types)
        script += generate_constructor(class_name, [], [])
        script += generate_constructor(class_name, attributes, attribute_types)

        for i in range(len(attributes)):
            script += generate_getter(attributes[i], attribute_types[i])
            script += generate_setter(attributes[i], attribute_types[i])

        num_methods: int = int(input("How many methods do you want to create in '" + str(class_name) + "' class? "))
        for i in range(num_methods):
            method_name: str = input("Please enter the name of the method: ")
            return_type: str = input("Please enter the return type of the method: ")
            parameters: list = []
            parameter_types: list = []  # initial value
            num_parameters: int = int(input("How many parameters do you want in the method '"
                                            + str(method_name) + "' (at least 0)? "))
            while num_parameters < 0:
                num_parameters = int(input("Sorry, invalid input! How many parameters do you want in the method '"
                                           + str(method_name) + "' (at least 0)? "))

            for k in range(num_parameters):
                parameter_name: str = input("Please enter the name of the parameter: ")
                parameter_type: str = input("Please enter the type of the parameter: ")
                parameters.append(parameter_name)
                parameter_types.append(parameter_type)

            script += generate_method(method_name, return_type, parameters, parameter_types)

        script += """       
}"""

        f = open(str(class_name) + ".java", "w")
        f.write(script)
        f.close()

        # Clearing the command line window
        clear()
        print("Your class is written in the file '" + str(class_name) + ".java'!")
        print("Enter 'Y' for yes.")
        print("Enter anything else for no.")
        continue_using = input("Do you want to continue using the application 'Java Class Generator'? ")
    sys.exit()


if __name__ == '__main__':
    main()
