import json

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

if __name__ == "__main__":
    json_file = json.load(open('data/ece310.json'))
    transcript_data = preprocess_data(json_file)

    # prettyprint and save output to file
    with open('data/exp.json', 'w') as f:
        json.dump(transcript_data, f, indent=4)
