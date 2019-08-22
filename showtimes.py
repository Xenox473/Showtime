import geocoder, json, urllib, datetime
import pprint as pp
from urllib.request import Request, urlopen

def generateURL():
    global amc_key
    global mdb_key
    global url
    with open('amc_key.txt', 'r') as fp:
            amc_key = fp.read()
    with open('mdb_key.txt', 'r') as fp:
            mdb_key = fp.read()
    url = 'https://api.amctheatres.com/v2/'
    # print(url)
    return

def sendRequest(temp_url):
    req = Request(temp_url)
    req.add_header('X-AMC-Vendor-Key', amc_key)
    resp = urlopen(req)
    data = json.load(resp)
    return data

def mdbMovieLookup(name):
    temp_url = 'https://api.themoviedb.org/3/search/movie?api_key=' + mdb_key + '&query=' + name
    print(temp_url)
    data = sendRequest(temp_url)
    return data

def amcShowtimesLookup(theatre_id, movie_name):
    now = datetime.datetime.now()
    temp_url = url + 'theatres/' + str(theatre_id) + '/showtimes/' + str(now.month) + '-' + str(now.day) + '-' + str(now.year) + '/?movie=' + movie_name
    print(temp_url)
    req = Request(temp_url)
    req.add_header('X-AMC-Vendor-Key', amc_key)
    resp = urlopen(req)
    print(resp)
    return

def getTheatre():
    temp_url = url + 'locations'
    lat, lng = getLatLng()
    params = {'latitude' : lat, 'longitude' : lng}
    url_values = urllib.parse.urlencode(params)
    temp_url = temp_url + '?' + url_values
    data = sendRequest(temp_url)
    # pp.pprint(data['_embedded']['locations'][5]['_embedded']['theatre']['name'])
    locations = data['_embedded']['locations']
    nearest_theatre = locations[0]['_embedded']['theatre']
    # pp.pprint(nearest_theatre.keys())
    return nearest_theatre

def getNowPlaying():
    theatre = getTheatre()
    temp_url = url + 'theatres/' + str(theatre['id']) + '/showtimes'
    print("Showing movies in " + theatre['name'])
    print('x-'*50)
    data = sendRequest(temp_url)
    showtimes = data['_embedded']['showtimes']
    # pp.pprint(data['_embedded']['showtimes'][0].keys())
    counter = 1
    for showtime in showtimes:
        print(str(counter) + '. ' + showtime['movieName'] + ' - ' + str(showtime['genre']))
        counter += 1
    print('x-'*50)
    user_input = input("What movie are you interested in?\n")
    selected_movie = showtimes[int(user_input) - 1]
    print("Providing details for " + selected_movie['movieName'])
    try:
        movieDetails = mdbMovieLookup(selected_movie['movieName'])
    except:
        movieDetails = None
    if not movieDetails:
        print("No further information for the movie could be found at this time.")
    else:
        print('Score: ' + str(movieDetails['results'][0]['vote_average']))

    return

def getLatLng():
    g = geocoder.ip('me')
    lat,lng = g.latlng
    return (lat,lng)

if __name__ == '__main__':
    generateURL()
    # getNowPlaying()
    # getLatLng()
    # getTheatre()
    # mdbMovieLookup('Spider')
    amcShowtimesLookup(6163, 'Angry Bird')
