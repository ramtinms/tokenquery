import unittest
from tokenquery.models.stack import Stack


class TestStackClass(unittest.TestCase):

    def test_stack(self):
        test_stack = Stack()

        self.assertEqual(test_stack.is_empty(), True)
        self.assertEqual(test_stack.size(), 0)
        self.assertEqual(test_stack.peek(), None)
        self.assertEqual(test_stack.pop(), None)
        test_stack.push('A')
        test_stack.push('B')
        test_stack.push('C')

if __name__ == '__main__':
    unittest.main()
