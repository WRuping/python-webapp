#!/usr/bin/env python
#_*_ coding: utf-8 _*_

__author__ = 'LYleonard'
'''
JSON API definition.
'''
import re, json, logging, functools

from transwarp.web import ctx

class Page(object):
    '''
    Page object for display pages.
    '''
    def __init__(self, item_count, page_index=1, page_size=10):
        '''
        Init Pagination by item_count, page_index, page_size.
        :param item_count:
        :param page_index:
        :param page_size:
        '''
        self.item_count = item_count
        self.page_size = page_size
        self.page_count = item_count // page_size + (1 if item_count % page_size else 0)
        if (item_count == 0) or (page_size < 1) or (page_index > self.page_count):
            self.offset = 0
            self.limit = 0
            self.page_index = 1
        else:
            self.page_index = page_index
            self.offset = self.page_size * (page_index - 1)
            self.limit = self.page_size
        self.has_next = self.page_index < self.page_count
        self.has_previous = self.page_index > 1

    def __str__(self):
        return 'item_count: %s, page_count: %s, page_index: %s, page_size: %s, offset: %s, limit: %s' % (self.item_count, self.page_count, self.page_index, self.page_size, self.offset, self.limit)

    __repr__ = __str__

def _dump(obj):
    if isinstance(obj, Page):
         return {
            'page_index': obj.page_index,
             'page_count': obj.page_count,
            'item_count': obj.item_count,
            'has_next': obj.has_next,
            'has_previous': obj.has_previous
         }
    raise TypeError('%s is not JSON serializable' % obj)


def dumps(obj):
    return json.dumps(obj)

class APIError(StandardError):
    '''
    The APIError which contains error(required), data(option) and message(option).
    '''
    def __init__(self, error, data='', message=''):
        super(APIError,self).__init__(message)
        self.error = error
        self.data = data
        self.message = message

class APIValueError(APIError):
    '''Indicate the input value has error or invalid. The data specifies the error field of input form.'''
    def __init__(self, field, message=''):
        super(APIValueError, self).__init__('value:invalid', field, message)

class APIResourceNotFoundError(APIError):
    '''Indicate resource was not found. The data specifies the resource name'''
    def __init__(self, field, message=''):
        super(APIResourceNotFoundError, self).__init__('value:notfound', field, message)

class APIPermissionError(APIError):
    '''Indicate the api has no permission'''
    def __init__(self, message=''):
        super(APIPermissionError, self).__init__('permission:forbidden', 'permission', message)

def api(func):
    '''
    A decorator that that make a function to json api, makes the return value as json.
    @api.route('/api/test')
    @api
    def api_test():
        return dict(result='123', items=[])
    '''
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        try:
            r = dumps(func(*args, **kw))
        except APIError, e:
            r = json.dumps(dict(error=e.error, data=e.data, message=e.message))
        except Exception, e:
            logging.exception(e)
            r = json.dumps(dict(error='internalerror', data=e.__class__.__name__, message=e.message))
        ctx.response.content_type = 'application/json'
        return r
    return _wrapper

if __name__=='__main__':
    import doctest
    doctest.testmod()