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
    # Reddit API endpoint for hot posts, requesting JSON format
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"

    # Set a custom User-Agent to avoid being blocked by Reddit's API throttling
    # Using a generic User-Agent that doesn't advertise automation is often safer.
    headers = {
        'User-Agent': 'Python/3.x:project:v1.0 (by /u/alu-scripting)'
    }

    # Parameters to limit the number of posts fetched
    params = {
        'limit': 10
    }

    try:
        # Make the GET request. Critically, set allow_redirects=False.
        response = requests.get(
            url,
            headers=headers,
            params=params,
            allow_redirects=False,
            timeout=5
        )

        # Check for status codes indicating an invalid subreddit or error
        # 404 Not Found is standard for nonexistent. 302 Found means redirect.
        if response.status_code >= 300:
            print(None)
            return

        # Parse the JSON response
        data = response.json()
        
        # Navigate the complex JSON structure: 
        # data -> 'data' -> 'children' (which is a list of posts)
        posts = data.get('data', {}).get('children', [])

        # Only print titles if posts exist. If list is empty, loop does nothing.
        # This handles valid but empty subreddits without printing None.
        for post in posts:
            title = post.get('data', {}).get('title')
            if title:
                print(title)

    except requests.exceptions.RequestException:
        # Catch any network errors (DNS failure, connection lost, etc.)
        print(None)
        return

if __name__ == '__main__':
    # This section is generally provided by the main test file (1-main.py)
    # but serves as a good test harness.
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        top_ten(sys.argv[1])
