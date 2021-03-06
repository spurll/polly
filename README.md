polly
=====

A simple website polling tool that polls a website until it changes.

Requirements:
  * [requests](http://docs.python-requests.org/en/latest/index.html)
  * [slacker](https://github.com/os/slacker)

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

triggers
--------
Polly is designed to trigger actions on changes. Triggers can be passed as a dict in the
settings json file, under the keyword ```triggers```.

Currently, the only supported triggers are ```MailTrigger``` and ```SlackTrigger```. Their options
are as follows:

```
{
    "mail": {
        "recipients": [LIST OF RECIPIENTS],
        "bcc": true or false,       # should you put recipients in the bcc or to field
        "username": LOGIN_USERNAME, # if not given, it will be prompted for
        "password": LOGIN_PASSWORD, # if not given, it will be prompted for
        "host": SMTP_HOST,          # defaults to gmail's host address
        "subject": "A CUSTOM SUBJECT FOR THE EMAIL"
    },
    "slack": {
        "recipients": [LIST OF "@user.name" AND/OR "#channel"],
        "token": SLACK_API_TOKEN,   # if not given, it will be prompted for
        "name": BOT_NAME            # defaults to "Polly"
        "icon": EMOJI,              # a Slack emoji; defaults to ":bird:"
        "message": "CUSTOM TEXT FOR THE MESSAGE"
    }
}
```

email
-----
As emailing is the most likely trigger to be used, it also can be added
directly from the command line.

To add an address to email, use the ```--mail``` argument.
```
python polly.py ADDRESS --mail EMAIL
```
The flag can be added multiple times:
```
python polly.py ADDRESS --mail EMAIL --mail ANOTHER_EMAIL
```

The SMTP host used is Google's, unless an alternative is provided with the ```--host``` argument

Username and password can be entered securely in a prompt, or using the ```--user``` and ```--password``` arguments.

The ```--bcc``` flag forces Polly to use bcc for sending to multiple addresses

Don't worry, Polly will check your login credentials at startup

formatters
----------
Formatters provide a way for polly to format site data, so that subjections of a page may be watched.

A formatter can be passed in in the settings json file under the keyword ```formatter```

Currently, the only supported formatted is the RegexFormatter, which applies a regex to the contents.
It may be directly invoked using the ```--regex``` argument.

It's sole argument is the expression its comparing against. If groups are used, the groups will be returned,
otherwise, the matching's success will be returned.
