"""
:authors: ALeDo
:license: Apache License, Version 2.0, see LICENSE file

:copyright: (c) 2023 ALeDo
"""

import json
import logging
import re
import time
import json
import aiohttp
import asyncio
from typing import Any, Union, Optional, List, Tuple
from .enums import (HttpReqigetTypes, ResponseCodes, )
from .exceptions import (AloHostError, MixiError, HttpMixiDxError, )

class AloHost():
    """
    :param alohost_api_token: - Alo Host API access token
    :param api_version: Current - Alo Host API version
    :return:
    """
    REQUEST_PER_SECOND_DELAY = 0.33 # ~ 3 request per second (REST API Limits requests to 200 minu)
    BASE_API_URL = 'https://api.alohost.io/api/'
    
    GET_REQUESTS_METHOD = re.compile(r'(get|history)$')
    POST_REQUESTS_METHOD = re.compile(r'(create|search|upload)')
    PUT_REQUESTS_METHOD = re.compile(r'(update|enable|disable)')
    DELETE_REQUESTS_METHOD = re.compile(r'delete$')
    
    def __init__(self, alohost_api_token:str, api_version:str='v3') -> None:
        self.alohost_api_token = alohost_api_token
        self.api_version = api_version
        self.last_request: float = 0.0
        self.lock: asyncio.Lock = asyncio.Lock()
        self.logger: logging.Logger = logging.getLogger('alohost_api')
        
    @property
    def full_api_url(self) -> str:
        """ Return full Alo Host API URL """
        return '{0}{1}/'.format(AloHost.BASE_API_URL, self.api_version)
    
    def get_api(self) -> 'AloHostMixiDx':
        """
        Return AloHostMixiDx(self)
        Allows you to access API methods as normal classes
        
        Example:
        >> ch.labels.get(...)
        """
        return AloHostMixiDx(self)
    
    async def _get_request_type(self, request_method:str) -> HttpReqigetTypes:
        """
        Defines HTTP request type by the method name
        
        :param request_method: - name of the requested method
        :return: - HTTP request type
        """
        if AloHost.GET_REQUESTS_METHOD.match(request_method): # GET Zapros
            return HttpReqigetTypes.GET 
        elif AloHost.POST_REQUESTS_METHOD.match(request_method): # POST Zapros
            return HttpReqigetTypes.POST 
        elif AloHost.PUT_REQUESTS_METHOD.match(request_method): # PUT Zapros
            return HttpReqigetTypes.PUT
        elif AloHost.DELETE_REQUESTS_METHOD.match(request_method): # DELETE Zapros
            return HttpReqigetTypes.DELETE
        else:
            self.logger.warning(f'Bad request: {request_method}')
            return HttpReqigetTypes.BAD_TYPE
        
    async def method(self, request:str, args:Optional[list], values:Optional[dict]) -> Optional[dict]:
        """
        Calling the API method

        :param request: - name of the requested API method
        :param args: - positional parameters of the API request
        :param values: - named API request parameters
        :return: - response to a request in json format
        :raise: - ApiError:  API request failed with status code 400, 422, 204 or 429
        """
        response: Optional[dict, aiohttp.ClientResponse] = None
        async with self.lock:
            request_delay = AloHost.REQUEST_PER_SECOND_DELAY - (time.time() - self.last_request)
            if request_delay > 0:
                await asyncio.sleep(request_delay)

            response = await self._do_request(request, args, values)
                
            self.last_request = time.time()
            self.logger.info(f'Last request: {self.last_request} Method: {request}')

        if response is not None:
            response_status_code: int = response.status
            if(response_status_code in ResponseCodes.OK.value):
                response: Optional[dict] = await response.json()
            elif response_status_code == ResponseCodes.TOO_MATCH_REQUEST:
                self.logger.warning('Too many requests! Sleeping 30 sec...')
                await asyncio.sleep(30)
                await self.method(request, args, values)
            else:
                self.logger.exception(f'Something go wrong: {response_status_code}, {request}')
                raise MixiError(await response.json(), response_status_code)
        return response

    async def _do_request(self, method_to_request:str, args:Optional[list], values:Optional[dict]) -> Optional[aiohttp.ClientResponse]:
        """
        Makes a request to the API

        :param method: - name of the requested API method
        :param args: - positional parameters of the API request
        :param values: - named API request parameters
        :return: - row response to a request
        :raise: - HttpMixiDxError: No such API method 
        """
        response: Optional[aiohttp.ClientResponse] = None
        base_api_requested_object, requested_method, additional_params, requested_method_type = await self._split_request(method_to_request, args)
        method_params_sep: str = '/' if additional_params else ''

        headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Alohost-Token': self.alohost_api_token
        }

        if requested_method == 'upload':
            values = {'file': open(json.loads(values)['file'], 'rb')}
        else:
            headers['Content-Type'] = 'application/json'
            
        async with aiohttp.ClientSession(headers=headers) as http:
            if requested_method_type == HttpReqigetTypes.GET: # GET-запрос 
                response = await http.get(self.full_api_url + base_api_requested_object + '{0}{1}'.format(method_params_sep, additional_params))
            elif requested_method_type == HttpReqigetTypes.POST: # POST-запрос
                response = await http.post(self.full_api_url + base_api_requested_object + '{0}{1}'.format(method_params_sep, additional_params), data=values)
            elif requested_method_type == HttpReqigetTypes.PUT: #PUT-запрос
                response = await http.put(self.full_api_url + base_api_requested_object + '{0}{1}'.format(method_params_sep, additional_params), data=values)
            elif requested_method_type == HttpReqigetTypes.DELETE: #Delete-запрос
                await http.delete(self.full_api_url + base_api_requested_object + '{0}{1}'.format(method_params_sep, additional_params))
            else:
                self.logger.exception(f'Something go wrong: {requested_method}')
                raise HttpMixiDxError('No such API method: {} '.format(requested_method))
            return response

    async def _split_request(self, request:str, args:Optional[list]) -> Tuple[str, str, str, HttpReqigetTypes]:
            """
            Split the request into several parts

            :param request: - name of the requested API method
            :param args: - positional parameters of the API request
            :return: - tuple of the obtained parts of the query

            Example:
                The request -- alo_host.stories.create(1, 'comments', 2) -- is divided into:
                    > method - stories
                    > request_method - create
                    > additional_param - 1/comments/2
            """
            base_api_requested_object: str = ''
            requested_method: str = ''
            additional_params: str = ''
            requested_method_type: Optional[HttpReqigetTypes] = None 

            parts_request = request.split('.')
            if (len(parts_request) == 1):
                base_api_requested_object = parts_request[0]
                requested_method_type = HttpReqigetTypes.GET
            else:
                base_api_requested_object, requested_method = parts_request
                if requested_method == 'search':
                    args += (requested_method,)
                requested_method_type = await self._get_request_type(requested_method)

            additional_params: str = '/'.join(list(map(str, args)))

            return base_api_requested_object, requested_method, additional_params, requested_method_type

class AloHostMixiDx():
    """
    Allows you to access API methods via:
    >>> ch.labels.get(...)
    """
    __slots__ = ('_alohost', '_method')

    def __init__(self, alohost:AloHost, method:Optional[str]=None) -> None:
        self._alohost = alohost
        self._method = method
    
    def _alternative_method_name(self, method:str) -> str:
        """
        Return converted the request name to an alternative form

        :param method: - name of the requested API method
        :return: - alternative form requested name
        """
        return method.lower().replace('_', '-')

    def __getattr__(self, method:str) -> 'AloHostMixiDx':
        return AloHostMixiDx(
            self._alohost, 
            (self._method + '.' if self._method else '') + self._alternative_method_name(method)
        )
        
    async def __call__(self, *args, **kwargs) -> aiohttp.ClientResponse:
        return await self._alohost.method(self._method, args, json.dumps(kwargs))  
