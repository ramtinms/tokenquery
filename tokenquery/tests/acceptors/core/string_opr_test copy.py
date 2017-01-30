import unittest
from tokenquery.acceptors.vector_opr import change_string_to_vector
from tokenquery.acceptors.vector_opr import cos_sim
from tokenquery.acceptors.vector_opr import cos_dist
from tokenquery.acceptors.vector_opr import man_dist


class TestVectorCoreAcceptorsClass(unittest.TestCase):

    def test_change_to_vector_method(self):
        self.assertEqual(change_string_to_vector('[0, 1, 0.06,   3,4,5.4, 0.0, -1]'),
                         [0.0, 1.0, 0.06, 3.0, 4.0, 5.4, 0.0, -1.0])

    def test_cos_sim_method(self):
        input_token_string = '[0.0, 1.0, 0.06, 3.0, 4.0, 5.4, 0.0]'
        param_string = '[0.0, 1.0, 0.06, 3.0, 4.0, 5.4, 0.0] > 0.5'
        self.assertEqual(cos_sim(input_token_string, param_string), True)

        input_token_string = '[0.0, 1.0, 0.06, 3.0, 4.0, 5.4, 0.0]'
        param_string = '[12.0, -1.0, 1.00, 3.0, -4.0, 5.4, 0.0] > 0.5'
        self.assertEqual(cos_sim(input_token_string, param_string), False)

    def test_cos_dist_method(self):
        input_token_string = '[0.0, 1.0, 0.06, 3.0, 4.0, 5.4, 0.0]'
        param_string = '[0.0, 1.0, 0.06, 3.0, 4.0, 5.4, 0.0] > 0.5'
        self.assertEqual(cos_dist(input_token_string, param_string), False)

        input_token_string = '[0.0, 1.0, 0.06, 3.0, 4.0, 5.4, 0.0]'
        param_string = '[12.0, -1.0, 1.00, 3.0, -4.0, 5.4, 0.0] > 0.5'
        self.assertEqual(cos_dist(input_token_string, param_string), True)

    def test_man_dist_method(self):
        input_token_string = '[0.0, 1.0, 0.06, 3.0, 4.0, 5.4, 0.0]'
        param_string = '[0.0, 1.0, 0.06, 3.0, 4.0, 5.4, 0.0] == 0'
        self.assertEqual(man_dist(input_token_string, param_string), True)

        input_token_string = '[0.0, 1.0, 0.06, 3.0, 4.0, 5.4, 0.0]'
        param_string = '[12.0, -1.0, 1.00, 3.0, -4.0, 5.4, 0.0] > 20'
        self.assertEqual(man_dist(input_token_string, param_string), True)


if __name__ == '__main__':
    unittest.main()
