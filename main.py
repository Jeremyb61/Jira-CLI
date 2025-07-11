import shlex
from jira_api import get_issue, create_issue, update_issue, list_issue_types, list_issues, escalate_issue, list_transitions

def main():
    print("Welcome to the Jira CLI shell. Type 'help' for commands, 'exit' to quit.")

    while True:
        try:
            command = input("jiracli> ").strip()
            if not command:
                continue
            if command.lower() in ["exit", "quit"]:
                break
            if command.lower() == "help":
                print("Commands:")
                print("  list - Lists all issue")
                print("  get <ISSUE-KEY> - To view one issue")
                print("  create <SUMMARY> <DESCRIPTION> <ISSUE-TYPE> - Create a new issue")
                print("  update <ISSUE-KEY> <NEW-SUMMARY> - Update an issue")
                print("  types - List issue types")
                print("  transitions <ISSUE-KEY> - To list availabe transitions for an issue")
                print("  escalate <ISSUE-KEY> - To escalate an issue")

                print("  exit")
                continue

            # Parse input like a shell command
            args = shlex.split(command)
            cmd = args[0]

            if cmd == "get" and len(args) >= 2:
                get_issue(args[1])
            elif cmd == "create" and len(args) >= 4:
                create_issue(args[1], args[2], args[3])
            elif cmd == "update" and len(args) >= 3:
                update_issue(args[1], args[2])
            elif cmd == "types":
                list_issue_types()
            elif cmd == "list":
                list_issues()
            elif cmd == "transitions" and len(args) >= 2:
                list_transitions(args[1])
            elif cmd == "escalate" and len(args) >= 2:
                escalate_issue(args[1])


            else:
                print("Invalid command or arguments. Type 'help'.")

        except KeyboardInterrupt:
            print("\nExiting.")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
