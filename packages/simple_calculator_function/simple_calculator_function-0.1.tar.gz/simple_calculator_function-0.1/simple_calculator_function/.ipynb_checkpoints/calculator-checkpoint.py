class Calculator:
    """Calculator class that performs the basic mathematical operations , addition, subtraction, multiplication , division , n'th root , also able to keep and reset last number.
    """ 
    
    def __init__(self,initial = 0):
        self.currentvalue = initial

    def reset_memory(self):
         
        """Resets the memory back to zero"""
        self.currentvalue = 0

    def add(self, number1, number2 = None):
        """
        Returns sum of two number values
        """
        try:
            if number2 == None:
                number2 = self.currentvalue

            self.currentvalue = float(number1) + float(number2)
            return self.currentvalue
        except:
            return 'Invalid input'

    def subtract(self, number1, number2 = None):
        """
        Subtracts number1 from number2 and returns the result
        """
        try:
            if number2 == None:
                number2 = self.currentvalue

            self.currentvalue = float(number2) - float(number1)
            return self.currentvalue
        except:
            return 'Invalid input'

    def multiply(self,  number1, number2 = None):
        """ 
        Multiplies two numbers number1 and number2 and returns the result
        """
        try:
            if number2 == None:
                number2 = self.currentvalue

            self.currentvalue = float(number1) * float(number2)
            return self.currentvalue
        except:
            return 'Invalid input'



    def divide (self,  number1, number2 = None):
        """ Divides number2 by number1 and returns the result
        """
        try:
            if number2 == None:
                number2 = self.currentvalue

            self.currentvalue = float(number2) / float(number1)
            return self.currentvalue
        except ZeroDivisionError:
            return 'Can not divide by zero.'
        except: 
            return 'Invalid input'


    def root(self,number1,number2=None):
        """
        Returns the number1'th Root of number2 
        """
        try:
            if number2 == None:
                number2 = self.currentvalue

            self.currentvalue = float(float(number2) ** (1/float(number1)))
            return self.currentvalue
        except:
            return 'Invalid input'



