
# Name: akv-secrets

### Description: The python script is used to read a template file, fetches the relative secrets from primary and common Azure Key Vaults while finally rendering a configuration file with substituted values.

#### Note: This python script/tool is in it's early stages of development.


<br>

## Getting Started

### Pre-requisites: 
- Azure Subscription
- Azure Resource Group
- Azure Key Vault with Secrets
- Azure Service Principal account information (App Client ID, Client Secret and Tenant ID) to authenticate with
- Access Policy Permissions (LIST, GET) for the Service Principal on the Azure Key Vaults (Primary and Common)
- Python3 and python-pip3 packages installed


<br>

### References:
Documentation can be found on Azure Key Vault using the Python Azure SDK library [here](https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/keyvault/azure-keyvault-secrets).

<br>

If you don't currently have an Azure Key Vault with Secrets already provisioned along with a Service Principal with access to the AKV Vault, you can create those resources to demonstrate how this script would work. (See below)

<br>

### (Optional): Preparing the Azure Environment Resources
#### NOTE: Be sure to replace any variables with strings enclosed in <angle brackets>.
```
RESOURCE_GROUP_NAME='<my-resource-group-name-here>'
PRIMARY_AKV_VAULT_NAME='<my-primary-akv-vault-name-here>'
COMMON_AKV_VAULT_NAME='<my-common-akv-vault-name-here>'
SP_ACCOUNT_NAME='<my-service-principal-name-here>'

az ad sp create-for-rbac --name $SP_ACCOUNT_NAME --skip-assignment

export AZURE_CLIENT_ID="<PASTE_SP_APP_ID_HERE>"

az keyvault create --name $COMMON_AKV_VAULT_NAME --location eastus --resource-group $RESOURCE_GROUP_NAME
az keyvault set-policy --name $COMMON_AKV_VAULT_NAME --spn $AZURE_CLIENT_ID --secret-permissions get list

az keyvault create --name $PRIMARY_AKV_VAULT_NAME --location eastus --resource-group $RESOURCE_GROUP_NAME
az keyvault set-policy --name $PRIMARY_AKV_VAULT_NAME --spn $AZURE_CLIENT_ID --secret-permissions get list

# Example Secrets with "Common" Values within the Common AKV Vault
az keyvault secret set --vault-name $COMMON_AKV_VAULT_NAME --name resource-group --value dev-resource-group
az keyvault secret set --vault-name $COMMON_AKV_VAULT_NAME --name subscription-id --value common-87654321-4321-4321-4321-987654321
az keyvault secret set --vault-name $COMMON_AKV_VAULT_NAME --name tenant-id --value common-12345678-1234-1234-1234-123456789
az keyvault secret set --vault-name $COMMON_AKV_VAULT_NAME --name user-password --value common-S3c47P@$$w0rd!

# Example Secrets with "Regional Overide" Values within the Primary AKV Vault
az keyvault secret set --vault-name $PRIMARY_AKV_VAULT_NAME --name resource-group --value dev-us-resource-group
az keyvault secret set --vault-name $PRIMARY_AKV_VAULT_NAME --name subscription-id --value dev-us-87654321-4321-4321-4321-987654321
az keyvault secret set --vault-name $PRIMARY_AKV_VAULT_NAME --name tenant-id --value dev-us-12345678-1234-1234-1234-123456789
az keyvault secret set --vault-name $PRIMARY_AKV_VAULT_NAME --name user-password --value dev-us-S3c47P@$$w0rd!
```


<br>

### Initializing the Python Runtime Environment
#### NOTE: Initialize the Python Environment, run the following commands (Tested on Centos 7):
```
yum install -y python3-pip

pip3 install --upgrade setuptools pip
pip3 install virtualenv

virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
```


<br>

### Running the Python Script
#### NOTE: Ensure you have set the following environment variables as the Default Azure Credentials for the Service Principal
```
export AZURE_CLIENT_ID="<GENERATED_APP_ID>"
export AZURE_CLIENT_SECRET="<GENERATED_PASSWORD>"
export AZURE_TENANT_ID="<TENANT_ID>"

pip3 install -r requirements.txt
python3 akv-secrets.py <Template-Filename> <PRIMARY_AKV_VAULT_NAME> <COMMON_AKV_VAULT_NAME>
```


<br>

## Working Example
```
# Install Required Packages
yum install -y python3-pip

pip3 install --upgrade setuptools pip
pip3 install virtualenv


# Activate VirtualEnv Environment
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate


# Set Environment Variables
export AZURE_CLIENT_ID="<GENERATED_APP_ID>"
export AZURE_CLIENT_SECRET="<GENERATED_PASSWORD>"
export AZURE_TENANT_ID="<TENANT_ID>"

pip3 install -r requirements.txt

python3 akv-secrets.py 'sample.txt' 'my-akv-vault' 'my-akv-common'
```