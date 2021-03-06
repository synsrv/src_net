
import unittest, os, pickle

import numpy as np


class Test_dynamic_synaptic_weights(unittest.TestCase):

    
    with open('builds/0000/raw/synee_a.p', 'rb') as pfile:
        synee_a = pickle.load(pfile)

    def test_final_weights_different_from_initial(self):

        self.assertFalse(np.allclose(
                         self.synee_a['a'][-1,:],
                         self.synee_a['a'][ 0,:]))
    

if __name__ == '__main__':
    unittest.main()
