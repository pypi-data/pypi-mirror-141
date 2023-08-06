
def take_user_input():
    number = int(input("Enter the index for fibonacci calculation user : "))
    return number

def fibonacciGeneratingFunction(number):
    import numpy as np 
    import math
    phi = (1 + np.sqrt(5)) / 2
    fn = math.floor(np.round((pow(phi, number)) / np.sqrt(5)))
    return ("The {}th fibonacci number is {}".format(number, fn))


# if __name__ == "__main__":

#     NUM = take_user_input()
#     RESULT = fibonacciGeneratingFunction(NUM)
#     print(RESULT)



    