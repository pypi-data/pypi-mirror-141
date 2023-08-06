import requests

class SMS:
    """
    Letesend sdk for sending and monitoring SMS
    """

    url = "https://apis.letesend.com/sms/"


    def __init__(self, auth_token, debug=False):
        self.auth_token  = auth_token
        self.debug       = debug
        self.status_code = ''
        self.status_text = ''


    def headers(self):
        """
        Http Request Headers
        """
        return {
            'Authorization': 'Token {}'.format(self.auth_token)
        }


    def __setResponse(self, response):
        """
        Set server response to object attributes
        """
        self.status_code = response.status_code
        self.status_text = response.text


    def is_debug(self, *args):
        """
        Logging if debug mode is True.
        e.g. in development
        """
        if self.debug:
            #Logging
            pass


    def send(self, to=None, name='LeteSend', body='Hello World !'):
        """
        Send SMS
        --------
        @to: Phone Number E.164 format
        @name: Company name, will be display on SMS Header
        @body: The Message body, 160 caracteres per SMS
        """

        payload = {
            "to"  : to,
            "name": name,    
            "body": body
        }

        #self.is_debug("\nSending SMS ...")

        response = requests.request(
            method  = "POST", 
            url     = self.url, 
            headers = self.headers(), 
            data    = payload)

        #self.is_debug(response.status_code, response.text)
        self.__setResponse(response)

        return response
