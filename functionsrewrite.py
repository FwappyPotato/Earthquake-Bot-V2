#Parser Loop
d = feedparser.parse('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.atom', modified=modified)
if d.status == 304:
    #print('unchanged')
    time.sleep(looptime)
    #exit loop
modified = d.modified
print('--updated at ' + modified)
        # Call Filter


# Filter
quakecords = (d.entries[0].where.coordinates[1], d.entries[0].where.coordinates[0])
distance = geopy.distance.distance(waypoint, quakecords).miles
print(str(d.entries[0].tags[1].term) + ' earthquake ' + str("%.2f" % distance) + ' miles away ' + str(quakecords))
if distance < pingdist: #configure in a way that allows n number of distances to be calculated
    # call ID checker

#ID Checker - If (matching - update message)/Else (send new message)

if d.entries[0].id == oldid
#could look for previous ID in feed instead of only entries index 1, then we can ignore non consequectial eathquakes


# Discord Bot

oldid = d.entries[0].id
