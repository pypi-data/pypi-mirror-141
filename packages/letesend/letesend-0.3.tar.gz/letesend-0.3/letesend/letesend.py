import requests

class SMS:
    """
    Letesend sdk for sending and monitoring SMS
    """

    url = "https://apis.letesend.com/sms/"


    def __init__(self, auth_token, debug=False):
        self.id          = ''
        self.to          = ''
        self.name        = ''
        self.body        = ''
        self.status      = ''
        self.date        = ''
        self.time        = ''
        self.status_code = ''
        self.status_text = ''
        self.ok          = False
        self.auth_token  = auth_token
        self.debug       = debug


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
        self.status_text = response.json()
        self.ok = response.ok
        if self.ok:
            try:
                self.id = response.json()['id']
                self.to = response.json()['to']
                self.name = response.json()['name']
                self.body = response.json()['body']
                self.status = response.json()['status']
                self.date = response.json()['date']
                self.time = response.json()['time']
            except:
                pass


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
