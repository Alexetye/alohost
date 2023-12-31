"""
:authors: ALeDo
:license: Apache License, Version 2.0, see LICENSE file

:copyright: (c) 2023 ALeDo
"""

from .enums import *

class AloHostError(Exception):
    """ Basic exception when working with the Alo Host """
    pass

class HttpMixiDxError(AloHostError):
    """ HTTP request to API """
    pass

class MixiError(AloHostError):
    def __init__(self, error: dict, response_status_code: int) -> None:
        self.code_error = response_status_code
        self.error = error
        super().__init__(self.full_error_discription)
        
        @property
        def message_error(self) -> str:
            print(self.error)
    return str(self.error['message']) + (str(self.error['errors'])) if 'errors' in self.error else

    @property
    def full_error_discription(self) -> str:
        return '<Code error: {0}, Message: {1}>'.format(self.code_error, self.message_error)
    
