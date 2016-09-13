# Written by Ali Murtaza Sharif
# Date: 10-Sept-2016
# Please don't steal

import requests

# TODO Some refactoring is needed to split up this function into more logical pieces
# TODO Find a way to improve  the robustness of the request mechanism
def login(userid, user_pass, term, semester, year, write_file = False):
    # login details
    payload = {
            "sid" : userid, 
            "PIN" : user_pass
            }
    
    # The important urls
    # NOTE maybe put them in a dictionary?
    base_url   = "https://horizon.mcgill.ca/pban1/"
    start_url  = base_url + "twbkwbis.P_WWWLogin"
    post_url   = base_url + "twbkwbis.P_ValLogin"
    target_url = base_url + "bwskfshd.P_CrseSchdDetl"
    logout_url = base_url + "twbkwbis.P_Logout"
    
    # Create session entity that we will be using
    minerva = requests.Session()
    
    # Go to the login page with the form to get the initial session data
    start_page = minerva.get(start_url)
    
    # Place the session data in a dictionary and add the login page as the referer
    post_headers = dict(start_page.headers)
    post_headers['Referer'] = start_url
    
    # Post the login data and header session data
    post_result = minerva.post(post_url, data = payload, headers = post_headers)
    
    # Goto the target page and pass the desired term
    target_page = minerva.post(target_url, data = {"term_in": "{}".format(term)}, headers = post_result.headers)
    
    if write_file:
        with open("{}_{}.html".format(semester, year), 'w') as f:
            f.write(target_page.text)
    
    # Logout and terminate our session
    # NOTE logout currently isn't working properly
    # I can't send GET request to logout and I don't know if sending a post request will terminate my session on the server
    # Whether or not this becomes a problem remains to be seen
    minerva.get(logout_url, cookies=target_page.cookies)

    return target_page.text
