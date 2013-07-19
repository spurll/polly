polly
=====

A simple website polling tool that polls a website until it changes.

Requirements:
  * [requests](http://docs.python-requests.org/en/latest/index.html)

To Run:
```
python polly.py ADDRESS
```
    
By default, the tool polls every 60 seconds. To adjust the polling time use the ```--delay``` argument
```
python polly.py ADDRESS --delay TIME_IN_SECONDS
```

Unless silenced using the ```--silence``` flag, polly will write an alert to stdout every time it runs
