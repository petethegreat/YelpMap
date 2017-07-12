#!/usr/bin/env python

from __future__ import print_function

import sys
import os
import requests
import urllib
from urllib import urlencode
from urllib import quote


import pandas as pd
# https://github.com/joestump/python-oauth2


# https://github.com/Yelp/yelp-fusion/blob/master/fusion/python/sample.py

API_ROOT = 'https://api.yelp.com/'
CREDENTIALS = 'yelpCredentials.txt'
TOKENCACHE = 'tokenCache.txt'


def GetCredentials():
    # credential info is stored in a text file.
    # this can be obtained by signing into yelp and registering an app
    fname = CREDENTIALS
    lines = None
    try:
        with open(fname,'r') as infile:
            lines = infile.readlines()
    except IOError:
        print('Error, could not open file {f}'.format(f=fname))
        sys.exit()

    words = lines[1].strip().split()
    thecid = words[0]
    thesecret = words[1]

    return thecid,thesecret

def GetToken():
    
    #check the cache file for an existing token
    if (os.path.exists(TOKENCACHE)):
        # read token if cachefile exists
        try:
            with open(TOKENCACHE,'r') as infile:
                token = infile.readline().strip()
                return token
        except IOError:
            print('Error, could not read from {tc}\n'.format(tc=TOKENCACHE))
            sys.exit()
    else:
        # get a new token if it does not
        theid,thesecret = GetCredentials()

        # send a POST request to get an auth token
        oauthpath='oauth2/token'
        authroot='{ar}{oauth}'.format(ar=API_ROOT,oauth=quote(oauthpath.encode('utf8')))
        payload = {
            'grant_type':'client_credentials',
            'client_id':theid,
            'client_secret':thesecret
        }


        r = requests.post(authroot,data=payload)
        if r.status_code != requests.codes.ok:
            print('Error, bad authentication request')
            print(r.status_code)
            print(r.text)
            sys.exit()

        # request is good.
        # get token info
        response_dict = r.json()
        token=response_dict['access_token']
        # print('token = {token}'.format(token=response_dict['access_token']))
        try:
            with open(TOKENCACHE,'w') as tc:
                tc.write('{token}\n'.format(token=thetoken))
        except IOError:
            print('could not write to {tc}'.format(tc=TOKENCACHE))
            sys.exit()
        return token


def pullFromYelp(payload,token):
    ''' Fetch restaurant information via yelp api '''
    # api search url
    searchurl = '{root}v3/businesses/search'.format(root=API_ROOT)

    # request headers - need authoriztion token in here
    headers = {'user-agent':'Pete\'s python script','Authorization':'Bearer {tk}'.format(tk=token)}
    
    # send get request with payload info
    q = requests.get(searchurl,headers=headers,params=payload)
    
    # check reponse
    if q.status_code != requests.codes.ok:
        print('Error, bad statuscode request')
        print(q.url)
        print(q.status_code)
        print(q.text)
        sys.exit()
    # parse json, return dictionary of results
    responsedict = q.json()
    return responsedict
    

def DoStuff():
    ''' pull info from yelp '''
    
    # restaurant categories to search for
    categories = ['chinese','french','burgers','mexican','mideastern','sushi','italian','steak','sushi','indpak']
    
    # how many results to fetch with each api call
    thelim = 50

    # info to send in api query. 
    payload = {'location':'Toronto, On, Ca','limit':thelim,'offset':0}
    
    # will store fetched results for each call in a dataframe. 
    # will store all results in a masterdf
    Masterdf = None

    # get the auth token
    token = GetToken()

    # loop over categories
    for cat in categories:
        # configure request
        # each call can retrieve at most 50 records
        # use offset to retrieve subsequent records (up to 1000)
        payload['offset'] = 0
        payload['categories'] = {'{ct}'.format(ct=cat)}
        
        # number of entries in this category that have been read
        read =0
        # total number of entries in this category
        total=1
        while read < min(total,1000):
            payload['offset'] = read
            responsedict = pullFromYelp(payload,token)
            total = responsedict['total']
        
            # lists to store info in
            yid = []
            lat = []
            lng = []
            name = []
            rating = []
            reviews = []
            thecat = []
        
            # loop over entries in the response
            for business in responsedict['businesses']:
                yid.append(business['id'].encode('utf-8'))
                lat.append(business['coordinates']['latitude'])
                lng.append(business['coordinates']['longitude'])
                name.append(business['name'].encode('utf-8'))
                rating.append(business['rating'])
                reviews.append(business['review_count'])
                thecat.append(cat)
            read += len(yid)
            print ('read {rd} of {t} {cat} restaurants'.format(t=total,cat=cat,rd=read))

            # construct dataframe from lists
            thisdf = pd.DataFrame({
                'yelpid':yid,
                'lat':lat,
                'lng':lng,
                'name':name,
                'rating':rating,
                'reviews':reviews,
                'category':thecat
                })

            # append thisdf to Masterdf
            if Masterdf is None:
                Masterdf = thisdf
            else:
                Masterdf = Masterdf.append(thisdf)
            # print(Masterdf.shape)
    # write Masterdf to file
    Masterdf.to_csv('yelpData.csv',na_rep='NA')

  
def main():

    DoStuff()


if __name__ == '__main__':
    main()
