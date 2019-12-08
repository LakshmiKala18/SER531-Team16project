from flask import render_template, request
from app import app
from SPARQLWrapper import SPARQLWrapper, JSON


@app.route('/')
@app.route('/index')
def index():
    uids = []
    sparql = SPARQLWrapper("http://35.184.170.79:3030/userdata/query")
    sparql.setQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX userdata: <http://www.semanticweb.org/raghavakannikanti/ontologies/2019/11/userdata#>
        PREFIX tweetdata: <http://www.semanticweb.org/raghavakannikanti/ontologies/2019/11/TweetonEvent#>
        PREFIX eventcat: <http://www.semanticweb.org/raghavakannikanti/ontologies/2019/10/eventcategory#>
        SELECT DISTINCT ?userid ?user_name
        WHERE {
            ?user userdata:has_ID ?userid.
            ?user userdata:has_name ?user_name.
        }""")
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for uid in results['results']['bindings']:
        u = []
        u.append(uid['userid']['value'])
        u.append(uid['user_name']['value'])
        uids.append(u)
    return render_template('welcome.html', uids=uids)


@app.route('/search2', methods=['POST'])
def search2():
    userid = float(request.form.get('userid'))
    print(type(userid))
    print(userid)
    tweets = []
    sparql = SPARQLWrapper("http://104.197.168.147:3030/eventcategory/sparql")
    sparql.setQuery("""
           PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX spatial: <http://jena.apache.org/spatial#>
PREFIX omgeo:   <http://www.ontotext.com/owlim/geo#>
PREFIX userdata: <http://www.semanticweb.org/raghavakannikanti/ontologies/2019/11/userdata#>
PREFIX tweetdata: <http://www.semanticweb.org/raghavakannikanti/ontologies/2019/11/TweetonEvent#>
PREFIX eventcat: <http://www.semanticweb.org/raghavakannikanti/ontologies/2019/10/eventcategory#>
SELECT distinct ?eventid ?eventime ?eventcity ?eventcat 
WHERE {
    SERVICE <http://34.70.187.222:3030/projecttweetdata/query>{
        SELECT ?lat ?long 
        WHERE {
        ?z tweetdata:has_latitude ?lat;
            tweetdata:tweeted_userID ?tuserid;
            tweetdata:has_longitude ?long.
            FILTER(xsd:float(?tuserid) = "%f"^^xsd:float).
        }
    }
    ?y eventcat:has_event_id ?eventid;
        eventcat:is_of_category ?eventcat;
        eventcat:at_city ?eventcity;
        eventcat:has_start_time ?eventime;
        eventcat:has_longitude ?elong;
        eventcat:has_latitude ?elat.
    FILTER((abs(xsd:float(?lat) - xsd:float(?elong)) < 1) && (abs(xsd:float(?long) - xsd:float(?elat)) < 1)).
 }limit 10""" % (userid))
    sparql.setReturnFormat(JSON)
    # sparql.method = "GET"
    results = sparql.query().convert()
    print(results)
    for tweet in results['results']['bindings']:
        t = [tweet['eventid']['value'], tweet['eventime']['value'], tweet['eventcity']['value'],
             tweet['eventcat']['value']]
        tweets.append(t)
    return render_template('search2.html', tweets=tweets)

@app.route('/search')
def search():
    location = request.args.get('location')
    tweets = []
    events = []
    event = []
    sparql = SPARQLWrapper("http://104.197.168.147:3030/eventcategory/sparql")
    sparql.setQuery(
        """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX userdata: <http://www.semanticweb.org/raghavakannikanti/ontologies/2019/11/userdata#>
            PREFIX tweetdata: <http://www.semanticweb.org/raghavakannikanti/ontologies/2019/11/TweetonEvent#>
            PREFIX eventcat: <http://www.semanticweb.org/raghavakannikanti/ontologies/2019/10/eventcategory#>
            SELECT distinct ?eventid ?eventime ?eventcity ?eventcat WHERE {
               ?y eventcat:has_event_id ?eventid;
                 eventcat:is_of_category ?eventcat;
                 eventcat:has_start_time ?eventime;
                 eventcat:has_longitude ?elong;
                 eventcat:has_latitude ?elat;
                 eventcat:at_city ?eventcity. 
                 FILTER(xsd:string(?eventcity) = "%s")
                 }limit 25""" % (location))
    sparql.setReturnFormat(JSON)
    # sparql.method = "GET"
    results = sparql.query().convert()
    for tweet in results['results']['bindings']:
        t = [tweet['eventid']['value'], tweet['eventime']['value'], tweet['eventcity']['value'],
             tweet['eventcat']['value']]
        tweets.append(t)
    return render_template('search.html', tweets=tweets)

@app.route('/event', methods=['POST'])
def event():
    eventID = request.form.get('eventID')
    tweets = []
    sparql = SPARQLWrapper("http://104.197.168.147:3030/eventcategory/query")
    sparql.setQuery(
        """PREFIX userdata: <http://www.semanticweb.org/raghavakannikanti/ontologies/2019/11/userdata#>
            PREFIX tweetdata: <http://www.semanticweb.org/raghavakannikanti/ontologies/2019/11/TweetonEvent#>
            PREFIX eventcat: <http://www.semanticweb.org/raghavakannikanti/ontologies/2019/10/eventcategory#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?elat ?elong
            WHERE {
                ?event eventcat:has_event_id ?eventid;
                    eventcat:has_longitude ?elong;
                    eventcat:has_latitude ?elat.
                    FILTER(xsd:float(?eventid) = "%s"^^xsd:float).
            }
            LIMIT 1""" % (eventID))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()['results']['bindings'][0]
    lat = float(results['elat']['value'])
    lng = float(results['elong']['value'])
    print(lat)
    print(lng)
    sparql = SPARQLWrapper("http://34.70.187.222:3030/projecttweetdata/query")
    sparql.setQuery(
        """PREFIX userdata: <http://www.semanticweb.org/raghavakannikanti/ontologies/2019/11/userdata#>
            PREFIX tweetdata: <http://www.semanticweb.org/raghavakannikanti/ontologies/2019/11/TweetonEvent#>
            PREFIX eventcat: <http://www.semanticweb.org/raghavakannikanti/ontologies/2019/10/eventcategory#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?tweet_text ?name ?tweet_date
            WHERE {
                #SERVICE <http://35.184.170.79:3030/userdata/query>
                #{
                #    ?user userdata:has_ID ?user_id.
                #    ?user userdata:has_name ?name.
                #}
                ?tweet rdf:type tweetdata:Tweet.
                ?tweet tweetdata:tweet_text ?tweet_text.
                ?tweet tweetdata:tweet_date ?tweet_date.
                ?tweet tweetdata:tweeted_userID ?user_id2.
                ?tweet tweetdata:has_latitude ?tweet_lat.
                ?tweet tweetdata:has_longitude ?tweet_lng.
                FILTER((abs(xsd:float(?tweet_lat) - "%f"^^xsd:float) < 0.5) && (abs(xsd:float(?tweet_lng) - "%f"^^xsd:float) < 0.5)).
                #FILTER(xsd:float(?user_id) = xsd:float(?user_id2)).
            }
            LIMIT 10""" % (lng, lat))
    sparql.setReturnFormat(JSON)
    # sparql.method = "GET"
    results = sparql.query().convert()
    for tweet in results['results']['bindings']:
        t = [tweet['tweet_text']['value'], tweet['tweet_date']['value']]
        tweets.append(t)
    return render_template('event.html', tweets=tweets)

# FILTER(?a (xsd:float(?lat) xsd:float(?long)) spatial:nearby(xsd:float(?elong) xsd:float(?elat) 10 'mi')).
