"""
A Python library for accessing the Meetup API.

"""
import os, httplib
import oauth2 as oauth
import requests
import simplejson as json

# Meetup class
class Meetup():
    CONSUMER_KEY    = 'CONSUMER_KEY_HERE'
    CONSUMER_SECRET = 'CONSUMER_SECRET_HERE'
    SERVER = 'api.meetup.com'
    REQUEST_TOKEN_URL = 'http://%s/oauth/request/' % SERVER
    AUTHORIZATION_URL = 'http://www.meetup.com/authorize/'
    ACCESS_TOKEN_URL = 'http://%s/oauth/access/' % SERVER
    CALLBACK_URL = 'CALLBACK_URL_HERE'
    DEBUG = False

    def FetchResponse(self, oauth_request, connection, debug=DEBUG):
        url = oauth_request.to_url()
        connection.request(oauth_request.http_method,url)
        response = connection.getresponse()
        s=response.read()
        if debug:
            print 'requested URL: %s' % url
            print 'server response: %s' % s
        return s

    def FetchResponse(self, oauth_request, connection, url): #added URL as config. parameter
        connection.request(oauth_request.method, url, headers=oauth_request.to_header()) #added headers to pass parameters
        response = connection.getresponse()
        s=response.read()
        return s

    def GetRequestToken(self):
        connection = httplib.HTTPSConnection(self.SERVER)
        consumer = oauth.Consumer(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        signature_method = oauth.SignatureMethod_PLAINTEXT()
        oauth_request = oauth.Request.from_consumer_and_token(consumer, http_url=self.REQUEST_TOKEN_URL)
        oauth_request.sign_request(signature_method, consumer, None)
        resp = self.FetchResponse(oauth_request, connection, self.REQUEST_TOKEN_URL) #passing in explicit url
        auth_token = oauth.Token.from_string(resp)
        auth_url = "%s?oauth_token=%s&oauth_callback=%s" % (self.AUTHORIZATION_URL, auth_token.key, self.CALLBACK_URL) #build the URL
        return auth_url, auth_token

    def GetAccessToken(self, access_code, request_token):
        request_token = oauth.Token.from_string(request_token)
        connection = httplib.HTTPSConnection(self.SERVER)
        consumer = oauth.Consumer(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        signature_method = oauth.SignatureMethod_PLAINTEXT()
        oauth_request = oauth.Request.from_consumer_and_token(consumer, token=request_token, http_url=self.ACCESS_TOKEN_URL)
        oauth_request.sign_request(signature_method, consumer, auth_token)
        resp = self.FetchResponse(oauth_request, connection, self.ACCESS_TOKEN_URL)
        access_token = oauth.Token.from_string(resp) # parse the response into an OAuthToken object / passingin explicit url
        return access_token

    def ApiCall(self, access_token, apiCall='https://api.meetup.com/2/groups/self'):
        signature_method = oauth.SignatureMethod_PLAINTEXT()
        connection = httplib.HTTPSConnection(self.SERVER)s
        consumer = oauth.Consumer(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        oauth_request = oauth.Request.from_consumer_and_token(consumer, token=access_token, http_url=apiCall)
        oauth_request.sign_request(signature_method, consumer, access_token)
        headers = oauth_request.to_header(realm='api.meetup.com')
        connection.request('GET', apiCall, headers=headers)
        resp = connection.getresponse()
        return json.loads(resp.read())