# Company Analysis

Enter any company's ticker and year, and my app can analyze that company's 10-K for the year to provide investment advice.

Link to the demo：[https://youtu.be/1c0R65d3Ezk](https://youtu.be/1c0R65d3Ezk)

# Tech Stack

I use React as the front-end framework and Flask as the back-end framework. The reason is that I downloaded 10-K text files locally for analysis, so I chose Python for string processing, and Flask is tightly integrated with Python. React, as a front-end framework, is convenient to write and more flexible for debugging compared to static web pages. Regarding the LLM API, I used the open-source LLama3 during debugging, but the results were mediocre, while OpenAI's model clearly performed better, as demonstrated in the demo video using OpenAI's API.

My overall approach is as follows: On the backend, I first use Python's API to download the 10-K files locally, then use regular expressions to extract the relevant items, and finally extract the information I need from those items. This information, along with my prompt, is input into the LLM, and the results are returned. On the front-end, the user inputs the company name and year, the backend locates the specified annual report, analyzes it, and the results are displayed on the front-end.

# Insights Selection

# Item 1

## Business

For a company that one is not familiar with, looking at the business section can quickly get you up to speed. This is where the company lays out the different segments of a business, from which we can learn:

1. What the company does?
2. What products or services it makes？
3. How it makes money？

## Markets and Distribution

 This part helps us understand:

1.  How the company distributes its products?
2.  Who its main customers are?

## Competition

This part helps us understand:

1. How competitive is in this industry?
2. What are key variables that companies within this industry compete on?

# Item 7

## Management’s Discussion and Analysis of Financial Condition and Results of Operations

This is where the company provides the revenue for each of the segements as well as discusses how each segment has been performing.

## Gross Margin

As investors, we want to see high gross margins, because this is a sign that the company has what is referred to as pricing power.

## Operating Expenses

Operating expenses are not directly associated with making a product or providing a service. So in order for a company to grow its profiability, the revenue needs to be increasing faster than expenses.
