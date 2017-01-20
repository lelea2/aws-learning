# Copyright 2015 Amazon Web Services, Inc. or its affiliates. All rights reserved.

import unittest, warnings
import sys
import memcache
import cache_manager
import utils

CLUSTER_CONFIG_ENDPOINT = utils.LAB_8_CLUSTER_CONFIG_ENDPOINT

class ElastiCacheTestCase(unittest.TestCase):
    warnings.simplefilter("ignore", ResourceWarning)
    drugName = "Ibuprofen"
    cacheMgr = memcache.Client([CLUSTER_CONFIG_ENDPOINT], debug=0)

    def test(self):
        warnings.simplefilter("ignore", ResourceWarning)
        try:
            drugName = ElastiCacheTestCase.drugName
            cacheMgr = ElastiCacheTestCase.cacheMgr
            cache_manager.setup()

            pharmaInfo = getFromCache(cacheMgr, drugName)
            print("First Access - Item from cache", pharmaInfo)
            self.assertIsNone(pharmaInfo)

            pharmaInfo = cache_manager.getPharmaInfo(drugName)
            self.assertIsNotNone(pharmaInfo)
            print("Item from cache or DB", pharmaInfo)

            pharmaInfo = getFromCache(cacheMgr, drugName)
            self.assertIsNotNone(pharmaInfo)
            print("Next Access - Item from cache", pharmaInfo)

        except Exception as err:
            print("Error message: {0}".format(err))
            sys.exit(1)
        cacheMgr = None

def getFromCache(cacheMgr, cacheKey):
    try:
        pharmaInfo = None
        pharmaInfo = cacheMgr.get(cacheKey)
    except Exception as err:
        print("Error message: {0}".format(err))
    return pharmaInfo

def deleteKeyInCache(cacheMgr, cacheKey):
    try:
        cacheMgr.delete(cacheKey)
    except Exception as err:
        print("Error message: {0}".format(err))

if __name__ == '__main__':
    unittest.main()
