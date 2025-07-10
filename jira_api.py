import requests
import json
from requests.auth import HTTPBasicAuth
from config import JIRA_DOMAIN, EMAIL, API_TOKEN, PROJECT_KEY

auth = HTTPBasicAuth(EMAIL, API_TOKEN)
headers = {"Accept": "application/json", "Content-Type": "application/json"}

def get_issue(issue_key):
    url = f"{JIRA_DOMAIN}/rest/api/3/issue/{issue_key}"
    try:
        response = requests.get(url, headers=headers, auth=auth)
        response.raise_for_status()
        data = response.json()

        summary = data['fields']['summary']
        description_adf = data['fields']['description']

        print(f"Issue Key: {data['key']}")
        print(f"Summary: {summary}")
        print("Description:")

        if description_adf and isinstance(description_adf, dict):
            try:
                for block in description_adf.get("content", []):
                    if block["type"] == "paragraph":
                        paragraph = ""
                        for content in block.get("content", []):
                            if content["type"] == "text":
                                paragraph += content["text"]
                        print(f"  {paragraph}")
            except Exception as parse_error:
                print("  (Could not parse description content.)")
        else:
            print("  (No description provided.)")
    except requests.exceptions.HTTPError as e:
        print(f"Failed to fetch issue: {e} - {response.text}")

def list_issues(jql="project = ISD ORDER BY created DESC"):
    url = f"{JIRA_DOMAIN}/rest/api/3/search"
    params = {"jql": jql}
    response = requests.get(url, headers=headers, auth=auth, params=params)
    if response.status_code == 200:
        issues = response.json().get("issues", [])
        for issue in issues:
            print(f"{issue['key']} - {issue['fields']['summary']}")
    else:
        print(f"Failed to fetch issues: {response.status_code}")


def list_issue_types():
    url = f"{JIRA_DOMAIN}/rest/api/3/issue/createmeta?projectKeys={PROJECT_KEY}&expand=projects.issuetypes.fields"
    
    try:
        response = requests.get(url, headers=headers, auth=auth)
        response.raise_for_status()
        data = response.json()

        issue_types = data["projects"][0]["issuetypes"]
        print(f"Issue types available in project {PROJECT_KEY}:")
        for itype in issue_types:
            print(f"- {itype['name']}")
    except requests.exceptions.HTTPError as e:
        print(f"Failed to fetch issue types: {e} - {response.text}")



def create_issue(issue_type, summary, description):
    url = f"{JIRA_DOMAIN}/rest/api/3/issue"
    
    payload = {
        "fields": {
            "project": {"key": PROJECT_KEY},
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": description
                            }
                        ]
                    }
                ]
            },
            "issuetype": {"name": issue_type}
        }
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            auth=auth,
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        print(f"Issue created: {data['key']}")
    except requests.exceptions.HTTPError as e:
        print(f"Failed to create issue: {e} - {response.text}")



def update_issue(issue_key, new_summary):
    url = f"{JIRA_DOMAIN}/rest/api/3/issue/{issue_key}"
    payload = json.dumps({
        "fields": {
            "summary": new_summary
        }
    })
    response = requests.put(url, headers=headers, auth=auth, data=payload)
    try:
        response.raise_for_status()
        print(f"Issue {issue_key} updated successfully.")
    except requests.exceptions.HTTPError as e:
        print(f"Failed to update issue: {e} - {response.text}")

