import unittest
from tokenquery.acceptors.int_opr import int_value
from tokenquery.acceptors.int_opr import int_ne
from tokenquery.acceptors.int_opr import int_e
from tokenquery.acceptors.int_opr import int_l
from tokenquery.acceptors.int_opr import int_le


class TestIntegerCoreAcceptorsClass(unittest.TestCase):

    def test_integer_methods(self):
        self.assertEqual(int_value('5', '=5'), True)
        self.assertEqual(int_value('5.6', '>a'), False)
        self.assertEqual(int_value('3', '=5.3'), False)
        self.assertEqual(int_value('token', '=4'), False)
        self.assertEqual(int_value('21', '=21'), True)
        self.assertEqual(int_ne('6', '5'), True)
        self.assertEqual(int_e('6', '5'), False)
        self.assertEqual(int_e('5', '5'), True)
        self.assertEqual(int_l('5', '6'), True)
        self.assertEqual(int_le('4', '5'), True)
        self.assertEqual(int_le('5', '5'), True)

if __name__ == '__main__':
    unittest.main()
