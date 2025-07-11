import subprocess
import sys

def run_command(args):
    # Execute command with shell features like pipes (|), redirection (>)
    process = subprocess.Popen(args, shell=True)
    # waits for the process to complete (and collects its output, not used here)
    process.communicate()

if __name__ == "__main__":
    # Get all command line arguments
    args = sys.argv[1:]

    # Exit if no arguments provided
    if not args:
        print("Usage: nopop <command and arguments>")
        sys.exit(1)

    # Parse and execute command
    run_command(args)
