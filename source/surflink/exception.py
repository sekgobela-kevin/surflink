
class URLError(Exception):
    '''Erros related to urls'''
    pass

class NotExistsError(Exception):
    '''Something required is missing'''

class TagNotExists(NotExistsError):
    '''Tag does not exists in html or xml document'''
    pass

class BaseUrlNotExists(NotExistsError):
    '''Base url is required but missing'''
    pass