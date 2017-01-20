# Copyright 2015 Amazon Web Services, Inc. or its affiliates. All rights reserved.

import memcache
import sys
import utils
import dynamoDB_manager

CLUSTER_CONFIG_ENDPOINT = utils.LAB_8_CLUSTER_CONFIG_ENDPOINT

#Welcome to the AWS Python SDK! Let's build a Pharmaceutical drug listing!

def getCacheItem(client, cacheKey):
    #STUDENT TODO: Get the value from cache using the given key
    try:
        pharmaInfo = None
        pharmaInfo = client.get(cacheKey)
    except Exception as err:
        print("Error message: {0}".format(err))
    return pharmaInfo

#Returns pharmaceutical usage information for the given drug.
#Attempts to retrieve item from cache.
#If the item is not found in cache, retrieves the information from DynamoDB and updates cache.
def getPharmaInfo(drugName, clusterEndpoint=CLUSTER_CONFIG_ENDPOINT):
    #Retrieves pharmaceutical usage information from cache for the given drug name. Set the cache if not available
    try:
        pharmaInfo = None
        #STUDENT TODO: Create MemCachedClient object
        mclient = memcache.Client([clusterEndpoint], debug=0)
        pharmaInfo = getCacheItem(mclient, drugName)
        if not pharmaInfo:
            pharmaInfo = dynamoDB_manager.getPharmaInfo(drugName)
            if not pharmaInfo:
                print("Given drug name not available in the table")
                return None
            setPharmaItem(mclient, drugName, pharmaInfo)
            pharmaInfo = getCacheItem(mclient, drugName)

            if not pharmaInfo:
                print("Unable to set the cache for the given DrugName:{0}".format(drugName))
    except Exception as err:
        print("Error message: {0}".format(err))
    return pharmaInfo

def setPharmaItem(client, cacheKey, usageInfo):
    #Retrieves usage information from DynamoDB and then populates the cache with that information
    #STUDENT TODO: Cache the pharmaceutical item using drug name as cache key and drug information as cache value
    try:
        client.set(cacheKey, usageInfo, 3600)
    except Exception as err:
        print("Error message: {0}".format(err))

def setup():
    dynamoDB_manager.setup()

def main(drugName):
    #Setting up DynamoDB
    setup()
    pharmaInfo = getPharmaInfo(drugName)
    return pharmaInfo

if __name__ == '__main__':
    print("===============================================================")
    print("Welcome to the AWS Python SDK! Let's build a Pharmaceutical drug listing!")
    print("===============================================================")
    drugName = 'Octinoxate'
    if len(sys.argv) > 1:
        drugName = sys.argv[1]
    pharmaInfo = main(drugName)
    print("Retrieved pharmaceutical information:")
    print("Given DrugName: {0}".format(drugName))
    print("Retrieved DrugInfo: {0}".format(str(pharmaInfo)))
