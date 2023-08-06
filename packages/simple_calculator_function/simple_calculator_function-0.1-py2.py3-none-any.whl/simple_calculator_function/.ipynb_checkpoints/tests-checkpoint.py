from calculator_simple_function import calculator
import unittest
c= calculator.Calculator()
class TestCalculator(unittest.TestCase):
   
    def test_add(self):
        return self.assertEqual(c.add(9,1), 7,"Incorrect")
        
    def test_subtract(self):
        return self.assertEqual(c.subtract(9,1), 7,"Incorrect")
    
    def test_division(self):
        return self.assertEqual(c.divide(0, 7),'Can not divide by zero.', "incorrect")
    
    def test_multiply(self):
        return self.assertEqual(c.multiply(15, 15),20, "Incorrect")
    
    def nth_root(self):
        return self.assertEqual(c.root(-4) , 'Invalid input',"Incorrect")
        
    def test_invalid(self):
        assert c.add('hello', 'hi') == 'Invalid input'
        
        assert c.subtract('how', 'are') == 'Invalid input'
        
        assert c.multiply('you', 'doing') == 'Invalid input'
        
        assert c.divide('i', 'am') == 'Invalid input'
        
        assert c.root('fine', 'thanks') == 'Invalid input'
        
    
    
    def test_memory(self):
        c.reset_memory()

        assert c.add(0) == 0
        assert c.add(1) == 1
        assert c.add(15) == 16

        c.reset_memory()

        assert c.subtract(0) == 0
        assert c.subtract(1) == -1
        assert c.subtract(1) == -2

        c.reset_memory()

        assert c.multiply(1, 1) == 1
        assert c.multiply(2,2) == 4
        assert c.multiply(12) == 48

        c.reset_memory()

        assert c.divide(2, 20) == 10
        assert c.divide(2) == 5
        assert c.divide(5) == 1

        c.reset_memory()

        assert c.root(2) == 0
        assert c.root(3,27) == 3
        assert c.root(2,256) == 16

        
