import unittest
from tokenquery.acceptors.string_opr import str_eq
from tokenquery.acceptors.string_opr import str_reg
from tokenquery.acceptors.string_opr import str_len


class TestStringCoreAcceptorsClass(unittest.TestCase):

    def test_string_methods(self):

        self.assertEqual(str_eq('equal', u'equal'), True)
        self.assertEqual(str_eq('equal', 'equal'), True)
        self.assertEqual(str_eq('equal', 'nequal'), False)
        self.assertEqual(str_reg('equal', 'eq.*'), True)
        self.assertEqual(str_reg('equal', '^eq.*'), True)
        self.assertEqual(str_reg('equal', 'neq.*'), False)
        self.assertEqual(str_reg('equal', '(eq.*)'), True)
        self.assertEqual(str_len('token', ',5'), True)
        self.assertEqual(str_len('token', '=5'), True)
        self.assertEqual(str_len('token', '>a'), False)
        self.assertEqual(str_len('token', ',5.3'),  False)
        self.assertEqual(str_len('token', ',4'), False)
        self.assertEqual(str_len('token', ',-1'), False)

if __name__ == '__main__':
    unittest.main()
