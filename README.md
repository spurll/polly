polly
=====

A simple website polling tool that polls a website until it changes.

Requirements:
  * [requests](http://docs.python-requests.org/en/latest/index.html)

basic usage
-----------
To Run:
```
python polly.py ADDRESS
```

By default, the tool polls every 60 seconds. To adjust the polling time use the ```--delay``` argument
```
python polly.py ADDRESS --delay TIME_IN_SECONDS
```

Unless silenced using the ```--silence``` flag, polly will write an alert to stdout every time it runs

Unless modified using the ```--eternal``` flag, polly will quit upon detecting a change

email
-----
Polly can email you when polling is finished.

To add an address to email, use the ```--mail``` argument.
```
python polly.py ADDRESS --mail EMAIL
```
The flag can be added multiple times:
```
python polly.py ADDRESS --mail EMAIL --mail ANOTHER_EMAIL
```

The SMTP host used is google's, unless an alternative is provided with the ```--host`` argument

Username and password can be entered securely in a prompt, or using the ```--user``` and ```--password``` arguments.

The ```--bcc``` flag forces Polly to use bccfor sending to multiple addresses

Don't worry, Polly will check your login credentials at startup
