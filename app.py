import os
import requests
from twilio.rest import Client
import flask
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
app = flask.Flask(__name__)

# twilio credential
account_sid = os.getenv("SID")
auth_token = os.getenv("TOKEN")
client = Client(account_sid, auth_token)

# catAPI
catUrl = "https://api.thecatapi.com/v1/images/search?format=json"
# catFactAPI
factUrl = "https://catfact.ninja/fact?max_length=140"

# catAPI credential
catData = {}
catHeaders = {"Content-Type": "application/json", "x-api-key": os.getenv("KEY")}
factData = {}
factHeaders = {"Accept": "application/json"}


catRes = requests.get(catUrl, headers=catHeaders, data=catData)
factRes = requests.get(factUrl, headers=factHeaders, data=factData)

catR = catRes.json()
factR = factRes.json()

# catAPI for image
images = catR[0]["url"]
# catFactAPI for fact
fact = factR["fact"]
# use twilio to send messages
message = client.messages.create(
    from_="+13185943649",
    messaging_service_sid=os.getenv("MID"),
    body="\n***CAT fact of the day!" + "\U0001F638" + "***\n" + fact,
    media_url=images,
    to="+1xxxxxxxxxx",
)

print(message.sid)


@app.route("/")
def main():
    return flask.render_template("landingPage.html", images=images)


@app.route("/landingPage")
def landingPage():
    return flask.render_template("landingPage.html")


@app.route("/about")
def about():
    return flask.render_template("about.html")


@app.route("/ourService")
def ourService():
    return flask.render_template("ourService.html")


app.run(
    debug=True,
)
