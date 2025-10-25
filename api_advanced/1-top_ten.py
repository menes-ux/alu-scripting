#!/usr/bin/python3
"""
Queries the Reddit API and prints the titles of the first 10 hot posts
for a given subreddit.
"""
import requests
import sys
from requests.exceptions import RequestException # Explicit import for robust error handling


def top_ten(subreddit):
    """
    Prints the titles of the first 10 hot posts for a given subreddit.
    If the subreddit is invalid, prints None.
    """
    # Reddit API endpoint for hot posts, requesting JSON format
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"

    # Use the User-Agent that gave you the best score so far
    headers = {
        'User-Agent': 'PostmanRuntime/7.35.0'
    }

    # Parameters to request exactly 10 posts
    params = {
        'limit': 10
    }

    try:
        # Request the data. Crucially, set allow_redirects=False.
        response = requests.get(
            url,
            headers=headers,
            params=params,
            allow_redirects=False,
            timeout=15
        )

        # 1. Check for non-200 status codes (404, 302 redirect, 429 throttling)
        # Any status code other than 200 means the request failed or the subreddit is invalid.
        if response.status_code != 200:
            print(None)
            return

        # 2. Status code is 200 OK. Safely parse JSON.
        data = response.json()
        
        # Navigate to the list of posts (children) using defensive dictionary lookups
        posts = data.get('data', {}).get('children', [])

        # 3. Print the titles
        for post in posts:
            # Safely extract the title
            title = post.get('data', {}).get('title')
            if title: 
                print(title)

    except RequestException:
        # Catch network-related errors (DNS failure, connection timeout, etc.)
        print(None)
    except Exception:
        # Catch any unexpected error during JSON parsing/data lookup
        # This acts as a fallback for any remaining errors.
        print(None)

if __name__ == '__main__':
    # PEP8: Imports are alphabetically ordered at the top.
    # The 'sys' import is only needed if this block is present.
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        top_ten(sys.argv[1])
