'''
ACME client library
===================

This is an ACME client library based on ``requests`` and ``cryptography`` packages.

This library is written from scratch by studying https://tools.ietf.org/html/rfc8555
and trying out Let's Encrypt staging and production environments.

This library automates all aspects of certificate issuance, including
generating keys and CSRs, and checking certificate expiration.

This means there's no need to manually invoke ``openssl`` and any other commands,
the only exception is domain validation instructions displayed by ``MyAcmeAuthzManual``.
However, you can provide your own private key for account and certificates,
and your own CSRs in PEM format.

This library provides basic client classes for ACME, as well as "batteries included" stuff:

* ``MyAcmeClient``:      the main class provides account management and basic methods for ACME requests

* ``MyAcmeOrderABC``:    this abstract class implements certificate issuance state mashine

* ``MyAcmeOrderFS``:     this subclass implements saving the state of certificate issuance to file system

* ``MyAcmeAuthzABC``:    this abstract class defines methods for setting up and cleaning up domain validation

* ``MyAcmeAuthzManual``: this implementation prints instructions for domain validation and waits for user input

* ``MyAcmeAuthzScript``: this class invokes scripts for domain validation according to provided configuration

* ``MyAcmeError``:       basic exception

* ``MyAcmeHttpError``:   ACME HTTP exception

A helper function ``get_certificate_validity_period`` returns certificate dates not_valid_before and not_valid_after,
which can be used to check certificate expiration.

How to use
----------

The first step is to instantiate ``MyAcmeClient`` class with a directory URL::

    my_acme = MyAcmeClient('https://acme-v02.api.letsencrypt.org/directory')

To apply for certificates, you should have an account on the ACME server.
The account is identified by client's public key.
The account is identified ONLY by client's public key. Contact emails are optional.

If you have no account key yet, there's a method to generate it for you::

    account_key = my_acme.generate_account_key()

The ``account_key`` is a key pair, containing both public and private keys
in PEM format, as bytes. You should permanently save the account key somewhere::

    with open('my-account-key.pem', 'wb') as f:
        f.write(account_key)

If you aleady have an account key, you should set it explicitly::

    with open('my-account-key.pem', 'rb') as f:
        my_acme.account_key = f.read()

or provide it to ``MyAcmeClient``::

    with open('my-account-key.pem', 'rb') as f:
        my_account_key = f.read()
    my_acme = MyAcmeClient('https://acme-v02.api.letsencrypt.org/directory', my_account_key)

Once ``account_key`` is set, you can create an account on the ACME server, if it was not created yet::

        acme.create_account()

This method can accept the list of contact URLs in the form "mailto:admin@example.org".
By default contacts is an empty list.

It's desirable to permanently save account URL, along with account key somewhere::

    saved_account_url = my_acme.account_url

This is because this URL is needed for subsequent requests and if not saved,
the client has to issue extra request to obtain it.

This URL should be restored after instantiation of ``MyAcmeClient``::

    my_acme.account_url = saved_account_url


How to apply for certificate issuance
-------------------------------------

After setting up the client, you should create an instance of some ``MyAcmeOrderABC`` subclass.
The library only provides ``MyAcmeOrderFS``, which stores state to a file, but if you have
better ideas you can be more creative.

``MyAcmeOrderABC`` needs an authenticator to validate domains. The simplest one is ``MyAcmeAuthzManual``
which simply prints instructions and waits for your confirmations.

So, the first step is to create an authenticator::

    authenticator = MyAcmeAuthzManual()

Then, create an instance of order::

    my_order = MyAcmeOrderFS(my_acme, 'example.com', authenticator, directory='.')

You can provide your own private key or CSR::

    my_order = MyAcmeOrderFS(my_acme, 'example.com', authenticator, csr=example_com_csr, directory='.')
    my_order = MyAcmeOrderFS(my_acme, 'example.com', authenticator, private_key=example_com_key, directory='.')

Private key is unnecessary if you provide your CSR because CSR is already signed.

Then, try to process the order::

    my_order.process_order()

Normally, ``process_order`` returns completion status as string, either "complete" or "failed".
In case of error, network error, for example, it raises an exception.
In this case you should repeat ``process_order`` until it returns completion status.

When ``process_order`` has successfully completed, call ``get_certificate`` method to obtain your certificate.
You should save it somewhere, obviously::

    certificate = my_order.get_certificate()

    with open('my-certificate.pem', 'wb') as f:
        f.write(certificate)


Internationalized domain names
------------------------------

MyACME accepts and returns all domain names as strings so they may contain non-ASCII characters.
Domain names are internally encoded and decoded as necessary.


The complete example
--------------------

::

    my_domain = 'example.com'
    with open('my-account-key.pem', 'rb') as f:
        my_account_key = f.read()
    my_acme = MyAcmeClient('https://acme-v02.api.letsencrypt.org/directory', my_account_key)
    authenticator = MyAcmeAuthzManual()
    my_order = MyAcmeOrderFS(my_acme, my_domain, authenticator, directory='.')
    my_order.process_order()
    certificate = my_order.get_certificate()
    with open('my-certificate.pem', 'wb') as f:
        f.write(certificate)

'''

__all__ = [
    'MyAcmeClient',
    'MyAcmeError',
    'MyAcmeHttpError',
    'MyAcmeOrderABC',
    'MyAcmeOrderFS',
    'MyAcmeAuthzABC',
    'MyAcmeAuthzManual',
    'MyAcmeAuthzScript',
    'get_certificate_validity_period'
]

class MyAcmeError(Exception):
    pass

class MyAcmeHttpError(MyAcmeError):

    def __init__(self, response):
        self.status = response.status_code
        try:
            payload = response.json()
            self.error_type = payload.get('type', '')
            self.detail = payload.get('detail', '')
        except Exception:
            self.error_type = ''
            self.detail = ''

class MyAcmeClient:

    #----------------------------------------------------------
    # Defaults

    rsa_key_size = 4096

    #----------------------------------------------------------
    # Initialization

    def __init__(self, directory_url, account_key=None):
        '''
        Initialize the instance of client object and, if account_key argument
        is provided, set account key.
        If account_key argument is not provided, the user should set the key
        explicitly before using calling client methods.
        '''
        self._directory_url = directory_url
        self._acme_directory = None  # cached value, see acme_directory property
        self._account_key = None     # placeholder, see account_key property
        self._account_url = None     # cached value, see account_url property
        self._replay_nonce = None    # placeholder, the value will be initialized on first request

        if account_key:
            self.account_key = account_key

    @property
    def acme_directory(self):
        '''
        The directory object, as returned by ACME server.
        '''
        if not self._acme_directory:
            response = requests.get(self._directory_url, headers=self._make_request_headers())
            if response.status_code // 100 != 2:
                raise MyAcmeHttpError(response)
            self._acme_directory = response.json()
        return self._acme_directory

    #----------------------------------------------------------
    # Account management

    @property
    def account_key(self):
        '''
        Get or set private key for ACME account.

        Setting account URL is a mandatory initialization task.
        This can be done by ``__init__`` if `account_key` argument is provided.
        Otherwise, the user should set the key explicitly before calling other methods.

        Account key is mandatory for ACME protocol. Even the account does not yet exist, the user
        should set account key to be able to call ``create_account`` method.

        The format for the key is PEM.
        '''
        return private_key_to_pem(self._account_key)

    @account_key.setter
    def account_key(self, account_key):
        self._account_key = private_key_from_pem(account_key)
        # reset cached account url
        self._account_url = None

    def generate_account_key(self):
        '''
        Generate private key for ACME account.

        Returns:
            bytes: private key in PEM format
        '''
        private_key = rsa.generate_private_key(
            public_exponent = 65537,
            key_size =  self.rsa_key_size
        )
        return private_key_to_pem(private_key)

    @property
    def account_url(self):
        '''
        Account URL is returned by ACME newAccount call and cached internally.
        This URL is required for many methods, so it's desirable to save it after account creation.
        Otherwise an extra call to ACME server will be issued to obtain this URL.
        This may break nonce sequence. Therefore, this property should be accessed BEFORE getting a nonce.

        This URL is reset in the following cases:
        * account key is set
        * account is deactivated
        '''
        if not self._account_url:
            response = self._new_account(only_return_existing=True)
            self._account_url = response.headers.get('Location', None)
        return self._account_url

    @account_url.setter
    def account_url(self, account_url):
        self._account_url = account_url

    def create_account(self, contact=[]):
        '''
        Create new account or update existing one.

        The user should set account key before calling this method.

        Contacts by default is an empty list. Contacts are OPTIONAL for ACME protocol.
        If the user, for example, generates a certificate for an email server TLS,
        this implies no contact email is available yet.

        Args:
            contact (list): contact URLs, in the form "mailto:admin@example.org"

        Returns:
            str: URL for the account. This URL is cached for subsequent requests.
        '''
        response = self._new_account(contact=contact)
        self._account_url = response.headers['Location']
        return self._account_url

    def get_account_status(self):
        '''
        Returns:
            account status (valid/deactivated/revoked), None if account does not exist
        '''
        try:
            response = self._new_account(only_return_existing=True)
        except MyAcmeHttpError as e:
            if e.status == 403:
                # deactivated or nonexistent
                return False
            elif e.error_type == 'urn:ietf:params:acme:error:accountDoesNotExist':
                return False
            else:
                raise
        payload = response.json()
        return payload['status']

    def change_account_key(self, new_account_key):
        '''
        Account key rollover. Set new account key for this object on success.
        Before calling this function ``new_account_key`` should be saved somewhere to avoid losing it on failure.
        '''
        old_account_key = self._account_key
        new_account_key = private_key_from_pem(new_account_key)

        account_url = self.account_url  # mind nonce sequence
        nonce = self._nonce

        # prepare inner JWS object
        old_key = {
            'protected': {
                'url': self.acme_directory['keyChange']
            },
            'payload': {
                'account': account_url,
                'oldKey': jwk_public(old_account_key)
            }
        }
        signed_old_key = jws(old_key, new_account_key)

        request = {
            'protected': {
                'nonce': nonce,
                'url': self.acme_directory['keyChange'],
                'kid': account_url
            },
            'payload': signed_old_key
        }
        signed_request = jws(request, self._account_key)
        self._post_as_get(self.acme_directory['keyChange'], signed_request)
        self._account_key = new_account_key

    def deactivate_account(self):
        '''
        Deactivate account.
        '''
        account_url = self.account_url  # mind nonce sequence
        nonce = self._nonce
        request = {
            'protected': {
                'nonce': nonce,
                'url': account_url,
                'kid': account_url
            },
            'payload': {
                'status': 'deactivated'
            }
        }
        signed_request = jws(request, self._account_key)
        self._post_as_get(account_url, signed_request)
        self._account_url = None

    #----------------------------------------------------------
    # Utilities

    def get_domains_from_csr(self, csr):
        '''
        Extract domain names from CSR.

        Args:
            csr: CSR as bytes

        Returns:
            list: domain names as unicode strings
        '''
        xxx
        idna_decode()

    #----------------------------------------------------------
    # Helpers

    @property
    def _nonce(self):
        if not self._replay_nonce:
            self._replay_nonce = self._get_nonce()
        return self._replay_nonce

    def _get_nonce(self):
        '''
        Get new nonce value from ACME server.
        '''
        response = requests.head(self.acme_directory['newNonce'], headers=self._make_request_headers())
        if response.status_code != 200:
            raise MyAcmeHttpError(response)
        return response.headers['Replay-Nonce']

    _user_agent = 'MyACME alpha'

    def _make_request_headers(self, headers=None):
        return {
            'User-Agent': self._user_agent,
            **(headers or {})
        }

    def _post_as_get(self, url, signed_request):
        '''
        Issue POST-as-GET request.
        '''
        post_data = indented_json(signed_request)
        request_headers = self._make_request_headers({'Content-Type': 'application/jose+json'})
        self._replay_nonce = None  # drop used nonce, just in case of requests.post failure
        response = requests.post(url, headers=request_headers, data=post_data)
        self._replay_nonce = response.headers['Replay-Nonce']
        print('=====', url)
        print(response.headers)
        print(response.content)
        if response.status_code // 100 != 2:
            raise MyAcmeHttpError(response)
        return response

    def _simple_request(self, url, payload):
        '''
        Shorthand wrapper for typical requests.
        '''
        account_url = self.account_url  # mind nonce sequence
        nonce = self._nonce
        request = {
            'protected': {
                'nonce': nonce,
                'url': url,
                'kid': account_url
            },
            'payload': payload
        }
        signed_request = jws(request, self._account_key)
        return self._post_as_get(url, signed_request)

    def _new_account(self, contact=[], only_return_existing=False):
        '''
        Send newAccount request.
        This is a helper for account management methods.
        '''
        request = {
            'protected': {
                'nonce': self._nonce,
                'url': self.acme_directory['newAccount']
            },
            'payload': {
                'termsOfServiceAgreed': True,
                'contact': contact,
                'onlyReturnExisting': only_return_existing
            }
        }
        signed_request = jws(request, self._account_key)
        response = self._post_as_get(self.acme_directory['newAccount'], signed_request)
        return response

    #----------------------------------------------------------
    # Helpers for MyAcmeOrder

    def _new_order(self, domains):
        '''
        Issue newOrder request.

        There's no way to get the list of orders for Let's Encrypt, at least.
        However, repeated newOrder request with same parameters returns same URLs.
        '''
        response = self._simple_request(
            self.acme_directory['newOrder'],
            {'identifiers': [{'type': 'dns', 'value': idna_encode(domain_name)} for domain_name in domains]}
        )
        payload = response.json()
        payload['__order_url__'] = response.headers['Location']  # https://www.rfc-editor.org/errata/eid5979
        return payload

    def _get_order(self, order_url):
        '''
        Issue request to order_url.
        '''
        # XXX as of time of writing neither RFC8555 nor its errata specify the format of payload
        #     which seems to be emptty string, not {}
        response = self._simple_request(order_url, '')
        payload = response.json()
        payload['__order_url__'] = order_url
        return payload

    def _authz_status(self, authz_url):
        '''
        Issue request for authorization URL, as returned by ``newOrder`` request.
        '''
        # XXX Retry-After is not supported
        # https://github.com/letsencrypt/boulder/blob/master/docs/acme-divergences.md
        response = self._simple_request(authz_url, '')
        return response.json()

    def _challenge(self, challenge_url):
        '''
        Respond to challenge_url to start authorization.
        '''
        response = self._simple_request(challenge_url, {})
        return response.json()

    def _finalize(self, finalize_url, csr):
        '''
        Send CSR to finalize_url.
        '''
        response = self._simple_request(finalize_url, {'csr': csr})
        return response.json()

    def _download_certificate(self, certificate_url):
        response = self._simple_request(certificate_url, '')
        return response.content

class MyAcmeOrderABC:
    '''
    MyAcmeOrderABC implements state machine to apply for certificate issuance.
    State machine implies tracking the state somehow. This class declares two abstract methods
    `load_state` and `save_state`.

    See ``MyAcmeOrderFS`` that implements these methods to permanently save state to a file.

    To apply for certificate issuance the user should call `process_order` method.
    Normally, this method returns completion status as string, either 'complete' or 'failed'.
    In case of error, network error, for example, it raises an exception.
    In such a case it should be called again.

    This class generates private key and CSR if the user does not provide them.
    If the user provides CSR, private key is unnecessary for certificate issuance.
    If the user provides private key but does not provide a CSR, the CSR will be generated automatically.
    If the user provides neither CSR, nor private key, both will be auto-generated.

    By default, auto-generated CSR contains only COMMON_NAME field and, optionally SAN extension.
    That's sufficient to get a certificate from Let's Encrypt, at least.

    To add more fields the user can add entries to ``csr_data`` dictionary::

        my_order.csr_data['Country Name'] = 'US'
        my_order.csr_data['State or Province Name'] = 'California'

    and so on.

    Field names are transformed to x509 names by converting them to upper case and replacing spaces
    with underscores. The following statements are also okay, therefore::

        my_order.csr_data['country name'] = 'US'
        my_order.csr_data['STATE OR PROVINCE_NAME'] = 'California'

    Here are most used names, for the full list see ``cryptography.x509.oid.NameOID``.

    COUNTRY_NAME             2-letter country code
    LOCALITY_NAME            e.g. city
    STATE_OR_PROVINCE_NAME
    STREET_ADDRESS
    ORGANIZATION_NAME        e.g. company
    ORGANIZATIONAL_UNIT_NAME e.g. section
    EMAIL_ADDRESS
    '''

    retry_delay_min = 5   # seconds
    retry_delay_max = 60  # seconds

    def __init__(self, client, domains, authenticator, private_key=None, csr=None, **kwargs):
        '''
        Args:
            client: an instance of ``MyAcmeClient`` class
            domains: domain name or list of domain names
            authenticator: an instance of ``MyAcmeAuthzABC`` subclass
            private_key (bytes): private key for the certificate in PEM format. If not provided, the key will be generated.
                                 Private key is unnecessary if CSR is provided, so this argument will not be used.
            csr (bytes): CSR in PEM format. if not provided, the CSR will be generated. In this case private key is required.
        '''
        self.client = client
        self.domains = [domains] if isinstance(domains, str) else domains
        self.authenticator = authenticator
        self._custom_private_key = private_key_from_pem(private_key) if private_key else None
        self._custom_csr = csr_from_pem(csr) if csr else None
        self.csr_data = dict()

    def load_state(self):
        '''
        Load certificate issuance state and private key.

        Returns:
            state data in JSON as bytes or None if the state is not defined yet, (i.e. the order is new)
        '''
        raise NotImplementedError('MyAcmeOrderABC.load_state is an abstract method. Use a subclass which implements it.')

    def save_state(self, order_state):
        '''
        This method should save order state.

        Args:
            order_state (bytes): state data in JSON
        '''
        raise NotImplementedError('MyAcmeOrderABC.save_state is an abstract method. Use a subclass which implements it.')

    def delay(self, seconds):
        '''
        The user can override this method to add logging.
        '''
        time.sleep(seconds)

    def process_order(self):
        '''
        Returns:
            str: status of processing: complete or failed
        '''
        # initialize state
        state = self.load_state()
        if state:
            self._state = json.loads(state)
            if self._state['state'] in ['complete', 'failed']:
                # previous order complete, start new one
                self._state = dict(state='new')
        else:
            # no saved state, start new order
            self._state = dict(state='new')

        # run state machine
        while self._state['state'] not in ['complete', 'failed']:
            next_method, next_states = self._get_transition()
            next_method = getattr(self, next_method)
            new_state = next_method()
            if new_state not in next_states:
                raise MyAcmeError(f'Internal error: bad new state {new_state}')
            self._state['state'] = new_state

            # save state after each transition
            state = indented_json(self._state)
            self.save_state(state)

        return self._state['state']

    def get_certificate(self):
        '''
        Get issued certificate.
        This method should be called after ``process_order`` returns "complete".

        Returns:
            certificate, as bytes, or None if ``process_order`` is not complete
        '''
        if self._state.get('certificate', None):
            return self._state['certificate'].encode('ascii')
        else:
            return None

    def get_private_key(self):
        '''
        Get auto-generated private key.
        Such a key is saved in state object.

        Returns:
            private key in PEM format as bytes or None if the key was not generated,
            i.e. the user provided the key or CSR
        '''
        if self._state.get('private_key', None):
            return self._state['private_key'].encode('ascii')
        else:
            return None

    _transitions = {
        # current state    transition method    possible next states, returned by transition method
        'new':             ('_new_order',       ('authorization', 'failed', 'complete', 'finalization', 'wait-issuance')),
        'authorization':   ('_authorization',   ('finalization', 'authorization', 'failed')),
        'finalization':    ('_finalization',    ('failed', 'complete', 'wait-issuance', 'download-cert')),
        'wait-issuance':   ('_wait_issuance',   ('download-cert', 'failed', 'complete', 'wait-issuance')),
        'download-cert':   ('_download_cert',   ('complete', ))
        # terminal states: complete, failed
    }

    def _get_transition(self):
        '''
        Get transition entry for current state.
        '''
        state = self._state['state']
        if state not in self._transitions:
            raise MyAcmeError(f'Internall error: bad state {state}')
        return self._transitions[state]

    def _rate_limit_delay(self, identifier):
        '''
        Calculate delay value from number of attempts and delay execution by calling ``self.delay``.

        Args:
            identifier: name of the data structure in ``self._state``
        '''
        now = time.time()
        data = self._state.setdefault(identifier, {'attempt': 0, 'delay_start': now})
        data['attempt'] += 1
        # calculate delay_end from previous delay_start
        data['delay_end'] = data['delay_start'] + min((data['attempt'] - 1) * self.retry_delay_min, self.retry_delay_max)
        data['delay_start'] = now
        # calculate period from current time and delay_end
        seconds = data['delay_end'] - now
        if seconds > 0.0:
            self.delay(max(1.0, seconds))

    def _new_order(self):
        '''
        Issue new order request.
        '''
        order = self.client._new_order(self.domains)
        # If an order already exists, Let's Encrypt returns it in response to newOrder request.
        # The returned order has "ready" status. For some reason, subsequent finalize
        # fails with orderNotReady error.
        # Extra request to get the order fixes the problem.
        order = self.client._get_order(order['__order_url__'])
        self._state['order'] = order
        return self._make_new_state(order['status'])

    def _make_new_state(self, order_status):
        '''
        Map order status to new state.
        '''
        if order_status == 'pending':
            # the order is awaiting authorization
            return 'authorization'
        if order_status == 'ready':
            # the order has passed authorization
            return 'finalization'
        if order_status == 'processing':
            # certificate issuance is still in progress
            return 'wait-issuance'
        if order_status == 'valid':
            # certificate has been issued
            return 'download-cert'
        if order_status == 'invalid':
            # the order is cancelled, expired, or CSR is invalid
            return 'failed'

        raise MyAcmeError(f'ACME protocol error: bad order status {order_status}')

    def _authorization(self):
        '''
        Check statuses of authorizations and process pending ones.
        '''
        order = self._state['order']
        authz_statuses = self._state.setdefault('authz_statuses', dict())

        self._rate_limit_delay('authz_rate_limit')

        valid_authorizations = 0
        invalid_authorizations = 0
        for authz_url in order['authorizations']:

            if authz_url in authz_statuses:
                # use saved status
                authz_status = authz_statuses[authz_url]
            else:
                # get new authz status
                authz_status = self.client._authz_status(authz_url)
                authz_statuses[authz_url] = authz_status

            # check if status already valid for this authz_url
            if authz_status['status'] == 'valid':
                valid_authorizations += 1
                continue

            # check if challenge already sent
            if '__challenge_sent__' in authz_status:
                if authz_status['status'] == 'pending':
                    # update status
                    print('Checking authz status for', authz_url)
                    challenge_sent = authz_status['__challenge_sent__']  # propagate this value to new status
                    authz_status = self.client._authz_status(authz_url)
                    authz_statuses[authz_url] = authz_status
                    authz_status['__challenge_sent__'] = challenge_sent

                if authz_status['status'] == 'valid':
                    valid_authorizations += 1
                elif authz_status['status'] == 'invalid':
                    invalid_authorizations += 1

                continue

            # challenge is not sent yet
            # collect authorization methods and parameters
            authz_params = dict()  # {challenge_type: {token: ..., key: ..., key_digest: ...}}
            challenge_urls = dict()
            for challenge in authz_status['challenges']:
                key_authz = challenge['token'] + '.' + thumbprint_public(self.client._account_key)
                key_digest = sha256_base64url(key_authz.encode('ascii'))
                authz_params[challenge['type']] = {
                    'token': challenge['token'],
                    'key': key_authz,
                    'key_digest': key_digest
                }
                challenge_urls[challenge['type']] = challenge['url']

            # setup authorization
            # note: validation_method is an alias for challenge_type
            domain = idna_decode(authz_status['identifier']['value'])
            validation_method_applied = self.authenticator.setup_domain_validation(domain, authz_params)
            # issue challenge request to start authorization
            chal_url = challenge_urls[validation_method_applied]
            print('Sending challenge request for', chal_url)
            self.client._challenge(chal_url)
            authz_status['__challenge_sent__'] = {
                'url': chal_url,
                'type': validation_method_applied,
                'params': authz_params[validation_method_applied]
            }

        # check if all authorizations are valid
        if len(order['authorizations']) == valid_authorizations:
            # cleanup validation
            try:
                for authz_status in authz_statuses.values():
                    if '__challenge_sent__' in authz_status:
                        domain = idna_decode(authz_status['identifier']['value'])
                        validation_method_applied, authz_params = authz_status['__challenge_sent__']
                        self.authenticator.cleanup_domain_validation(domain, validation_method_applied, authz_params)
            except Exception:
                pass
            return 'finalization'

        # check if all authorizations are invalid
        elif len(order['authorizations']) == invalid_authorizations:
            # Let's Encrypt does not implement the ability to retry challenges:
            # https://github.com/letsencrypt/boulder/blob/master/docs/acme-divergences.md#section-82
            # Return state based on order status, which, definitely, is failed.
            # We could return failed without getting order, just do this for the record in the saved state.
            print('Authorization failed')
            order = self.client._get_order(order['__order_url__'])
            self._state['order'] = order
            return self._make_new_state(order['status'])

        else:
            # not all authorizations are valid yet, try again
            return 'authorization'

    def _finalization(self):
        '''
        All authorizations have passed, upload CSR to finalize URL
        '''
        if self._custom_csr:
            # CSR is provided by user
            csr = base64url(self._custom_csr)
        else:
            # will generate CSR
            # need a private key for signing CSR
            if self._custom_private_key:
                # private key is provided by user
                private_key = self._custom_private_key
            else:
                # generate private key
                private_key = rsa.generate_private_key(
                    public_exponent = 65537,
                    key_size = self.client.rsa_key_size
                )
                self._state['private_key'] = private_key_to_pem(private_key).decode('ascii')
            # generate CSR
            csr = self._generate_csr(private_key)

        finalize_url = self._state['order']['finalize']
        order = self.client._finalize(finalize_url, csr)
        self._state['order'] = order
        return self._make_new_state(order['status'])

    def _wait_issuance(self):
        '''
        Poll the order URL.
        '''
        self._rate_limit_delay('order_rate_limit')
        order = self.client._get_order(self._state['order']['__order_url__'])
        self._state['order'] = order
        return self._make_new_state(order['status'])

    def _download_cert(self):
        '''
        Download certificate from ACME server.
        '''
        certificate_url = self._state['order']['certificate']
        self._state['certificate'] = self.client._download_certificate(certificate_url).decode('ascii')
        return 'complete'

    def _generate_csr(self, private_key):
        '''
        Generate CSR.
        '''
        # instantiate CSR builder
        builder = x509.CertificateSigningRequestBuilder()

        # prepare list of NameOID attributes
        name_list = [
            x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, idna_encode(self.domains[0]))
        ]
        for name, value in self.csr_data.items():
            name = '_'.join(re.split('[ _]+', name.upper()))
            if name == 'COMMON_NAME':
                # already defined, avoid overriding
                continue
            if not hasattr(x509.oid.NameOID, name):
                raise MyAcmeError(f'Bad CSR field name {name}')
            name_list.append(x509.NameAttribute(getattr(x509.oid.NameOID, name), value))

        builder = builder.subject_name(x509.Name(name_list))

        # add SAN extension for multiple domains
        if len(self.domains) > 1:
            san = x509.SubjectAlternativeName([x509.DNSName(idna_encode(domain)) for domain in self.domains])
            builder = builder.add_extension(san, critical=False)

        # build CSR
        request = builder.sign(private_key, hashes.SHA256())
        csr = request.public_bytes(serialization.Encoding.DER)
        return base64url(csr)

class MyAcmeOrderFS(MyAcmeOrderABC):
    '''
    This subclass implements saving state to file system.

    The order is identified by primary domain name, which is the first name in the ``domains`` list.
    The state is saved to file:

        directory/example.com.myacme.json
    '''
    def __init__(self, client, domains, authenticator, directory=None, **kwargs):
        super().__init__(client, domains, authenticator, **kwargs)
        self.directory = directory

    def load_state(self):
        if not os.path.exists(self.state_filename):
            return None
        with open(self.state_filename, 'rb') as f:
            return f.read()

    def save_state(self, order_state):
        # atomically replace the state
        with self.create_temp_file() as temp_file:
            temp_file.write(order_state)
            temp_filename = temp_file.name
        os.replace(temp_filename, self.state_filename)

    def filename_from_primary_domain(self, suffix=''):
        return self.domains[0].lower().replace('*', 'STAR') + suffix

    def create_temp_file(self):
        return tempfile.NamedTemporaryFile(prefix=self.filename_from_primary_domain('.'), dir=self.directory, delete=False)

    @property
    def state_filename(self):
        if not hasattr(self, '_state_filename'):
            self._state_filename = os.path.join(self.directory, self.filename_from_primary_domain('.myacme.json'))
        return self._state_filename

class MyAcmeAuthzABC:
    '''
    Authorization interface to validate domain.
    '''
    def setup_domain_validation(self, domain, authz_params):
        '''
        This method is called for all available challenge types methods for ``domain``.

        Args:
            domain: domain name for which to setup validation
            authz_params (dict): {challenge_type: {token: ..., key: ..., key_digest: ...}}

        Returns:
            str: applied validation method, i.e. challenge_type, http-01, dns-01, etc.
        '''
        raise NotImplementedError('MyAcmeAuthzABC.setup_domain_validation is an abstract method. '
                                  'Use a subclass which implements it.')

    def cleanup_domain_validation(self, domain, validation_method, authz_params):
        '''
        This method should remove files or DNS records or other data used for domain validattion.

        Args:
            domain: domain name for which to cleanup validation
            validation_method: the method used for validation as returned by setup_domain_validation.
            authz_params: parameters for specific validation method, i.e. {token: ..., key: ..., key_digest: ...}
        '''
        raise NotImplementedError('MyAcmeAuthzABC.cleanup_domain_validation is an abstract method. '
                                  'Use a subclass which implements it.')

class MyAcmeAuthzManual(MyAcmeAuthzABC):
    '''
    Print instructions how to setup validation and wait for user input.
    '''
    def setup_domain_validation(self, domain, authz_params):
        available_methods = []
        if 'dns-01' in authz_params:
            available_methods.append('dns-01')
            params = authz_params['dns-01']
            print()
            print(f'=== How to set up dns-01 validation for {domain} ===')
            print('Create the following TXT record:')
            print(f"_acme-challenge.{idna_encode(domain)}. 300 IN TXT \"{params['key_digest']}\"")
        if 'http-01' in authz_params:
            available_methods.append('http-01')
            params = authz_params['http-01']
            print()
            print(f'=== How to set up http-01 validation for {domain} ===')
            print(f"Write the following value to {domain}/.well-known/acme-challenge/{params['token']}")
            print(params['key'])
        if len(available_methods) == 0:
            if len(authz_params) == 0:
                raise MyAcmeError('No domain validation methods are provided')
            else:
                raise MyAcmeError(f'Domain validation methods {", ".join(sorted(authz_params.keys()))} are not supported')
        print()
        while True:
            for validation_method in available_methods:
                s = input(f'Use {validation_method} (y/n)?')
                if s.lower().strip() == 'y':
                    return validation_method

    def cleanup_domain_validation(self, domain, validation_method, authz_params):
        if validation_method == 'dns-01':
            print()
            print(f"Please remove TXT record _acme-challenge.{idna_encode(domain)}. 300 IN TXT \"{authz_params['key_digest']}\"")
            input('Press ENTER when done')
        elif validation_method == 'http-01':
            print()
            print(f"Please remove static file {domain}/.well-known/acme-challenge/{authz_params['token']}")
            input('Press ENTER when done')

class MyAcmeAuthzScript(MyAcmeAuthzABC):
    '''
    Invoke scripts for setting up/cleaning up validation.

    Configuration example::

        {
            # configuration for all domains
            'all': {
                'dns-01': {
                    'setup':   'myacme-zonefile /etc/bind/master/{domain} add {resource_record} ; rndc reload {domain}',
                    'cleanup': 'myacme-zonefile /etc/bind/master/{domain} del {resource_record} ; rndc reload {domain}'
                },
                'http-01': {
                    'setup':   'echo {key} >/var/www/{domain}/.well-known/acme-challenge/{token}',
                    'cleanup': 'rm /var/www/{domain}/.well-known/acme-challenge/{token}'
                }
            },

            # configuration for specific domains
            'example.com': {
                'http-01': {
                    'setup':   'echo {key} >/mnt/www-root/{domain}/.well-known/acme-challenge/{token}',
                    'cleanup': 'rm /mnt/www-root/{domain}/.well-known/acme-challenge/{token}'
                }
            },
            '*.example.com': {
                'dns-01': {
                    'setup':   'myacme-zonefile /etc/bind/{domain} add {resource_record} ; rndc reload {domain}',
                    'cleanup': 'myacme-zonefile /etc/bind/{domain} del {resource_record} ; rndc reload {domain}'
                }
            }
        }

    Keys other than 'http-01' and 'dns-01' are ignored, i.e. actual configuration may also include 'install' command.

    Substitutions, shell-escaped:

    * domain:     primary domain name, wildcard part is stripped

    * token:      domain validation token

    * key:        domain validation key for http-01

    * key_digest: domain validation key digest for dns-01

    * resource_record: domain validation resource record for dns-01

    '''
    def __init__(self, config):
        '''
        Args:
            config (dict): configuration object
        '''
        self.config = config

    def setup_domain_validation(self, domain, authz_params):
        # get authenticators for domain
        # authenticators: {domain|all: {http-01|dns-01: MyAcmeAuthz}}
        if domain in self.authenticators:
            # get authenticators for specific domain
            authenticators = self.authenticators[domain]
        elif 'all' in self.authenticators:
            # get authenticator for all domains
            authenticators = self.authenticators[domain]
        else:
            raise MyAcmeError(f'No authenticators provided for {domain}')

        # get available validation methods
        validation_methods = sorted(set(authz_params.keys()).intersection(set(authenticators.keys())))
        if not validation_methods:
            raise MyAcmeError(f"No suitable validation methods provided for {domain}: "
                              f"needed {', '.join(sorted(authz_params.keys()))}; "
                              f"provided {', '.join(sorted(authenticators.keys()))}")

        # run authenticators for available validation methods
        # 1. call prerequisites methods
        for method in validation_methods:
            authenticator = authenticators[method]
            authenticator.prerequisites(method, domain, **authz_params)
        # 2. call setup methods
        for method in validation_methods:
            authenticator = authenticators[method]
            if authenticator.setup(method, domain, **authz_params):
                return method
        raise MyAcmeError(f'Failed setting up validation for {domain}')

#-----------------------------------------------------------------------------------
# Helper functions

def get_certificate_validity_period(cert_bytes):
    '''
    Get dates from the certificate between which it is valid.

    Args:
        cert_bytes: certificate in PEM format

    Returns:
        tuple: (not_valid_before, not_valid_after), datetime, UTC, inclusive.
    '''
    cert = x509.load_pem_x509_certificate(cert_bytes)
    return (cert.not_valid_before, cert.not_valid_after)

def base64url(b):
    '''
    https://tools.ietf.org/html/rfc4648#section-5
    The function accepts bytes and returns string, to simplify typical use cases.
    '''
    return base64.urlsafe_b64encode(b).replace(b'=', b'').decode('ascii')

def sha256_base64url(b):
    '''
    Calculate SHA256 hash of bytes and return an ASCII string in base64url format.
    The function accepts bytes and returns string, to simplify typical use cases.
    '''
    return base64url(hashlib.sha256(b).digest())

def indented_json(value):
    '''
    Serialize value to indented JSON.
    Indented JSON is used for most ACME requests.

    Returns:
        bytes: serialized value in UTF-8
    '''
    return json.dumps(value, sort_keys=True, indent=4).encode('utf-8')

def compact_json(value):
    '''
    Serialize value to compact JSON.
    Compact JSON is used for key thumbprints.

    Returns:
        bytes: serialized value in UTF-8
    '''
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode('utf-8')

def private_key_to_pem(private_key):
    '''
    Convert private key to PEM format, as bytes.
    '''
    return private_key.private_bytes(
        encoding = serialization.Encoding.PEM,
        format = serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm = serialization.NoEncryption()
    )

def private_key_from_pem(key_bytes):
    '''
    Return private key object from `key_bytes` in PEM format.
    '''
    return serialization.load_pem_private_key(key_bytes, None)

def csr_to_pem(csr):
    '''
    Convert CSR to PEM format, as bytes.
    '''
    return csr.public_bytes(csr, serialization.Encoding.PEM)

def csr_from_pem(csr_bytes):
    '''
    Return CSR object from `csr_bytes` in PEM format.
    '''
    return x509.load_pem_x509_certificate(csr_bytes)

def jws(request, private_key):
    '''
    Build signed request.
    https://tools.ietf.org/html/rfc7515
    '''
    # make a copy of protected header to modify
    protected = request['protected'].copy()

    # set algorithm and key fields
    # TODO set these fields depending on private key class?
    protected['alg'] = 'RS256'
    if 'kid' not in protected:
        protected['jwk'] = jwk_public(private_key)

    # encode protected headers and payload
    protected = base64url(indented_json(protected))
    if request['payload'] == '':
        # somewhat strange, but empty string should produce empty string
        # i.e. if we encoded empty string in normal way, it would look as IiI which stands for ""
        payload = ''
    else:
        payload = base64url(indented_json(request['payload']))

    # calculate signature
    signing_input = '.'.join((
        protected,
        payload
    ))
    signature = private_key.sign(signing_input.encode('ascii'), padding.PKCS1v15(), hashes.SHA256())

    # prepare output
    signed_request = {
        'signature': base64url(signature),
        'protected': protected,
        'payload': payload
    }
    return signed_request

def jwk_public(private_key):
    '''
    Make JWK representation of public key.
    '''
    public_numbers = private_key.public_key().public_numbers()
    return {
        'kty': 'RSA',
        'e': base64url(cryptography.utils.int_to_bytes(public_numbers.e)),
        'n': base64url(cryptography.utils.int_to_bytes(public_numbers.n))
    }

def thumbprint_public(private_key):
    '''
    Make thumbpring of public key.
    https://tools.ietf.org/html/rfc8555#section-8.1

    Returns:
        str: thumbprint of public key
    '''
    # make JWK representation of public key
    key = jwk_public(private_key)
    # encode to compact JSON
    key = compact_json(key)
    # compute thumbprint
    return sha256_base64url(key)

def idna_encode(domain):
    '''
    Encode domain name to ASCII representation in IDNA encoding.
    '''
    # encode each part except stars
    parts = ['*' if part == '*' else idna.encode(part).decode('ascii') for part in domain.split('.')]
    return '.'.join(parts)

def idna_decode(domain):
    '''
    Decode domain name from IDNA.
    '''
    # decode each part except stars
    parts = ['*' if part == '*' else idna.decode(part) for part in domain.split('.')]
    return '.'.join(parts)

#-----------------------------------------------------------------------------------
# Dependencies

import base64
import json
import hashlib
import os
import re
import tempfile
import time

import idna
import requests

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography import x509
import cryptography.utils

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
