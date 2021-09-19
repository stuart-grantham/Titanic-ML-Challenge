import urllib.request
from bs4 import BeautifulSoup


# Go to the Website:
# https://find-and-update.company-information.service.gov.uk/search 

# Search for “Barclays”
# https://find-and-update.company-information.service.gov.uk/search?q=Barclays 

# Click on the first result:
# https://find-and-update.company-information.service.gov.uk/company/00048839 

#Parse the HTML

host = 'https://find-and-update.company-information.service.gov.uk'
url_search_addition = "/search?q="

def get_entity_details(entity_name):

    details = {
     'company_name': None,
     'registered_address': None,
     'company_status': None,
     'company_type': None,
     'incorporated_on': None }
    #funtions will run here
    #local function operating on details
    def add_to_details(web_dict_name,details_name):
        if web_dict_name in webpage_company_details.keys():
           details[details_name] = webpage_company_details[web_dict_name]
        else:
          details[details_name] = "{} Detail not found on page".format(details_name)
    
    company_href = get_company_href(entity_name)
    if company_href != "":
        webpage_company_details =  get_company_details(company_href)
    else:
        return "Search Result not found"

    #use quick function to  populate details dictionary with webpage data
    # if nothing is found, returns detail not found
    add_to_details("company_name","company_name")
    add_to_details("Registered office address","registered_address")
    add_to_details("Company status","company_status")
    add_to_details("Company type","company_type")
    add_to_details("Incorporated on","incorporated_on")
    return details

def get_company_details(company_href):
    try:
        webpage_dict = {}
        with urllib.request.urlopen(host+company_href) as webpage:
            webpage_read = webpage.read()
        bs_webpage = BeautifulSoup(webpage_read,"html.parser")
        #zero in on the content box
        bs_webpage = bs_webpage.find(id="content-container")
        #extract name
        webpage_dict["company_name"] = bs_webpage.find(class_="company-header").p.text
        #loop through all the dlelements, as they contain all the company data besides name
        dl_elements = bs_webpage.find_all("dl")
        for dl_element in dl_elements:
            #add to output dictionary, using name in the dt element as the key
            webpage_dict[dl_element.dt.text] = dl_element.dd.text.strip()
    finally:
        #return whatever the webpage_dict was completed
        return webpage_dict

def get_company_href(entity_name):
    try:
        with urllib.request.urlopen(host+url_search_addition+entity_name) as webpage:
            webpage_read = webpage.read()
        bs_webpage = BeautifulSoup(webpage_read,"html.parser")
        #find the results list
        bs_webpage = bs_webpage.find(id="results")
        #find the first element that is a company, (can change to just first result if needed)
        bs_webpage = bs_webpage.find("li",class_="type-company")
        return bs_webpage.find("a").get("href")
    except:
        #if error was encountered, no HREF
        return ""

if __name__ == '__main__':
    #script calls go here
    entities_to_test = ["Barclays", "Screwfix","ASDA", "Brokensearch1123"]
    #run test for a list of entities
    print([get_entity_details(entity) for entity in entities_to_test])

#Possible improvements:
#Incorporate with testing framework
#Handle errors better
#use ENV file

