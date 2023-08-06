def addition(num1, num2):
    """
    Function to get the sum off two numbers
    :param num1: the number on which the operations takes place
    :param num2: the number that gets added to the first one
    :return: Returns the Sum
    """
    sum = num1 + num2
    return sum

def substract(num1, num2):
    """
    Function to get the Difference between two numbers
    :param num1: the number on which the operations takes place
    :param num2: the number that gets substracted from the first one
    :return: Returns the Difference
    """
    dif = num1 - num2
    return dif

def divide(num1, num2):

    """
    Function to get the Quotient for two numbers
    :param num1: the number on which the operations takes place
    :param num2: the divisor
    :return: Returns the Quotient
    """
    if num2 == 0:
        print('Deviding by 0 not allowed')
    else:
        quotient = num1 / num2
        return quotient


"""Comment"""

def multiply(num1, num2):
    """
    Function to get the Product of two numbers
    :param num1: first number for the multiplikation
    :param num2: second number for the multiplication
    :return: returns the product
    """
    product = num1 * num2
    return product