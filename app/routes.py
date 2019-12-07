from flask import render_template, request
from app import app
from SPARQLWrapper import SPARQLWrapper, JSON

@app.route('/')
@app.route('/index')
def index():
    return render_template('welcome.html')

@app.route('/search')
def search():
    location = request.args.get('location')
    tweets = []
    events = []
    event = []
    sparql = SPARQLWrapper("http://34.70.187.222:3030/projecttweetdata/query")
    sparql.setQuery("""
        PREFIX userdata: <http://www.semanticweb.org/raghavakannikanti/ontologies/2019/11/userdata#>
        PREFIX tweetdata: <http://www.semanticweb.org/raghavakannikanti/ontologies/2019/11/TweetonEvent#>
        PREFIX eventcat: <http://www.semanticweb.org/raghavakannikanti/ontologies/2019/10/eventcategory#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT *
        WHERE {
            ?tweet rdf:type tweetdata:Tweet.
            ?tweet tweetdata:tweet_text ?tweet_text.
            ?tweet tweetdata:tweet_date ?tweet_date.
            ?tweet tweetdata:tweeted_userID ?user_id.
            ?tweet tweetdata:has_latitude ?tweet_lat.
            ?tweet tweetdata:has_longitude ?tweet_lng.
            SERVICE <http://35.184.170.79:3030/userdata/query>
            {
                ?user rdf:type userdata:User.
                ?user userdata:has_ID ?user_id.
                ?user userdata:has_name ?name.
                ?user userdata:has_location ?user_location.
                ?user userdata:has_screenname ?user_screenname
            }
        }
        LIMIT 1
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print(results)
    for tweet in results['results']['bindings']:
        t = []
        t.append(tweet['tweet_text']['value'])
        t.append(tweet['name']['value'])
        tweets.append(t)
    return render_template('search.html', tweets=tweets)