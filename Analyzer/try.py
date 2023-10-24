import requests

# SonarQube server URL and authentication token
sonarqube_url = 'http://localhost:9000'
token = 'sqp_f847b5425c21ec5d45d3c24aa7d70d8e7c30fa41'

# API endpoint to get issues
api_endpoint = f'{sonarqube_url}/api/issues/search'


# List of issue keys you're interested in
issue_keys = ['AW2B7o6r3B9TT8GyB1XZ', 'AW2B7o6r3B9TT8GyB1Ya', 'AW2B7o6r3B9TT8GyB1Yb']  # Example issue keys

# Define parameters for the API request
params = {
    'issues': ','.join(issue_keys)
}

# Set up headers for authentication
headers = {
    'Authorization': f'Bearer {token}'
}

# Send the API request
response = requests.get(api_endpoint, params=params, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the response JSON
    issues = response.json()['issues']
    
    # Print information about each issue
    for issue in issues:
        print(f"Rule: {issue['rule']} | Message: {issue['message']} | Line: {issue['line']}")
else:
    print(f"Error: {response.status_code} - {response.text}")