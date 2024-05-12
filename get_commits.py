import requests
import json 
from datetime import datetime
import os

access_token=os.getenv('GITHUB_API_TOKEN')


def get_commits(api_url, owner, repo, start_date, end_date, access_token):
    headers = {'Accept': 'application/vnd.github.v3+json', "X-GitHub-Api-Version": "2022-11-28"}
       

    
    # If you have a personal access token, you can provide it for authentication
    if access_token:
        headers['Authorization'] = f'Token {access_token}'

    url = f'{api_url}/repos/{owner}/{repo}/commits'
    
    # Add 'since' and 'until' parameters for date range filtering
    params = {}
    params['since'] = start_date
    params['until'] = end_date
    print(params)

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        commits = response.json()
        with open('commits.json', 'w') as file:
            json.dump(commits, file)
            
        return [commit['commit']['author']['date'] + ' - ' + commit['commit']['message'] for commit in commits]
    else:
        print(f"Error: Unable to fetch commits. Status code: {response.status_code}")
        return None

if __name__ == "__main__":
    # Replace the following variables with your GitHub repository details
    api_url = 'https://api.github.com'
    owner = 'nszchagas'
    repo = 'pibic'
    
    start_date = '2023-11-01T00:00:00Z'
    end_date =   '2023-12-31T00:00:00Z'  

    commit_timestamps = get_commits(api_url, owner, repo, start_date, end_date, access_token)


    if commit_timestamps:
        print("Message | Timestamp")
        for i, timestamp in enumerate(commit_timestamps):
            print(i+1, " ", timestamp)

