# Copyright 2015 Amazon Web Services, Inc. or its affiliates. All rights reserved.

import unittest
import infections_data_uploader
import warnings

class InfectionsDataUploaderTest(unittest.TestCase):


    def test_infections_uploader(self):
        warnings.simplefilter("ignore", ResourceWarning)
        numFailures = infections_data_uploader.loadInfectionsData()
        self.assertEqual(0, numFailures)

if __name__ == '__main__':
    unittest.main()
