#Bradley Scharf
## HW 1
## SI 364 F18
## 1000 points

#################################

## List below here, in a comment/comments, the people you worked with on this assignment AND any resources you used to find code (50 point deduction for not doing so). If none, write "None".

#None

## [PROBLEM 1] - 150 points
## Below is code for one of the simplest possible Flask applications. Edit the code so that once you run this application locally and go to the URL 'http://localhost:5000/class', you see a page that says "Welcome to SI 364!"

from flask import Flask, render_template, request
import requests
import json
app = Flask(__name__)
app.debug = True

@app.route('/class')
def hello_to_you():
    return 'Welcome to SI 364!'

@app.route('/movie/<movie_name>')
def movie(movie_name):
	base_url = "https://itunes.apple.com/search?"
	params_diction = {"term": movie_name, "media": "movie"}
	resp = requests.get(base_url, params=params_diction)
	text = resp.text
	return text




## [PROBLEM 2] - 250 points
## Edit the code chunk above again so that if you go to the URL 'http://localhost:5000/movie/<name-of-movie-here-one-word>' you see a big dictionary of data on the page. For example, if you go to the URL 'http://localhost:5000/movie/ratatouille', you should see something like the data shown in the included file sample_ratatouille_data.txt, which contains data about the animated movie Ratatouille. However, if you go to the url http://localhost:5000/movie/titanic, you should get different data, and if you go to the url 'http://localhost:5000/movie/dsagdsgskfsl' for example, you should see data on the page that looks like this:

# {
#  "resultCount":0,
#  "results": []
# }


## You should use the iTunes Search API to get that data.
## Docs for that API are here: https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
## Of course, you'll also need the requests library and knowledge of how to make a request to a REST API for data.

## Run the app locally (repeatedly) and try these URLs out!

## [PROBLEM 3] - 250 points

## Edit the above Flask application code so that if you run the application locally and got to the URL http://localhost:5000/question, you see a form that asks you to enter your favorite number.
## Once you enter a number and submit it to the form, you should then see a web page that says "Double your favorite number is <number>". For example, if you enter 2 into the form, you should then see a page that says "Double your favorite number is 4". Careful about types in your Python code!
## You can assume a user will always enter a number only.

@app.route('/question')
def double_fav_num():
    html_form = '''
    <html>
    <body>
    <form method="GET" action="http://localhost:5000/answer">
        <label>Enter your favorite number:
            <input name="Favorite_Number" value="0" type="number">
        </label></br>
        <input type="submit" value="Submit">
    </form>
    </body>
    </html>
    '''
    return html_form

@app.route('/answer', methods = ['GET', 'POST'])
def result_doubled():
    if request.method == 'GET':
        number = request.args.get('Favorite_Number')
        number_doubled = str(int(number)*2)
        return "Double your favorite number is {}".format(number_doubled)



## [PROBLEM 4] - 350 points

## Come up with your own interactive data exchange that you want to see happen dynamically in the Flask application, and build it into the above code for a Flask application, following a few requirements.

## You should create a form that appears at the route: http://localhost:5000/problem4form

## Submitting the form should result in your seeing the results of the form on the same page.

## What you do for this problem should:
# - not be an exact repeat of something you did in class
# - must include an HTML form with checkboxes and text entry
# - should, on submission of data to the HTML form, show new data that depends upon the data entered into the submission form and is readable by humans (more readable than e.g. the data you got in Problem 2 of this HW). The new data should be gathered via API request or BeautifulSoup.

# You should feel free to be creative and do something fun for you --
# And use this opportunity to make sure you understand these steps: if you think going slowly and carefully writing out steps for a simpler data transaction, like Problem 1, will help build your understanding, you should definitely try that!

# You can assume that a user will give you the type of input/response you expect in your form; you do not need to handle errors or user confusion. (e.g. if your form asks for a name, you can assume a user will type a reasonable name; if your form asks for a number, you can assume a user will type a reasonable number; if your form asks the user to select a checkbox, you can assume they will do that.)

# Points will be assigned for each specification in the problem.

@app.route('/problem4form', methods = ['GET', 'POST'])
def books():
    html_form = '''
    <html>
    <body>
    <form method="POST" action="/problem4form">
        <label>Enter your Zip Code to get the current weather:
            <input name="Zip_Code" value="" type="text">
        </label></br>
        <label>Metrics:
            <input type="checkbox" name="tempc" value="celcius">Celcius(C)
            <input type="checkbox" name="tempf" value="fahrenheit">Fahrenheit(F)<br>
        </label></br>
        <input type="submit" value="Submit">
    </form>
    </body>
    </html>
    '''
    if request.method == 'POST':
    	zipcode = request.form.get('Zip_Code')
    	apikey = "780d91df19062e7556708d6d283ff296"
    	base_url = "http://api.openweathermap.org/data/2.5/weather?"
    	params_diction = {"zip": zipcode, "APPID": apikey}
    	resp = requests.get(base_url, params=params_diction)
    	text = resp.text
    	output = json.loads(text)
    	temp = output['main']['temp']
    	description = output['weather'][0]['description']
    	print(request.form.get('tempc'))
    	print(request.form.get('tempf'))
    	if request.values.get('tempc') == "celcius":
    		converted_temp_c = (int(temp)/10)
    		rounded_temp_c = (str(converted_temp_c)[0:5])
    		html_form = html_form + "Currently the weather outside in your area is " + str(rounded_temp_c)+"°C "+"with " + description + "<br>"
    	if request.values.get('tempf') == "fahrenheit":
    		converted_temp_f = ((int(temp)/10) * (9/5)) + 32
    		rounded_temp_f = (str(converted_temp_f)[0:5])
    		html_form = html_form + "Currently the weather outside in your area is " + str(rounded_temp_f)+"°F "+"with " + description + "<br>"
    return html_form

if __name__ == '__main__':
    app.run()

