PyMeetup
========

A simpler library for the Meetup in Python. I didn't like the cumbersome [current implementation](https://github.com/meetup/python-api-client) So why not build something new?

### Oauth step
Initializing the library:

	from meetup import Meetup
	m = Meetup()
	url, token = m.GetRequestToken()
	
	# open url and authenticate, get the callback code.
	
	access_token = m.GetAccessToken(code, token)
	
### Making API Calls
Making an API call is as simple as possible: 

	reponse = m.ApiCall(access_token, 'API_ENDPOINT_AND_PARAMETERS')
	
	
	



