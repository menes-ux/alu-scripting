#!/usr/bin/python3
"""
Queries the Reddit API and prints the titles of the first 10 hot posts
for a given subreddit.
"""
import requests
import sys


def top_ten(subreddit):
    """
    Prints the titles of the first 10 hot posts for a given subreddit.
    If the subreddit is invalid, prints None.
    """
    # The simpler URL format is often preferred, with limit in the query string
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"

    # Use a generic User-Agent to avoid API throttling. 
    # The simplified 'PostmanRuntime/7.35.0' is acceptable, but let's 
    # use a slightly more custom one for safety against generic blocking.
    headers = {
        'User-Agent': 'alu-api-advanced/1.0 (by /u/alu-scripting)'
    }

    # Parameters to request exactly 10 posts
    params = {
        'limit': 10
    }

    try:
        # Request the data, disable redirects
        response = requests.get(
            url,
            headers=headers,
            params=params,
            allow_redirects=False,
            timeout=10  # Increased timeout for robustness
        )

        # 1. Check for invalid subreddit (404, or 302 redirect)
        if response.status_code >= 300:
            print(None)
            return

        # 2. Status code is 200 OK. Now safely parse JSON.
        data = response.json()
        
        # Navigate to the list of posts (children)
        posts = data.get('data', {}).get('children', [])

        # 3. Print the titles
        for post in posts:
            title = post.get('data', {}).get('title')
            if title:
                print(title)

    except requests.exceptions.RequestException:
        # Catch network/connection-specific errors.
        print(None)
        return
    except Exception:
        # Catch any remaining unexpected JSON/parsing errors 
        # (e.g., if the structure changes).
        print(None)
        return

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        top_ten(sys.argv[1])
