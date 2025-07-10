# main.py

import argparse
from jira_api import get_issue, create_issue, update_issue, list_issue_types, list_issues

parser = argparse.ArgumentParser(description="Jira CLI Tool")
subparsers = parser.add_subparsers(dest="command")

# GET issue
get_parser = subparsers.add_parser("get", help="Get a Jira issue")
get_parser.add_argument("issue_key", help="Jira issue key (e.g. ITSD-1)")

# Get issue type
list_types_parser = subparsers.add_parser("types", help="List issue types for this project")


# CREATE issue
create_parser = subparsers.add_parser("create", help="Create a new Jira issue")
create_parser.add_argument("issue_type", help="Type of issue to create (e.g. Task, Bug, Incident, Service Request)")
create_parser.add_argument("summary", help="Summary of the issue")
create_parser.add_argument("description", help="Description of the issue")


# UPDATE issue
update_parser = subparsers.add_parser("update", help="Update an existing Jira issue")
update_parser.add_argument("issue_key", help="Jira issue key")
update_parser.add_argument("new_summary", help="New summary to set")

# Add new subcommand
list_parser = subparsers.add_parser("list", help="List issues in the project")




args = parser.parse_args()

if args.command == "get":
    get_issue(args.issue_key)
elif args.command == "create":
    create_issue(args.issue_type, args.summary, args.description)
elif args.command == "update":
    update_issue(args.issue_key, args.new_summary)
elif args.command == "list":
    list_issues()
elif args.command == "types":
    list_issue_types()

else:
    parser.print_help()
