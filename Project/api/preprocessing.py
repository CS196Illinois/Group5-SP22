import flask
from flask import request, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import json
from SearchEngine import search

UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = {'json'}

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_dict(sentence, start, end) -> dict:
    obj = {}
    obj['sentence'] = sentence
    obj['start'] = start
    obj['end'] = end
    return obj

def preprocess_data(obj):
    """
    Preprocess transcript data. 
    :param obj The transcript file.
    Data format is as follows:
        {
            "i": 0,         The index of the word entry.
            "w": "Hello",   The word spoken.
            "s": 265340,    Time in millisec since meeting start time at the beginning of the word.
            "e": 265580,    Time in millisec since meeting start time at the end of the word.
            "t": "word",    The type of transcript entry. I am not sure of types other than word.
            "a": 56         I do not know what this is.
        },
    This function parses a json file into sentences and returns data in the following format:
        {
            "sentence": "This is the sentence spoken.",
            "start"   : 265340,
            "end"     : 269340
        }
    """

    data = []
    curr_sent = []
    curr_start = obj[0]['s'] // 1000 

    for itm in obj:
        """
        iterate through every item in the json transcript. 
        Each iteration, append the current word to an array.
        If we encounter a punctuation, append the current array as a dict
        to the data array and reset the current sentence.
        """

        curr_sent += [itm['w']]
        if itm['w'][-1] == '.' or itm['w'][-1] == '?': # check for end of sentence -> the [-1] means look at last char
            # build the sentence with what we have 
            sentence = ' '.join(curr_sent)
            # get the end time of the current sentence
            end_time = itm['e'] // 1000
            # append the sentence to the data dict
            data += [get_dict(sentence, curr_start, end_time)]
            # get new start time
            curr_start = itm['s'] // 1000
            # reset current sentence
            curr_sent = []
    
    return data

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS     


@app.route('/processfile/', methods=['GET','POST'])
def upload_file():
        # check if the post request has the file part
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return 403, "File not found"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            f = json.load(open(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
            data = preprocess_data(f) # figure out what the data path is
            return jsonify(data)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/search/<filename>/<query>', methods=['GET','POST'])
def search_file(query):
    #  use the search function from SearchEngine.py to search for the 
    # input phrase in the transcript file with the given filename.

    res = search(f'./uploads/{filename}.json', query)
    return jsonify(res)

  


@app.route('/', methods=['GET'])
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <body>

    <h1>MediaSpace Searcher</h1>

    </body>
    </html>
    '''


# @app.route('/api/v1/resources/books/all', methods=['GET'])
# def api_all():
    # return jsonify(data)


# @app.route('/api/v1/resources/books', methods=['GET'])
# def api_id():
#     # Check if an ID was provided as part of the URL.
#     # If ID is provided, assign it to a variable.
#     # If no ID is provided, display an error in the browser.
#     if 'id' in request.args:
#         id = int(request.args['id'])
#     else:
#         return "Error: No id field provided. Please specify an id."

#     # Create an empty list for our results
#     results = []

#     # Loop through the data and match results that fit the requested ID.
#     # IDs are unique, but other fields might return many results
#     for book in file:
#         results.append(book)

#     # Use the jsonify function from Flask to convert our list of
#     # Python dictionaries to the JSON format.
#     return jsonify(results)

app.run()