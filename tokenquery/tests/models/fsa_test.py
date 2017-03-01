import unittest
from tokenquery.models.fsa import State
from tokenquery.models.fsa import StateMachine


class TestFSAClass(unittest.TestCase):

    def test_state(self):
        test_state = State('state_name', 'capture_name', None)
        self.assertEqual(test_state.get_state_name(), True)

        # TODO add more test

    def test_state_machine(self):
        pass

if __name__ == '__main__':
    unittest.main()
