# Letesend Python


```py
from letesend import SMS

AUTH_TOKEN  = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
sms         = SMS(AUTH_TOKEN)

sms.send(
    to      = "+243842779630",
    name    = "Company",
    body    = "Hello World !"
)

print(sms.status_code, sms.status_text)
```
