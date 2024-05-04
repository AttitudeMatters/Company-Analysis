from sec_edgar_downloader import Downloader
import os
import re
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import platform

tickers = ["AAPL", "MSFT"] # examples


def download_10K_filings(ticker, start_year, end_year):
    dl = Downloader("MyCompanyName", "my.email@domain.com")
    for year in range(start_year, end_year + 1):
        dl.get("10-K", ticker, after=f"{year}-01-01", before=f"{year}-12-31")


def download(ticker):
    if os.path.exists(f"sec-edgar-filings/{ticker}"):
        print("existed company!")
        return
    # Download 10-K filings from 1995 to 2023 for each ticker
    print(f"Downloading 10-K filings for {ticker} from 1995 to 2023...")
    download_10K_filings(ticker, 1995, 2023)
    print(f"Completed downloads for {ticker}")


def read_txt(file_name):
    txt_file = open(file_name, "r", encoding='UTF8')
    str_txt = txt_file.read()
    return str_txt


def extract_between(text, start, end):
    pattern = re.compile(r'{}(.*?){}'.format(re.escape(start), re.escape(end)), re.S)
    result = re.search(pattern, text)
    return result.group(1) if result else None


business_prompt = "Please answer the following questions based on the given information." \
                  "1. What the company does?" \
                  "2. What products or services it make" \
                  "3. How it makes money" \
                  "output in the format of HTML"

market_prompt = "Please answer the following questions based on the given information." \
                "1.How the company distributes its products?" \
                "2. Who its main customers are?" \
                "output in the format of HTML"

competition_prompt = "Please answer the following questions based on the given information." \
                     "1. How competitive is in this industry?" \
                     "2. What are key variables that companies within this industry compete on?" \
                     "output in the format of HTML"

management_prompt = "Please plot a table based on the given information and analyze the table" \
                    "output in the format of HTML"

gmargin_prompt = "Please plot a table based on the given information and analyze the table" \
                    "output in the format of HTML"

oexpenses_prompt = "Please plot a table based on the given information and analyze the table" \
                    "output in the format of HTML"

def LLM(input, prompt):
    url = "https://api.awanllm.com/v1/completions"
    AWANLLM_API_KEY = "5b8deeea-cf54-4fec-9a01-52397db508ea"

    payload = json.dumps({
        "model": "Meta-Llama-3-8B-Instruct",
        "prompt": f"{input}"
                  f"{prompt}"
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {AWANLLM_API_KEY}"
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.json()['choices'][0]['text'])
    return response.json()['choices'][0]['text']


def analyze(ticker, year_to_analysis):
    download(ticker)

    print("All requested filings have been downloaded.")

    data_dir = f"./sec-edgar-filings/{ticker}/10-K"
    path_list = os.listdir(data_dir)
    if platform.system() == 'Darwin':
        path_list.remove('.DS_Store')
    path_list = sorted(path_list)
    print(path_list)

    # Regex to find <DOCUMENT> tags
    doc_start_pattern = re.compile(r'<DOCUMENT>')
    doc_end_pattern = re.compile(r'</DOCUMENT>')
    type_pattern = re.compile(r'<TYPE>[^\n]+')

    year_to_analysis = str(year_to_analysis)[-2:]
    year_folder_name = 'not found'
    for folder in path_list:
        if folder.split('-')[1] == year_to_analysis:
            year_folder_name = folder
            print("year folder name:", year_folder_name)
            break
    if year_folder_name == 'not found':
        print("no year")
        return -1
    for folder in path_list:
        # Path updated to reflect the file naming convention you mentioned
        file_path = os.path.join(data_dir, year_folder_name, "full-submission.txt")

        raw_10k = read_txt(file_path)

        doc_start_is = [x.end() for x in doc_start_pattern.finditer(raw_10k)]
        doc_end_is = [x.start() for x in doc_end_pattern.finditer(raw_10k)]
        doc_types = [x[len('<TYPE>'):] for x in type_pattern.findall(raw_10k)]

        document = {}

        # Create a loop to go through each section type and save only the 10-K section in the dictionary
        for doc_type, doc_start, doc_end in zip(doc_types, doc_start_is, doc_end_is):
            if doc_type == '10-K':
                document[doc_type] = raw_10k[doc_start:doc_end]
        # display excerpt the document
        print(document['10-K'][0:500])

        break

    # Write the regex
    item1 = re.compile(r'(>Item(\s|&#160;|&nbsp;)(1)\b\.{0,1})|(ITEM\s(1)\b|(Item 15))')

    # Use finditer to math the regex
    matches = item1.finditer(document['10-K'])

    # Write a for loop to print the matches
    for match in matches:
        print(match)

    # Matches
    matches = item1.finditer(document['10-K'])

    # Create the dataframe
    test_df = pd.DataFrame([(x.group(), x.start(), x.end()) for x in matches])

    test_df.columns = ['item', 'start', 'end']
    test_df['item'] = test_df.item.str.lower()

    # Display the dataframe
    test_df.head()

    # Get rid of unnesesary charcters from the dataframe
    test_df.replace('&#160;', ' ', regex=True, inplace=True)
    test_df.replace('&nbsp;', ' ', regex=True, inplace=True)
    test_df.replace(' ', '', regex=True, inplace=True)
    test_df.replace('\.', '', regex=True, inplace=True)
    test_df.replace('>', '', regex=True, inplace=True)

    # display the dataframe
    test_df.head()

    # Drop duplicates
    pos_dat = test_df.sort_values('start', ascending=True).drop_duplicates(subset=['item'], keep='last')

    # Set item as the dataframe index
    pos_dat.set_index('item', inplace=True)

    # Display the dataframe
    print(pos_dat)

    item_1_raw = document['10-K'][pos_dat['start'].loc['item1']:pos_dat['start'].loc['item15']]

    print(item_1_raw[0:1000])

    ## First convert the raw text we have to exrtacted to BeautifulSoup object
    item_1_content = BeautifulSoup(item_1_raw, 'html.parser')

    ### By just applying .pretiffy() we see that raw text start to look oragnized, as BeautifulSoup
    ### apply indentation according to the HTML Tag tree structure
    print(item_1_content.prettify()[0:1000])

    print(item_1_content.get_text("\n\n"))

    business_raw = item_1_content.get_text("\n\n")
    business = extract_between(business_raw, "Business", "Markets and Distribution")

    print(business)
    result = {}
    result['business_result'] = LLM(business, business_prompt)

    market = extract_between(business_raw, "Markets and Distribution", "Competition")
    result['market_result'] = LLM(market, market_prompt)

    competition = extract_between(business_raw, "Competition", "Supply of Components")
    result['competition_result'] = LLM(competition, competition_prompt)

    # get item7

    item7 = re.compile(r'(>Item(\s|&#160;|&nbsp;)(7A|7)\.{0,1})|(ITEM\s(7A|7))')

    # Use finditer to math the regex
    matches = item7.finditer(document['10-K'])

    # Write a for loop to print the matches
    for match in matches:
        print(match)

    # Matches
    matches = item7.finditer(document['10-K'])

    # Create the dataframe
    test_df = pd.DataFrame([(x.group(), x.start(), x.end()) for x in matches])

    test_df.columns = ['item', 'start', 'end']
    test_df['item'] = test_df.item.str.lower()

    # Display the dataframe
    test_df.head()

    # Get rid of unnesesary charcters from the dataframe
    test_df.replace('&#160;', ' ', regex=True, inplace=True)
    test_df.replace('&nbsp;', ' ', regex=True, inplace=True)
    test_df.replace(' ', '', regex=True, inplace=True)
    test_df.replace('\.', '', regex=True, inplace=True)
    test_df.replace('>', '', regex=True, inplace=True)

    # display the dataframe
    test_df.head()

    # Drop duplicates
    pos_dat = test_df.sort_values('start', ascending=True).drop_duplicates(subset=['item'], keep='last')

    # Set item as the dataframe index
    pos_dat.set_index('item', inplace=True)

    # Display the dataframe
    print(pos_dat)

    item_7_raw = document['10-K'][pos_dat['start'].loc['item7']:pos_dat['start'].loc['item7a']]

    item_7_raw[0:1000]

    ## First convert the raw text we have to exrtacted to BeautifulSoup object
    item_7_content = BeautifulSoup(item_7_raw, 'html.parser')

    ### By just applying .pretiffy() we see that raw text start to look oragnized, as BeautifulSoup
    ### apply indentation according to the HTML Tag tree structure
    print(item_7_content.prettify()[0:1000])

    print(item_7_content.get_text("\n\n"))

    i7_raw = item_7_content.get_text()
    management = extract_between(i7_raw,
                                 "Management’s Discussion and Analysis of Financial Condition and Results of Operations",
                                 "Gross Margin")

    print(management)
    result['management_result'] = LLM(management, management_prompt)

    gmargin = extract_between(i7_raw, "Gross Margin", "Operating Expenses")
    result['gmargin_result'] = LLM(gmargin, gmargin_prompt)

    oexpense = extract_between(i7_raw, "Operating Expenses", "Research and Development")
    result['oexpense_result'] = LLM(oexpense, oexpenses_prompt)

    return result

# result = analyze("AAPL", 2002)
# with open("result.txt", "w") as output_file:
#     print(result, file=output_file)
