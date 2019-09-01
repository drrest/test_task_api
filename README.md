# This is test task of API

Running: 
You can run project by the docker-compose

```bash
docker-compose build
```
```bash
docker-compose up
```

#### As a result docker will up 2 containers API & BOT
#### BOT will starts after 10 seconds and after complete work will start again.
#### Result of bot work will be placed into file *output.std* in the folder __bot

# API POINTS

### Authentication works via JWT token inside HEADERS

```text
So header will include
Authorization: Bearer  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6ImRyLnJlc3RAZ21haWwuY29tIiwiZXhwIjoxNTY3MjExNzE4LCJlbWFpbCI6ImRyLnJlc3RAZ21haWwuY29tIn0.XEetq3m6kYcgSmj4pF4WTu_HIV22WGUL7XBCQtWRr-E
```

## User Section

### - /user/signup
registering new user

request **POST**
```json
{  
   "email":"test@test.com",
   "first_name":"FirstName",
   "last_name":"LastName",
   "password":"asdfg12345"
}
``` 
response:
```json
{
    "response": {
        "answer": {
            "id": 1,
            "email":"test@test.com",
            "first_name":"FirstName",
            "last_name":"LastName"
            "date_joined": "2019-09-01T00:57:48.704458Z"
        }
    }
}
```

  
### - /user/login
logging in

request **POST**
```json
{  
   "email":"test@test.com",
   "password":"asdfg12345"
}
```
response:
```json
{
    "name": "FirstName LastName",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImRyLnJlc3RAZ21haWwuY29tIiwiZXhwIjoxNTY3MzAzMTY1LCJlbWFpbCI6ImRyLnJlc3RAZ21haWwuY29tIn0.ZMsMm4Q_ys_p6lWVCurN1xqreG7RUrnG3se7dBAEMxQ"
}
```

## Post Section

### - /post/creation
create of post with current user

request **POST** (*Autorized*)
```json
{
   "title": "[title]",
   "text": "[text]"
}
```
response
```json
{
    "response": {
        "answer": "ok"
    }
}
```

### - /post/like
like of some selected post ( will remove current user from unlikers of this post)

request **POST** (*Autorized*)
```json
{
   "post": "[post_id]"
}
```
response
```json
{
    "response": {
    "answer": "ok",
    "likes": 5,
    "unlikes": 3
    }
}
```

### - /post/unlike
unlike of some selected post ( will remove current user from likers of this post)

request **POST** (*Autorized*)
```python
{
   "post": [post_id]
}
```
response
```json
{
    "response": {
    "answer": "ok",
    "likes": 5,
    "unlikes": 3
    }
}
```


### - /post/list
return list of posts, which attribute draft == False

request **POST** (*Autorized*)
```json
{
   empty
}
```
response
```json
{
    "response": {
        "answer": [
            {
                "pk": 642,
                "meta": {
                    "title": "HFDRZXTRIXVWEYC",
                    "created": "2019-09-01T01:05:28.439Z",
                    "last_updated": "2019-09-01T01:05:28.439Z",
                    "text": "Kghxknwaytqcjhlaisvhetnkgzyjorqhnbllerdwnflqivzdsvppvepyoyimclgcwsyazlmeqqqrnlfwqnipfykgktqcnzgslcje",
                    "draft": false,
                    "user": 124,
                    "likers": [],
                    "unlikers": []
                }
            },{next post},{next post},{next post}
	    ]
	}
}
```
