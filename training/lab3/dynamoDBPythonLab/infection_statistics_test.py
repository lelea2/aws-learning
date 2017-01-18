# Copyright 2015 Amazon Web Services, Inc. or its affiliates. All rights reserved.

import unittest
import infection_statistics
import warnings

class InfectionStatisticsTest(unittest.TestCase):


    def test_infections_statistics(self):
        warnings.simplefilter("ignore", ResourceWarning)
        itemCount = infection_statistics.queryByCity(cityName="Reno")
        self.assertEqual(178, itemCount)

if __name__ == '__main__':
    unittest.main()
