akismet-async
=========

An asyncronous Python 3 Akismet client library.

## Installation
```
pip install akismet-async
```

## API key verification
Get your Akismet API key [here](http://akismet.com/plans/).
```python
from akismet import Akismet, Comment

akismet_client = Akismet(api_key="YOUR_AKISMET_API_KEY" blog="http://your.blog/",
                user_agent="My App/1.0.0")

await akismet_client.verify_key()
```

## Example usage
You can check a comment's spam score by creating a dictionary or a `Comment()` object
for greater type safety:
```python
from akismet import Akismet, Comment

akismet_client = Akismet(api_key="YOUR_AKISMET_API_KEY" blog="http://your.blog/",
                user_agent="My App/1.0.0")

comment = Comment(
    comment_content="This is the body of the comment",
    user_ip="127.0.0.1",
    user_agent="some-user-agent",
    referrer="unknown"
)

first_spam_status = await akismet_client.check(comment)

second_spam_status = await akismet_client.check(
    {
        "user_ip": "127.0.0.2",
        "user_agent": "another-user-agent",
        "referrer": "unknown",
        "comment_content": "This is the body of another comment",
        "comment_author": 'John Doe',
        "is_test": True,
    }
)
```
`check()` returns one of the following strings:
* `ham`
* `probable_spam`
* `definite_spam`
* `unknown`

### Submit Ham
If you have determined that a reported comment is not spam, you can report
the false positive to Akismet:
```python
await akismet_client.submit_ham(comment)
```

### Submit Spam
If a spam comment passes the Akismet check, report it to Akismet:
```python
await akismet_client.submit_spam(comment)
```
