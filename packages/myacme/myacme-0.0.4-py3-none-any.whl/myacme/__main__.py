'''
Command-line ACME client
========================

Account creation
----------------

Before applying to certificate issuance you need an account on ACME server.

The following command would generate private key and create an account::

    myacme create account ak=my-account-key.pem

However, if my-account-key.pem already exists (in case you have already generated it
with `openssl`, for example) this command would use your existing key.

By default ACME server is Let's Encrypt https://acme-v02.api.letsencrypt.org/directory
You can specify your own server by providing its directory URL::

    myacme create account ak=my-account-key.pem acme=https://my.acme.com/directory

Or, you can use a predefined URL::

    myacme create account ak=my-account-key.pem acme=le-staging

where ``le-staging`` is a directory URL for Let's Encrypt staging environment.

Optionally you can provide one or more emails for your account::

    myacme create account ak=my-account-key.pem email=john.doe@example.com email=sarah.connor@example.com

If you run this command for an existing account it will change contact emails.


Update account
--------------

Change account key::

    myacme update account ak=my-account-key.pem new-ak=new-account-key.pem

New account key may already exist. If not, will be generated::

    myacme update account ak=my-account-key.pem email=john.doe@example.com

The above can be done with a single command.

Account deactivation
--------------------

If you no longer need an account you can deactivate it::

    myacme deactivate account ak=my-account-key.pem

You can specify other ACME server with `acme` parameter, see Account creation.


Manually applying for certificate issuance
------------------------------------------

If you already have a CSR, you can get the certificate with a single command::

    myacme certificate ak=my-account-key.pem csr=my-csr.pem cert=my-cert.pem

You'll have to prove you own your domain. This command will print instructions how to do that.

If you got a temporary error, such as network error or server error, you can run the above command repeatedly.
The state of appliance process is saved to a file <domain-name>.myacme.json in the current directory.

If you don't have a CSR but do have already generated private key (with `openssl` command, for example),
``myacme`` will automatically generate a CSR for the issuance process::

    myacme certificate ak=my-account-key.pem dom=example.com dom=www.example.com private-key=my-key.pem cert=my-cert.pem

The CSR will be saved only in the state filename, you can extract it with `myacme get csr` command (see below).

Finally, if you have neither CSR, nor private key, `myacme` will generate everything for you::

    myacme certificate ak=my-account-key.pem dom=example.com dom=www.example.com private-key=my-key.pem cert=my-cert.pem

Yes, this is exactly the same command as above. This simply checks your ``my-key.pem`` and if it does not exist,
the key will be automatically generated and written to that file.


Automatic certificate management
--------------------------------

XXX in progress

Initialize certificate management environment::

    myacme init dir=/etc/myacme

This command will create /etc/myacme directory (if it does not yet exist), all
subdirectories, basic configuration files, and an account.

You can provide more details with the following statements in any order:

* ACME server, if you don't want default Let's Encrypt: acme=https://my.acme.com/directory
* existing account key: ak=my-account-key.pem
* contact emails: email=john.doe@example.com email=sarah.connor@example.com

Add managed certificate::

    myacme add dir=/etc/myacme dom=example.com dom=www.example.com template=nginx

This will create a subdirectory ``/etc/myacme/example.com`` and copy configuration files
from ``/etc/myacme/templates/nginx``
You need to revise configuration and set ``active`` parameter to true in XXX

The following command should be run daily::

    myacme manage dir=/etc/myacme

This will check certificates and apply for re-issuance for expiring ones.

Is root access necessary for automatic certificate management?
Basically, no. If file permissions are properly set, say, if myacme can put certificates to a subdirectory
under ``/etc/nginx``, root access is obviously not required. However, nginx should be restarted after changing
certificate, but this is what ``sudo`` is for.
It's up to the user how to set up things properly.


Utility commands
----------------

Extract private key from state file example.com.myacme.json to my-key.pem::

    myacme get state=example.com.myacme.json private-key=my-key.pem

This works only if private key was generated automatically.

Extract certificate from state file example.com.myacme.json to my-key.pem::

    myacme get state=example.com.myacme.json cert=my-certificate.pem

This works only if certificate was successfully issued.

You can get everything with one command::

    myacme get state=example.com.myacme.json private-key=my-key.pem cert=my-certificate.pem

Authorization scripts
---------------------

XXX

``myacme-zonefile``

'''

predefined_directory_urls = {
    'le':         'https://acme-v02.api.letsencrypt.org/directory',
    'le-staging': 'https://acme-staging-v02.api.letsencrypt.org/directory'
}

def main():
    try:
        if len(kvgargs.group) == 0:
            print(__doc__)
            sys.exit(0)

        action, args = kvgargs.group.popitem(last=False)

        # get directory URL
        if 'acme' in args:
            directory_url = args['acme']
            if directory_url in predefined_directory_urls:
                directory_url = predefined_directory_urls[directory_url]
        else:
            # use Let's Encrypt by default
            directory_url = predefined_directory_urls['le']

        # create ACME client
        acme = MyAcmeClient(directory_url)

        # run action handler
        action_handlers = {
            ('create', 'account'): create_account,
            ('update', 'account'): update_account,
            ('deactivate', 'account'): deactivate_account,
            'certificate': certificate_issuance,
            'init': initialize_managed_dir,
            'add': add_managed_certificate,
            'manage': manage_certificates,
            'get': get_data_from_saved_state
        }
        if action not in action_handlers:
            print('Wrong action requested:', action if isinstance(action, str) else ' '.join(action), file=sys.stderr)
            sys.exit(1)

        handler = action_handlers[action]
        exit_code = handler(acme, args)
        sys.exit(exit_code)

    except MyAcmeHttpError as e:
        print(e.status, e.error_type, e.detail, file=sys.stderr)
        sys.exit(1)
    except Exception:
        print(traceback.format_exc(), file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(1)

#-----------------------------------------------------------------------------------
# Accounts

def create_account(acme, args):
    if 'ak' not in args:
        print('Account key is required: ak=<filename>', file=sys.stderr)
        return 1
    account_key_filename = args['ak']
    account_key = _load_or_generate_account_key(acme, account_key_filename)
    acme.account_key = account_key

    contacts = _prepare_contacts(args)

    acme.create_account(contacts)
    print('Account created')
    print(acme.account_url)
    return 0

def update_account(acme, args):
    account_key = _load_account_key(args)
    if account_key is None:
        return 1
    acme.account_key = account_key

    if 'new-ak' in args:
        # change account key
        new_account_key_filename = args['new-ak']
        new_account_key = _load_or_generate_account_key(acme, new_account_key_filename)
        acme.change_account_key(new_account_key)
        print('Account key changed')

    if 'email' in args:
        # change contacts
        contacts = _prepare_contacts(args)
        print('Changing contacts not implemented yet', file=sys.stderr)
        return 1

    return 0

def deactivate_account(acme, args):
    account_key = _load_account_key(args)
    if account_key is None:
        return 1
    acme.account_key = account_key
    acme.deactivate_account()
    print('Account deactivated')
    return 0

#-----------------------------------------------------------------------------------
# Manual certificate issuance

def certificate_issuance(acme, args):
    if 'cert' not in args:
        print('Certificate file name is required for output: cert=<filename>', file=sys.stderr)
        return 1

    account_key = _load_account_key(args)
    if account_key is None:
        return 1
    acme.account_key = account_key

    domains = []
    csr = None
    private_key = None

    if 'csr' in args:
        # load csr and get domain names from it
        csr_filename = args['csr']
        if not os.path.exists(csr_filename):
            print('CSR file does not exist:', csr_filename, file=sys.stderr)
            return 1

        if 'dom' in args:
            print('Reading domain names from provided CSR:', csr_filename, file=sys.stderr)
            print('Ignoring provided domin names:', ', '.join(args['dom']), file=sys.stderr)

        with open(csr_filename, 'rb') as f:
            csr = f.read()

        domains = acme.get_domains_from_csr(csr)

    else:
        if 'dom' not in args:
            print('Please provide domain name or names: dom=example.com', file=sys.stderr)
            return 1

        domains = args['dom']

        if 'private-key' not in args:
            print('Please private key file name: private-key=<filename>', file=sys.stderr)
            print('If <filename> already exists, private key will be loaded from that file.', file=sys.stderr)
            print('Otherwise, it will be generated and stored to that file.', file=sys.stderr)
            return 1

        private_key_filename = args['private-key']
        if os.path.exists(private_key_filename):
            with open(private_key_filename, 'rb') as f:
                private_key = f.read()

    authenticator = MyAcmeAuthzManual()
    order = MyAcmeOrderFS(acme, domains, authenticator, directory='.', csr=csr, private_key=private_key)
    status = order.process_order()
    if status == 'failed':
        print('Failed getting certificate.', file=sys.stderr)
        return 1

    if not private_key:
        private_key = order.get_private_key()
        with open(private_key_filename, 'wb') as f:
            f.write(private_key)

    certificate_filename = args['cert']
    certificate = order.get_certificate()
    with open(certificate_filename, 'wb') as f:
        f.write(certificate)

#-----------------------------------------------------------------------------------
# Managed certificate issuance

def initialize_managed_dir(acme, args):
    pass

def add_managed_certificate(acme, args):
    pass

def manage_certificates(acme, args):
    pass

#-----------------------------------------------------------------------------------
# Utilities

def get_data_from_saved_state(acme, args):
    pass

#-----------------------------------------------------------------------------------
# Helpers

def _load_or_generate_account_key(acme, account_key_filename):
    '''
    Helper function for create account or change account key.
    '''
    if os.path.exists(account_key_filename):
        # load existing account key
        with open(account_key_filename, 'rb') as f:
            account_key = f.read()
    else:
        # generate account key
        account_key = acme.generate_account_key()
        with open(account_key_filename, 'wb') as f:
            f.write(account_key)
    return account_key

def _load_account_key(args):
    '''
    Helper function for account action handlers and certificate issuance.
    '''
    if 'ak' not in args:
        print('Account key is required: ak=<filename>', file=sys.stderr)
        return None
    # check account key
    account_key_filename = args['ak']
    if not os.path.exists(account_key_filename):
        print('Account key file does not exist:', account_key_filename, file=sys.stderr)
        return None
    # load account key
    with open(account_key_filename, 'rb') as f:
        return f.read()

def _prepare_contacts(args):
    '''
    Helper function for create account or change account contacts
    '''
    contacts = args.get('email', [])
    if not isinstance(contacts, list):
        contacts = [contacts]
    return ['mailto:' + email for email in contacts]

#-----------------------------------------------------------------------------------
# Dependencies

import os
import sys
import traceback

import kvgargs

from .client import MyAcmeClient, MyAcmeOrderFS, MyAcmeAuthzManual, MyAcmeHttpError

#-----------------------------------------------------------------------------------
# Run main

if __name__ == '__main__':
    main()

#-----------------------------------------------------------------------------------
# Copyright 2021 AXY axy@declassed.art
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software without
#    specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
