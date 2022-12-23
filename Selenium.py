from lib2to3.pgen2 import driver
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import json


def filter_journals():
    try:
        journal_input_div_object = driver.find_element(By.ID,"refinement-ContentType:Journals")
        driver.execute_script("arguments[0].click();", journal_input_div_object)
        sleep(1)
    except:
        print("canot filter journals")

#getting authors
def get_author():
    try:
        authors = journal.find_element(By.CSS_SELECTOR,'xpl-authors-name-list').text
        list_auths = authors.split(';\n')
    except:
        list_auths = None
        print("Authors not found")
    return list_auths

#getting title
def get_title():
    try:
        tile_object = journal.find_element(By.CSS_SELECTOR,'h3')
        title = tile_object.text
    except:
        title= None
        print("title not found")
    return title

#getting publication info (year type publisher)
def get_journal_info():
    try:
        pub_info = journal.find_element(By.CSS_SELECTOR,'div.publisher-info-container')
        year = pub_info.find_element(By.XPATH,'./span[1]').text
        year = year.replace('Year: ', '')

    
        type = pub_info.find_element(By.XPATH,'./span[2]').text
        type = type.lstrip("|")

        publisher = pub_info.find_element(By.XPATH,'./span[3]').text
        #formating publisher
        publisher = publisher.lstrip('|')
        publisher = publisher.replace(' Publisher: ', '')
    except:
        print("info not nound")
        publisher= None
        type= None
        year= None

    return publisher, type, year

#getting journal link
def get_journal_link():
    try:
        tile_object = journal.find_element(By.CSS_SELECTOR,'h3')
        titleToclick = tile_object.find_element(By.CSS_SELECTOR,'a')
        journal_link = titleToclick.get_attribute("href")
    except:
        print("journal link not found")
        journal_link = None
    return journal_link

#click event on the journal
def click_journal():
    #Cliking the link
    try:
        tile_object = journal.find_element(By.CSS_SELECTOR,'h3')
        titleToclick = tile_object.find_element(By.CSS_SELECTOR,'a')
        ActionChains(driver).move_to_element(titleToclick).perform()
        titleToclick.click()
        sleep(1)
    except:
        print("Nothing to clik")

#getting abstract
def get_abstract():
    try:
        absract_div = driver.find_element(By.CLASS_NAME , "row.document-main-body")
        abstract_div2 = absract_div.find_element(By.CLASS_NAME,"u-mb-1")
        abstract_text = abstract_div2.find_element(By.XPATH,"./div[1]").text
    except:
        abstract_text = None
        print("abstract not found")

    return abstract_text

#getting the conference location
def get_conference_location():
    try:
        location_div = driver.find_element(By.CLASS_NAME , "u-pb-1.doc-abstract-conferenceLoc")
        location_text = location_div.text
        formated_location_text = location_text.rsplit(': ',1)[1]
    except:
        formated_location_text = None
        print("location not found")
    return formated_location_text

#getting the references from the dropdown
def get_references():
    try:
        #clicking on the dropdown to display elements
        references_dropdown = driver.find_element(By.ID,"references")
        ActionChains(driver).move_to_element(references_dropdown).perform()
        references_dropdown.click()

        sleep(0.5)
        #getting the references from the dropdown
        references_list = driver.find_elements(By.CLASS_NAME,"reference-container")
        r_list = list()
        for ref in references_list:
            ref_text = ref.find_element(By.XPATH,"./xpl-reference-item-migr/div/div/div[3]/div[1]").text
            splited_refs = ref_text.split('.\n')
            r_list.append(splited_refs)
        driver.back()
    except:
        r_list = None
        print("references not found")

    return r_list

def get_keywords():
    keyword_list = list()
    final_list_kw = list()
    try:
        #clicking on the dropdown to display elements
        keywords_dropdown = driver.find_element(By.ID,"keywords")
        ActionChains(driver).move_to_element(keywords_dropdown).perform()
        keywords_dropdown.click()

        sleep(0.5)

        #getting the keywords from the dropdown
        
        keyword_div = driver.find_element(By.CLASS_NAME,"accordion-body.collapse.show")
        keywords_ul = keyword_div.find_element(By.XPATH,"./xpl-document-keyword-list/section/div/ul")
        keywords_li = keywords_ul.find_elements(By.CSS_SELECTOR,"li.doc-keywords-list-item")

        str_kw = ""
        for kw in keywords_li:
            keyword = kw.find_element(By.XPATH,"./ul").text
            str_kw += keyword

        keyword_list = str_kw.split('\n')
        keyword_list = list(set(keyword_list))
        
        #filter the array
        for character in keyword_list:
            if character == ',':
                continue
            final_list_kw.append(character)        
        driver.back()
    except:
            keyword_list = None
            print("keywords not found")
    return final_list_kw

def write_scraped_data_json(file_location:str):
    with open(file_location, "w") as write_file:
        #convert the list into a json file
        json.dump(all_journals, write_file, indent=4)

#event to click coockies 
#accepting cookies to destroy the overlay
def accept_cookies():
    cookies_btn = driver.find_element(By.CLASS_NAME, "cc-btn.cc-dismiss")
    driver.execute_script("arguments[0].click();", cookies_btn)



current_page = 1
PATH = "C:\Program Files (x86)\chromedriver.exe"
turn_it= True
all_journals = list()
while(turn_it):
    dico_journal= {}
    driver = webdriver.Chrome(PATH)
    #web_site = "https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=Abdelmalek%20Essaadi&newsearch=true&type=alt3&pageNumber="+str(current_page)
    web_site = "https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=blockchains&pageNumber="+str(current_page)
    driver.get(web_site)
    sleep(1)
    filter_journals()
    journals = driver.find_elements(By.CLASS_NAME, "List-results-items")

    enf_of_recherche = False
    next_page = 2
    
    accept_cookies()

    for journal in journals:
        
        authors_tmp  = get_author()
        title_tmp = get_title()
        publisher_tmp, type_tmp, year_tmp = get_journal_info()
        journal_link_tmp = get_journal_link()

        #click journal
        click_journal()

        abstract_tmp = get_abstract()
        location_tmp = get_conference_location()
        references_tmp = get_references()
        keywords_tmp = get_keywords()

        #go back to the privious page
        driver.back()

        dico_journal = {"authors":authors_tmp, "title":title_tmp,"publisher":publisher_tmp, "type":type_tmp , "year":year_tmp , "journal_link":journal_link_tmp,"abstract": abstract_tmp, "location": location_tmp,"references": references_tmp, "keywords": keywords_tmp } 
        
        #debuging purposes
        #print(dico_journal)

        #this list contains all our data
        all_journals.append(dico_journal)



    print("current page",current_page)

    driver.close()
    
    current_page += 1
    
    if(dico_journal == {} or current_page == 15 ):
        turn_it = False

write_scraped_data_json("scraped_data.json")

driver.close()



