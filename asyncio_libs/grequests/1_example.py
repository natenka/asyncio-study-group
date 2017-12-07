import grequests

req = grequests.get('http://httpbin.org/delay/5')
job = grequests.send(req, grequests.Pool(1))
