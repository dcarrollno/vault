#!/usr/bin/env python

import os
import json
import click
import shelve
import hvac
from hvac import exceptions


# This is a very fast export/import script to grab Vault secrets.
# We first build the secret list then use a callback to comb
# that list and store the secret name as the key, and json as the value.

def recurse(key):

    if key.endswith('/'):
        result = client.list(path=key)
        for x in result['data']['keys']:
            if x.endswith('/'):
                recurse(key+x)
            else:
                print(f'SECRET found at {x}')
                path = key+x
                print(f'Looking up secret at {path}')
                result=client.read(path)
                secret=(json.dumps(result['data']))
                s[path]=secret
    else:
        print(f'Looking up secret at {key}')
        result = client.read(key)
        secret=(json.dumps(result['data']))
        s[key]=secret


def backup_secrets():

    print(f"Backing up from {os.environ.get('VAULT_ADDR')}")
    all_secrets = client.list(path='secret')
    all_secret_keys = (all_secrets['data']['keys'])
    for key in all_secret_keys:
        recurse('secret/'+key)

    s.close()


def read_secrets_from_shelve():
    for key,value  in s.items():
        print(f'{k}\t{v}')


def write_secret_to_vault(k,v):

    print(f'Restoring {k}')
    result = client.write(k, **v)


def restore_secrets():

    for k,v in s.items():
        val=json.loads(v)
        write_secret_to_vault(k,val)


@click.command()
@click.option("-b", is_flag=True, help="backup Vault secrets to shelve")
@click.option("-r", is_flag=True, help="restore Vault secrets to Vault instance")

def main(b,r):
    """ Main Function """

    if b:
        backup_secrets()
    if r:
        restore_secrets()

if __name__=='__main__':
    client = hvac.Client()
    s = shelve.open("secrets_export.db")
    main()
