import requests

# SonarQube server URL and authentication token
sonarqube_url = 'http://localhost:9000'
token = 'sqp_f847b5425c21ec5d45d3c24aa7d70d8e7c30fa41'

# API endpoint to get issues
api_endpoint = f'{sonarqube_url}/api/issues/search'

# Java file path you're interested in (e.g., relative to the project root)
java_file_path = 'data_code_stable/Codes/eclipse::che/Demo/14953/60d11768d02f6d3513a17b17d831e2eee337db0a'

# Define parameters for the API request
params = {
    'componentKeys': f'eclipse_LTS:data_code_stable/Codes/eclipse::che/Demo/14953/60d11768d02f6d3513a17b17d831e2eee337db0a',
    'rules': 'java:S106',
    'statuses': 'OPEN',
    'types': 'CODE_SMELL',
    'ps': 100  # Number of results per page, adjust as needed
}

# Set up headers for authentication
headers = {
    'Authorization': f'Bearer sqp_f847b5425c21ec5d45d3c24aa7d70d8e7c30fa41'
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