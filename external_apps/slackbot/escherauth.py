#code taken from https://github.com/emartech/escher-python and updated to python3

import datetime
import hmac
import requests
import urllib.request, urllib.parse, urllib.error
import re

from hashlib import sha256, sha512

try:
    from urllib.parse import urlparse, parse_qsl, urljoin
    from urllib.parse import quote
except:
    from urllib.parse import urlparse, parse_qsl, urljoin, quote


class EscherException(Exception):
    pass


class EscherRequestsAuth(requests.auth.AuthBase):
    def __init__(self, credential_scope, options, client):
        self.escher = Escher(credential_scope, options)
        self.client = client

    def __call__(self, request):
        return self.escher.sign(request, self.client)


class EscherRequest():
    _uri_regex = re.compile('([^?#]*)(\?(.*))?')

    def __init__(self, request):
        self.type = type(request)
        self.request = request
        self.prepare_request_uri()

    def request(self):
        return self.request

    def prepare_request_uri(self):
        if self.type is requests.models.PreparedRequest:
            self.request_uri = self.request.path_url
        if self.type is dict:
            self.request_uri = self.request['uri']
        match = re.match(self._uri_regex, self.request_uri)
        self.uri_path = match.group(1)
        self.uri_query = match.group(3)

    def method(self):
        if self.type is requests.models.PreparedRequest:
            return self.request.method
        if self.type is dict:
            return self.request['method']

    def host(self):
        if self.type is requests.models.PreparedRequest:
            return self.request.host
        if self.type is dict:
            return self.request['host']

    def path(self):
        return self.uri_path

    def query_parts(self):
        return parse_qsl((self.uri_query or '').replace(';', '%3b'), True)

    def headers(self):
        if self.type is requests.models.PreparedRequest:
            headers = []
            for key, value in self.request.headers.items():
                headers.append([key, value])
            return headers
        if self.type is dict:
            return self.request['headers']

    def body(self):
        if self.type is requests.models.PreparedRequest:
            return self.request.body or ''
        if self.type is dict:
            return self.request.get('body', '')

    def add_header(self, header, value):
        if self.type is requests.models.PreparedRequest:
            self.request.headers[header] = value
        if self.type is dict:
            self.request['headers'].append((header, value))


class AuthParams:
    def __init__(self, data, vendor_key):
        self._init_data(data, 'X-' + vendor_key + '-')

    def _init_data(self, data, prefix):
        self._data = {}
        for (k, v) in data:
            if k.startswith(prefix):
                self._data[k.replace(prefix, '').lower()] = v

    def get(self, name):
        if name not in self._data:
            raise EscherException('Missing authorization parameter: ' + name)
        return self._data[name]

    def get_signed_headers(self):
        return self.get('signedheaders').lower().split(';')

    def get_algo_data(self):
        data = self.get('algorithm').split('-')
        if len(data) != 3:
            raise EscherException('Malformed Algorithm parameter')
        return data

    def get_algo_prefix(self):
        return self.get_algo_data()[0]

    def get_hash_algo(self):
        return self.get_algo_data()[2].upper()

    def get_credential_data(self):
        data = self.get('credentials').split('/', 2)
        if len(data) != 3:
            raise EscherException('Malformed Credentials parameter')
        return data

    def get_credential_key(self):
        return self.get_credential_data()[0]

    def get_credential_date(self):
        return datetime.datetime.strptime(self.get_credential_data()[1], '%Y%m%d')

    def get_credential_scope(self):
        return self.get_credential_data()[2]

    def get_expires(self):
        return int(self.get('expires'))

    def get_request_date(self):
        return datetime.datetime.strptime(self.get('date'), '%Y%m%dT%H%M%SZ')


class AuthenticationValidator:
    def validate_mandatory_signed_headers(self, headers_to_sign):
        if 'host' not in headers_to_sign:
            raise EscherException('Host header is not signed')

    def validate_hash_algo(self, hash_algo):
        if hash_algo not in ('SHA256', 'SHA512'):
            raise EscherException('Only SHA256 and SHA512 hash algorithms are allowed')

    def validate_dates(self, current_date, request_date, credential_date, expires, clock_skew):
        if request_date.strftime('%Y%m%d') != credential_date.strftime('%Y%m%d'):
            raise EscherException('The request date and credential date do not match')

        min_date = current_date - datetime.timedelta(seconds=(clock_skew + expires))
        max_date = current_date + datetime.timedelta(seconds=clock_skew)
        if request_date < min_date or request_date > max_date:
            raise EscherException('Request date is not within the accepted time interval')

    def validate_credential_scope(self, expected, actual):
        if actual != expected:
            raise EscherException('Invalid credential scope (provided: ' + actual + ', required: ' + expected + ')')

    def validate_signature(self, expected, actual):
        if expected != actual:
            raise EscherException('The signatures do not match (provided: ' + actual + ', calculated: ' + expected + ')')


class Escher:
    _normalize_path = re.compile('([^/]+/\.\./?|/\./|//|/\.$|/\.\.$)')

    def __init__(self, credential_scope, options={}):
        self.credential_scope = credential_scope
        self.algo_prefix = options.get('algo_prefix', 'ESR')
        self.vendor_key = options.get('vendor_key', 'Escher')
        self.hash_algo = options.get('hash_algo', 'SHA256')
        self.current_time = options.get('current_time', datetime.datetime.utcnow())
        self.auth_header_name = options.get('auth_header_name', 'X-Escher-Auth')
        self.date_header_name = options.get('date_header_name', 'X-Escher-Date')
        self.clock_skew = options.get('clock_skew', 300)
        self.algo = self.create_algo()
        self.algo_id = self.algo_prefix + '-HMAC-' + self.hash_algo

    def sign(self, r, client, headers_to_sign=[]):
        request = EscherRequest(r)

        for header in [self.date_header_name.lower(), 'host']:
            if header not in headers_to_sign:
                headers_to_sign.append(header)

        signature = self.generate_signature(client['api_secret'], request, headers_to_sign, self.current_time)
        request.add_header(self.auth_header_name, ", ".join([
            self.algo_id + ' Credential=' + client['api_key'] + '/' + self.short_date(
                self.current_time) + '/' + self.credential_scope,
            'SignedHeaders=' + self.prepare_headers_to_sign(headers_to_sign),
            'Signature=' + signature
        ]))
        return request.request

    def authenticate(self, r, key_db):
        request = EscherRequest(r)

        auth_params = AuthParams(request.query_parts(), self.vendor_key)
        validator = AuthenticationValidator()

        validator.validate_mandatory_signed_headers(auth_params.get_signed_headers())
        validator.validate_hash_algo(auth_params.get_hash_algo())
        validator.validate_dates(
            self.current_time,
            auth_params.get_request_date(),
            auth_params.get_credential_date(),
            auth_params.get_expires(),
            self.clock_skew
        )
        validator.validate_credential_scope(self.credential_scope, auth_params.get_credential_scope())

        if auth_params.get_credential_key() not in key_db:
            raise EscherException('Invalid Escher key')

        calculated_signature = self.generate_signature(
            key_db[auth_params.get_credential_key()], request,
            auth_params.get_signed_headers(),
            auth_params.get_request_date()
        )
        validator.validate_signature(calculated_signature, auth_params.get('signature'))

        return auth_params.get_credential_key()

    def hmac_digest(self, key, message, is_hex=False):
        if not isinstance(key, bytes):
            key = key.encode('utf-8')
        digest = hmac.new(key, message.encode('utf-8'), self.algo)
        if is_hex:
            return digest.hexdigest()
        return digest.digest()

    def generate_signature(self, api_secret, req, headers_to_sign, current_time):
        canonicalized_request = self.canonicalize(req, headers_to_sign)
        string_to_sign = self.get_string_to_sign(canonicalized_request, current_time)

        signing_key = self.hmac_digest(self.algo_prefix + api_secret, self.short_date(current_time))
        for data in self.credential_scope.split('/'):
            signing_key = self.hmac_digest(signing_key, data)

        return self.hmac_digest(signing_key, string_to_sign, True)

    def canonicalize(self, req, headers_to_sign):
        return "\n".join([
            req.method(),
            self.canonicalize_path(req.path()),
            self.canonicalize_query(req.query_parts()),
            self.canonicalize_headers(req.headers(), headers_to_sign),
            '',
            self.prepare_headers_to_sign(headers_to_sign),
            self.algo(req.body().encode('utf-8')).hexdigest()
        ])

    def canonicalize_path(self, path):
        changes = 1
        while changes > 0:
            path, changes = self._normalize_path.subn('/', path, 1)
        return path

    def canonicalize_headers(self, headers, headers_to_sign):
        headers_list = []
        for key, value in iter(sorted(headers)):
            if key.lower() in headers_to_sign:
                headers_list.append(key.lower() + ':' + self.normalize_white_spaces(value))
        return "\n".join(sorted(headers_list))

    def normalize_white_spaces(self, value):
        index = 0
        value_normalized = []
        pattern = re.compile(r'\s+')
        for part in value.split('"'):
            if index % 2 == 0:
                part = pattern.sub(' ', part)
            value_normalized.append(part)
            index += 1
        return '"'.join(value_normalized).strip()

    def canonicalize_query(self, query_parts):
        safe = "~+!'()*"
        query_list = []
        for key, value in query_parts:
            if key == 'X-' + self.vendor_key + '-Signature':
                continue
            query_list.append(quote(key, safe=safe) + '=' + quote(value, safe=safe))
        return "&".join(sorted(query_list))

    def get_string_to_sign(self, canonicalized_request, current_time):
        return "\n".join([
            self.algo_id,
            self.long_date(current_time),
            self.short_date(current_time) + '/' + self.credential_scope,
            self.algo(canonicalized_request.encode('utf-8')).hexdigest()
        ])

    def create_algo(self):
        if self.hash_algo == 'SHA256':
            return sha256
        if self.hash_algo == 'SHA512':
            return sha512

    def long_date(self, time):
        return time.strftime('%Y%m%dT%H%M%SZ')

    def short_date(self, time):
        return time.strftime('%Y%m%d')

    def prepare_headers_to_sign(self, headers_to_sign):
        return ";".join(sorted(headers_to_sign))