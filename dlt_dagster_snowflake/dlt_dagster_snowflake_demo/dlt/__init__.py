from dlt.sources.helpers import requests
import dlt
from openai import OpenAI
from pytrends.request import TrendReq
from datetime import datetime
import logging
import toml
import time
import os


def openai_sentiment(context: str):
    """
    Analyzes the sentiment of a given text using OpenAI.

    Args:
        context: The text string for which the sentiment is to be analyzed.

    Returns:
        A string indicating the sentiment of the text, which could be 'positive', 'negative', or 'neutral'.
        If an error occurs, it returns a string describing the error.
    """

    # Load your OpenAI API key from the secrets.toml file accessed by dlt
    with open(os.getcwd() + '/.dlt/secrets.toml', 'r') as secrets_file:
        secrets = toml.load(secrets_file)
        openai_key = secrets["openai"]["openai_api_key"]

    # Initialize the OpenAI client
    client = OpenAI(api_key = openai_key)

    # Set up the prompt
    messages = [
        {"role": "system", "content": "You will be given a comment text. Give the sentiment of the comment in one word. It should be either negative, positive, or neutral."},
        {"role": "assistant", "content": f"{context}"}
    ]

    # Try to get the sentiment
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
        output = response.choices[0].message.content 
        return output
    except Exception as e:
        # Return the error message if an exception occurs
        return f"An error occurred: {e}"


# The 'write_disposition' parameter determines how the data returned by this function is handled.
# 'append' means that the data will be added to the end of the existing data.
# Other possible values for 'write_disposition' are 'replace' (which replaces the existing data with the new data) 
# and 'merge' (which merges the new data with the existing data, updating any existing records that have the same primary key).
@dlt.resource(write_disposition = "append")
def hacker_news(orchestration_tools: tuple[str] = ("Airflow", )):
    """
    This function fetches stories related to specified orchestration tools from Hackernews. 
    For each tool, it retrieves the top 5 stories that have at least one comment. 
    The stories are then appended to the existing data.

    Args:
        orchestration_tools: A tuple containing the names of orchestration tools for which stories are to be fetched.

    Yields:
        A generator that yields dictionaries. Each dictionary represents a story and contains the tool name along with the story details returned by the API request.
    """

    for tool in orchestration_tools:
        response = requests.get(f'http://hn.algolia.com/api/v1/search?query={tool}&tags=story&numericFilters=num_comments>=1&hitsPerPage=5')
        data = response.json()
        # Add the tool name to each story
        data["hits"] = [{"tool_name": tool, **item} for item in data["hits"]]
        # Yield each story one by one
        yield from data["hits"]


@dlt.transformer(data_from = hacker_news, write_disposition = "append")
def comments(story):
    """
    This function fetches comments for each story yielded by the 'hacker_news' function. 
    It calculates the number of pages of comments based on the number of comments each story has, 
    and fetches comments page by page. The comments are then appended to the existing data.

    Args:
        story: A dictionary representing a story, yielded by the 'hacker_news' function.

    Yields:
        A generator that yields lists of dictionaries. Each list represents a page of comments, 
        and each dictionary within the list represents a comment and contains the tool name, story title, 
        story URL, sentiment of the comment, and the comment details returned by the API request.
    """

    tool_name = story["tool_name"]
    story_title = story["title"]
    story_id = story["story_id"]
    url = story.get("url")
    num_comments = story["num_comments"]

    num_pages = int(num_comments/20) # The API returns 20 comments per page
    if num_pages != num_comments/20:
        num_pages += 1

    for page in range(num_pages):
        response = requests.get(f'http://hn.algolia.com/api/v1/search?tags=comment,story_{story_id}&page={page}')
        data = response.json()
        # Add the tool name, story title, story URL, and sentiment to each comment
        data["hits"] = [{"tool_name": tool_name, "story_title": story_title, "story_url": url, "sentiment": openai_sentiment(item["comment_text"]), **item} for item in data["hits"]]
        #data["hits"] = [{"tool_name": tool_name, "story_title": story_title, "story_url": url, **item} for item in data["hits"]] # Without sentiment_analysis
        # Yield each page of comments
        yield data["hits"]


@dlt.source()
def hacker_news_full(orchestration_tools:tuple[str] = ("Airflow", )):
    """
    This function is a dlt source that groups together the resources and transformers needed to fetch 
    Hackernews stories and their comments for specified orchestration tools. 

    Args:
        orchestration_tools: A tuple containing the names of orchestration tools for which Hacker News stories and comments are to be fetched.

    Yields:
        A generator that yields the results of the 'hacker_news' resource piped into the 'comments' transformer.
    """

    # The 'hacker_news' resource fetches stories for the specified orchestration tools
    # The 'comments' transformer fetches comments for each story yielded by the 'hacker_news' resource
    yield hacker_news(orchestration_tools = orchestration_tools) | comments


@dlt.resource(write_disposition = "append")
def google_trends(orchestration_tools: tuple[str] = ("Airflow",), start_date='2023-01-01', geo=''):
    """
    This function fetches Google Trends data for specified orchestration tools. 
    It attempts to retrieve the data multiple times in case of failures or empty responses. 
    The retrieved data is then appended to the existing data.

    Args:
        orchestration_tools: A tuple containing the names of orchestration tools for which Google Trends data is to be fetched.
        start_date: The start date for the Google Trends data. Defaults to '2023-01-01'.
        geo: The geographic area for the Google Trends data. Defaults to an empty string, which means worldwide.

    Yields:
        A generator that yields lists of dictionaries. Each list represents the Google Trends data for a tool, 
        and each dictionary within the list contains the tool name and the Google Trends data.
    """

    # pytrend = TrendReq()
    for tool in orchestration_tools:
        attempts = 0
        max_attempts = 5  # Set a maximum number of attempts to avoid infinite loops
        while attempts < max_attempts:
            try:
                end_date = datetime.now().strftime('%Y-%m-%d')
                timeframe = f'{start_date} {end_date}'
                pytrend.build_payload(kw_list = [tool], timeframe = timeframe, geo = geo)
                data_df = pytrend.interest_over_time()
                
                if not data_df.empty:
                    data_df.reset_index(inplace = True)
                    data_df.rename(columns = {tool: 'Hits'}, inplace=True)
                    data = data_df.to_dict('records')
                    data = [{"tool": tool, **item} for item in data]
                    print(data)
                    yield data
                    break  # Successfully fetched data, exit the retry loop
                else:
                    logging.warning(f"No data for {tool}. Retrying...")
                    attempts += 1
                    time.sleep(60)  # Wait before retrying
            except Exception as e:
                logging.warning(f"Encountered an error fetching data for {tool}: {e}. Attempt {attempts+1}/{max_attempts}. Retrying...")
                attempts += 1
                time.sleep(100)  # Wait before retrying
            
            if attempts >= max_attempts:
                logging.error(f"Max retries reached for {tool}. Moving to the next tool.")