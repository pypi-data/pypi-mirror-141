from .include import length_check
import string as _string ## Function string is defined in code
import random
import secrets
import warnings

#### 0123456789
digits = _string.digits

#### Return random integer value
def integer(length:int=6, prefix:int=None, ignore_max_length:bool=False):

    #### Check if specified length is allowed
    length_check(length, ignore_max_length) ## Will fail if returns True

    #### Prefix should be of type int
    if not isinstance(prefix, int):
        if not prefix == None:
            raise TypeError('Prefix should be of type int')
    
    generated = ""
    
    #### Create random integer
    c = length
    while not c == 0:
        cur_random_int = random.choice(digits)
        if not int(cur_random_int) == 0: ## If an integer starts with 0 the 0 will be ignored
            generated += ''.join(cur_random_int)
            c -= 1

    generated = int(generated)

    #### Add prefix
    if not prefix == None:
        generated = int(str(prefix) + str(generated)) ## Workaround with int and str functions TODO clean up
        
    return generated

#### Return random string value
def string(length:int=6, prefix:str=None, ignore_max_length:bool=False, type:str="all", 
            uppercase_only=False, lowercase_only=False):

    #### ! depricated since 0.1.6, will be removed in v1.0.0
    if type == "integer":
        type = "number"
        warnings.warn("Type 'integer' has been depricated since version 0.1.6, please use type 'number'. The 'integer' type will be removed in 'v1.0.0'", DeprecationWarning, stacklevel=2)
    
    #### Check if specified length is allowed
    length_check(length, ignore_max_length) ## Will fail if returns True

    #### Prefix should be of type str
    if not isinstance(prefix, str):
        if not prefix == None:
            raise TypeError('Prefix should be of type str')

    #### String can't be both uppercase only and lowercase only
    if uppercase_only and lowercase_only:
        raise ValueError('A string can not be uppercase only and lowercase only at the same time')

    #### Check if 'type' is 'integer'
    if type == "number":
        generated = str(integer(length=length)) ## Why write duplicate code?
    else:

        #### Check for upperscase_only or lowercase_only
        alphabet = _string.ascii_uppercase if uppercase_only else _string.ascii_lowercase if lowercase_only else _string.ascii_letters

        choices = alphabet + _string.digits if type == "all" else alphabet if type == "letter" else _string.digits
        generated = ''.join(secrets.choice(choices) for i in range(length))

    if not prefix == None:
        generated = prefix + generated

    return str(generated)

def password(length:int=10, ignore_max_length:bool=False):

    #### Check if specified length is allowed
    length_check(length, ignore_max_length) ## Will fail if returns True

    alphabet = _string.ascii_letters + _string.digits ## Returns abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(length))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break

    return password

#### Generate random byte string (Basicly a wrapper for secrets.token_bytes)
def bytes(length:int=32, ignore_max_length:bool=False):

    #### Check if specified length is allowed
    length_check(length, ignore_max_length) ## Will fail if returns True

    return secrets.token_bytes(length)

#### Generate a random text string in hexadecimal (Basicly a wrapper for secrets.token_hex)
def hex(length:int=32, ignore_max_length:bool=False):

    #### Check if specified length is allowed
    length_check(length, ignore_max_length) ## Will fail if returns True

    return secrets.token_hex(length)

def urlsafe(*args, length:int=32, ignore_max_length:bool=False):

    #### Check if specified length is allowed
    length_check(length, ignore_max_length) ## Will fail if returns True

    #### Generate
    generated = secrets.token_urlsafe(length)

    #### Check if 'padding' is defined in 'args'
    if 'padding' in args:
        generated  += '=' ## Padding is useful when using for encryption

    #### Check if 'encoded' is defined in 'args'
    if 'encoded' in args:
        generated  = generated.encode()

    return generated

#### Secrets function is depricated but will wrap around 'bytes', 'hex' and 'urlsafe' functions
def secret(*args, length:int=32, type:str='bytes', ignore_max_length:bool=False): #### ! depricated since 0.1.6, will be removed in v1.0.0

    #### Throw warning
    warnings.warn("The 'secrets' function has been depricated since version 0.1.6 and it will be removed in version 1.0.0. Use seperate 'bytes', 'hex' and 'urlsafe' functions instead", DeprecationWarning, stacklevel=2)

    #### Call the right function
    if type == "bytes":
        return bytes(length=length, ignore_max_length=ignore_max_length)
    elif type == "hex":
        return hex(length=length, ignore_max_length=ignore_max_length)
    elif type == "urlsafe":
        return urlsafe(*args, length=length, ignore_max_length=ignore_max_length)
    else:
        raise Exception('Unable to generate a secret key of type {}'.format(type))

#### Check database cursor
def database(cursor, *args, **kwargs):
    
    #### Default method is string
    if not "method" in kwargs:
        method = "string"
    else:
        method = kwargs['method']
        del kwargs['method'] ## Kwargs need to be passed to generation functions, method is useless here

    #### Generate new until 'id_exists' becomes False
    id_exists = True
    while id_exists:

        #### Generate
        generated_id = string(*args, **kwargs) if method == 'string' else integer(*args, **kwargs) if method == 'integer' else None

        #### Check if it appears in the database
        cursor['cursor'].execute('SELECT "{}" FROM {} WHERE {} = "{}"'.format(cursor['column'], cursor['table'], cursor['column'], generated_id))
        if not len(cursor['cursor'].fetchall()):
            id_exists = False

    return generated_id
