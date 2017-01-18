# Copyright 2015 Amazon Web Services, Inc. or its affiliates. All rights reserved.

import unittest
import utils
import infection_statistics
import warnings

TABLE_NAME = utils.LAB_S3_INFECTIONS_TABLE_NAME


class PatientReportLinkerTest(unittest.TestCase):


    def test_report_link(self):
        warnings.simplefilter("ignore", ResourceWarning)
        dynamodb = utils.connect2Service('dynamodb')
        myTable = dynamodb.Table(TABLE_NAME)
        for i in range(1, 4):
            isPresent = False
            rec = myTable.get_item(Key={'PatientId': str(i)})
            if rec.get('Item').get('PatientReportUrl'):
                isPresent = True
            self.assertTrue(isPresent)

if __name__ == '__main__':
    unittest.main()
