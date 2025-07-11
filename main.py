import shlex
from jira_api import get_issue, create_issue, update_issue, list_issue_types, list_issues

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
                print("  List all issue: list")
                print("  To view one issue: get <ISSUE-KEY>")
                print("  Create a new issue: create <SUMMARY> <DESCRIPTION> <ISSUE-TYPE>")
                print("  Update an issue: update <ISSUE-KEY> <NEW-SUMMARY>")
                print("  List issue types: types")
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

            else:
                print("Invalid command or arguments. Type 'help'.")

        except KeyboardInterrupt:
            print("\nExiting.")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
