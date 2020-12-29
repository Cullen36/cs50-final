from decimal import *
from functools import wraps

from flask import render_template, session


def error(message="Bad request", code=400):
    """Returns an error page with a message and error code."""
    return render_template("error.html", code=code, message=message), code

def chance(p1, p2, dom_s, rec_s):
    """Add some descriptive text here."""
    # format symbols
    n1 = dom_s + dom_s
    n2 = dom_s + rec_s
    n3 = rec_s + rec_s
    
    # decide base case
    
    # if either is hd
    if p1 == 'hd' or p2 == 'hd':
        # if only 1 is hd
        if (p1 == 'hd' and p2 != 'hd') or (p1 != 'hd' and p2 == 'hd'):
            # if other is he
            if (p1 == 'hd' and p2 == 'he') or (p1 == 'he' and p2 == 'hd'):
                # he + hd 
                return {
                    'hd':[0.5, n1], 
                    'he':[0.5, n2]
                    }
            else:
                # hd + hr
                return {
                    'he':[1, n2]
                    }
        else:
            # hd + hd
            return {
                'hd': [1, n1]
                }
    # if one is he
    elif p1 == 'he' or p2 == 'he':
        # if other is he
        if (p1 == 'he' and p2 == 'he'):
            # he + he
            return {'he': [0.5, n2],
            'hr': [0.25, n3],
            'hd': [0.25, n1]}
        else:
            # he + hr
            return {'he': [0.5, n2],
            'hr': [0.5, n3]}
    else:
        # hr + hr
        return {'hr': [1, n3]}

def mult(data):
    """Add some descriptive text here."""
    chances = []
    rownum = 0
    con = 0
    for row in data:
        # checks if this is the first iteration (runs code only once below but gets the data from the first row)
        if rownum == 0:
            # iterates over the key value pairs in the first row of data
            for key, value in row.items():
                # sets a counter
                rowN = 0
                # itterates through the rows of data again skipping the first to avoid multiplying a gene by itself
                for thisrow in data:
                    if rowN > 0 and not rowN > 1:
                        # sets a blank list
                        thisgene=[]
                        if len(data) > 2:
                            # iterates over key value pairs for other rows
                            for k, v in thisrow.items():
                                # calculates chance as a fraction
                                c = (value[0] * v[0])
                                # adds symbols together to form the full symbol (i.e: AaSs)
                                h = value[1] + v[1]
                                # appends these to a dictionary
                                thisgene.append({f'chance{con}' : [c, h]})
                                con += 1
                            # appends dictionary to list
                            chances.append(thisgene)
                        elif len(data) == 2:
                            # iterates over key value pairs for other rows
                            for k, v in thisrow.items():
                                # calculates chance as a fraction
                                c = (value[0] * v[0]).as_integer_ratio()
                                # adds symbols together to form the full symbol (i.e: AaSs)
                                h = value[1] + v[1]
                                # appends these to a dictionary
                                thisgene.append({f'chance{con}' : [c, h]})
                                con += 1
                            # appends dictionary to list
                            chances.append(thisgene)
                    rowN += 1
        rownum += 1
        
        # returns value on second itteration of first loop for efficency
        if rownum > 0:
            if len(data) == 2:
                return chances
            break
    # recursion?
    if len(data) > 2:
        it2 = []
        it2.append({})
        for sub in chances:
            for chance in sub:
                for key, value in chance.items():
                    it2[0][key] = value
        con = 0
        for row in data:
            if con > 1:
                it2.append(row)
            con += 1
        return mult(it2)

    
def which_traits(traits, gene):
    """Add some descriptive text here."""
    string = ''
    count = 0
    for i in traits:
        if i['dom_s'] in gene:
            if count == 0:
                string = string + i['dom_n'] 
            else:
                string = string + ', ' + i['dom_n'] 
        elif i['dom_s'] not in gene:
            if count == 0:
                string = string + i['rec_n'] 
            else:
                string = string + ', ' + i['rec_n'] 
        count += 1
    return string
    

def prob(genes):
    """Returns the probability of the given (list of) genes occuring simultaneously."""
    return genes

def count_required(f):
    """Decorator which ensures the user starts from the beginning."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("count") is None:
            return error("Bad request: Start at the beginning.", 400)
        return f(*args, **kwargs)
    return decorated_function
