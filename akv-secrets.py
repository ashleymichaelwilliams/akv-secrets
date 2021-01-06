#!/bin/python
import sys, os, re, json
import fileinput

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


# Declare static input variables
file_name = (sys.argv[1])
akv_store_name = (sys.argv[2])
akv_common_store_name = (sys.argv[3])


# Set Azure Credentials using Default Environment Variables for use with the Azure Key Vaults
credential = DefaultAzureCredential()


print()

# Reads each line of template file
with open(file_name, 'r') as fp:
    parseOutput = filter(None, fp.read().splitlines())

    # Builds list of items (lines of text) from the tamplate file
    returned_list = []
    returned_list = list(parseOutput)

    # Filters list to variables (with curly braces) and cleans formatting storing items into a new list
    filtered_results = []
    for items in returned_list:

        open_curly_braces   = '{{'
        closed_curly_braces = '}}'

        if (open_curly_braces in items) and (closed_curly_braces in items):
            filtered_results.append(items)

            # Removes curly braces '{{' and '}}'
            filtered_results = [re.sub(r'(' + open_curly_braces + '|' + closed_curly_braces + ')', '', curly_braces) for curly_braces in filtered_results]
            # Removes spaces and key string 'someKey: '
            filtered_results = [re.sub(r'\ +.*: ', '', key) for key in filtered_results]


    # Builds a dictionary with keys from the filtered list
    a_dict = {}
    for kv in filtered_results:
        a_dict.update({ kv : ''})


# Fetches secret's (value) using the secret's name (key) and updates dictionary values
for k, v in a_dict.items():
    print("Now fetching Secret: ", k)
    try:
        # Constructs the URL connection string for the Azure Key Vault service
        AKV_URL_ADDR = 'https://{}.vault.azure.net'.format(akv_store_name)

        # Authenticates with specified Azure Key Vault using the default credentials
        secret_client = SecretClient(vault_url=AKV_URL_ADDR, credential=credential)
        secret = secret_client.get_secret(k)

    except:
        try:
            print()
            print("WARNING:")
            print("The secret '" + k + "'" + " is missing from the '" + akv_store_name + "' Key Vault, now trying the '" + akv_common_store_name + "' Key Vault...")

            AKV_COMMON_URL_ADDR = 'https://{}.vault.azure.net/'.format(akv_common_store_name)

            # Authenticates with Common Azure Key Vault using the default credentials
            secret_client = SecretClient(vault_url=AKV_COMMON_URL_ADDR, credential=credential)
            secret = secret_client.get_secret(k)
            print("SUCCESS:")
            print("Found the secret '" + k + "'" + " in the '" + akv_common_store_name + "' Key Vault!")
            print()

        except:
            print("Failed to find the secret '" + k + "'" + " in the '" + akv_common_store_name + "' Key Vault!")
            print()

    finally:
        a_dict[k] = secret.value


print()

# Prints the dictionary with the fetched values
print("Dictionary Result:")
print(json.dumps(a_dict, indent=4, sort_keys=True))
print()


# Iterate over the specified file replacing the {{placeholder}} with the value from dictionary
for line in fileinput.input(files=file_name, inplace=True):
    line = line.rstrip()

    for f_key, f_value in a_dict.items():
        if f_key in line:
            line = line.replace(f_key, f_value)
            line = line.replace(open_curly_braces, '')
            line = line.replace(closed_curly_braces, '')
    print(line)
