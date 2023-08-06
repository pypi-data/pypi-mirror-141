# Letesend Python

This is a python library for sending and monitoring SMS with [letesend](https://letesend.com/).
Letesend is a sms gateway that tries to make sms price cheaper, more information at [letesend.com](https://letesend.com/).


## Installation

Install using [pip](https://pypi.org/project/letesend/) with :

```sh
pip install letesend
```

## Example Usage

Go to [letesend.com/console](https://letesend.com/console) and copy your **auth token**. After installing, import **letesend** into your program and replace your **auth token**, see the code below.


```py
from letesend import SMS

AUTH_TOKEN  = "Replace_Your_Auth_Token_Here"
sms         = SMS(AUTH_TOKEN)

sms.send(
    to      = "+243xxxxxxxxx",
    name    = "Company",
    body    = "Hello World !"
)

if sms.ok:
    print('SMS processed successfully')

print(sms.status_code, sms.status_text)
```

**Output**

```py
SMS processed successfully
```

```py
201 {
    "id":5,
    "to":"+243xxxxxxxxx",
    "name":"Company",
    "body":"Hello World !",
    "status":"0",
    "date":"2022-03-05",
    "time":"11:57:28.357820"
}
```

**Troubleshoot**

```py
403 {
    'detail': 'Your balance (0.0$) is insufficient to send 1 SMS.'
}
```
It means you don't have enough money in your account For sending the SMS.
```py
400 {
    'to': ['The phone number entered is not valid.']
}
```
The phone number must a **E.164** format.


## Class Description

The SMS class description provides **methods** and **attributes** for sending and monitoring SMS.

### Methods

#### Send

Send sms with letesend gateway.

| Parameters  | Type | Description |
|-------------|------|-------------|
| to          | String  | The receiver phone number (E.164 format) |
| name        | String  | The name (will be displayed in the SMS header) |
| body        | Strimg  | The sms body (the message) |


### attributes

| Name  | Type | Description |
|-------------|------|-------------|
| id          | Integer| The unique sms indetification |
| to          | String | The receiver phone number (E.164 format)|
| name        | String | The name (will be displayed in the SMS header)|
| body        | String | The sms body (the message) |
| status      | String | The SMS status <br/> **0** : Processed <br/> **1** : Sent <br/> **2** : Queued <br/> **3** : Scheduled <br/> **4** : Undelivered <br/> **5** : Delivered <br/> **6** : Delivery_unknown <br/> **7** : Failed  |
| date        | String | The date the request was sent to our server |
| time        | String | The time the request was sent to our server |
| status_code | String | The http response status <br> **201**  : The SMS has successfully Processed <br/> **403**  : Can not send SMS for some reasons <br/> **400** : Bad Request|
| status_text | String | The http response details |
| ok          | Boolean| SMS processed successfully|
| auth_token  | String | The Authentication token. |

<br/>

More information at [letesend.com](https://letesend.com/) or contact us at  [support@letesend.com](mailto:support@letesend.com/)
