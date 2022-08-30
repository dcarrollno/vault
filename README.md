# Vault Secrets Exporter-Importer

This is a quick program to export the secrets from a Vault instance and save it locally to a shelve file.
You can then restore the secrets from the shelve file to a new Vault instance, thereby creating a migration.
This can also be used as a backup engine for your secrets but you may want to include encryption beyond say
your cloud storage functionality. 

Future improvements could include encrypting the shelve file on disk but I will defer that work for now.

## Running the export
```
export VAULT_ADDR=<your vault address>
export VAULT_TOKEN=<your vault token>
./vault_backup.py -b
```
A resulting shelve file named secrets_export.db will be created. Be careful to not allow this file to be accessible
to anyone and keep it secure until you delete it. 

## Restoring Vault Secrets
```
export VAULT_ADDR=<target_vault_address>
export VAULT_TOKEN=<target_vault_token>
./vault_backup.py -r 
```

