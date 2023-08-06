# module level doc-string
__doc__ = """
Generic functional utility module for KDS

@author: Manoj Bonam
Created on Fri Jul 30 15:29:55 2021

################################################# INSTRUCTIONS #########################################################
# In your program always import the entire kdsutil module first, to properly set the local variables.                  #
# from kdslib import kdsfunctionalutil                                                                                 #
########################################################################################################################

"""


import os
import yaml
import sys
import msal
import requests

#================================================================
# Check if environment variable is set
#================================================================
try:
    if os.name == 'nt':
        env = os.environ['kds-python-config']
        print("nt user's Environment variable:" + str(env))
    else:
        env = os.environ['kds_python_config']
        print("posix user's Environment variable:" + str(env))
except:
    print("Configuration file env variable is not set.")
    print("set kds-python-config variable")
    sys.exit(1)
    
#===============================================================
# If environment variable is set then read the config yaml file
#===============================================================
with open(env,"r") as yamlConfig:
    cfg = yaml.safe_load(yamlConfig)


"""
   The refreshPBIdataset function is used to refresh a PBI dataset. The workspaceID and datasetID have to be packed and passed
   as a dict to this function. 
   For a successful refresh, these(one or both, based on test vs prod) accounts have to be added as Members to your workspace/dataset
 
"""

def refreshPBIdataset(**kwargs):
    
    workspaceID_ = kwargs.get('WORKSPACEID')
    datasetID_ = kwargs.get('DATASETID')
    authority_url = cfg.get('PBI_OnDemand_Refresh').get('authority_url')
    resource_url = cfg.get('PBI_OnDemand_Refresh').get('resource_url')
    client_id = cfg.get('PBI_OnDemand_Refresh').get('client_id')
    clientsecret_ = cfg.get('PBI_OnDemand_Refresh').get('client_secret')
    
    app = msal.ConfidentialClientApplication(client_id,  #confidential client
                                             authority=authority_url,
                                             client_credential=clientsecret_)
    

    result = app.acquire_token_for_client(scopes=resource_url)
    access_token = result['access_token']   
    
    #refresh_url = 'https://api.powerbi.com/v1.0/myorg/groups/WORKSPACEID/datasets/DATASETID/refreshes'
    refresh_url = f'''https://api.powerbi.com/v1.0/myorg/groups/{workspaceID_}/datasets/{datasetID_}/refreshes'''
    header = {'Authorization': f'Bearer {access_token}'}
    r = requests.post(url=refresh_url, headers=header)
    return r.raise_for_status()
    
    