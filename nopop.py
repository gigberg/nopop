import subprocess
import sys
import os
# import ctypes

def get_persist_dir():
    # Determine the base directory where the program is running
    if getattr(sys, 'frozen', False):
        # If the script is running from a PyInstaller bundle (EXE)
        # PyInstaller sets 'sys.frozen = True' when running in a frozen (packaged) state.
        base_dir = os.path.dirname(sys.executable)
    else:
        # If the script is running normally (as .py)
        base_dir = os.path.dirname(os.path.abspath(__file__))
    # Append 'data' to the base directory to form the persist directory
    persist_dir = os.path.join(base_dir, 'data')
    return persist_dir

def run_command(cmd_line):
    # Execute the command in a new process, using the shell to interpret the command
    print("Running command:", cmd_line)
    try:
        # Use shell=True to allow pipes, redirection, etc.
        process = subprocess.Popen(cmd_line, shell=True)
        # Wait for the process to complete and collect its output (not used here)
        process.communicate()
    except Exception as e:
        error_msg = f"Failed to run command:\n{cmd_line}\n\nError: {str(e)}"
        print(error_msg)
        # Display the error message in a message box
        # useful when standard i/o is not available caused by --noconsole option in PyInstaller
        # ctypes.windll.user32.MessageBoxW(0, error_msg, "Execution Error", 0)

if __name__ == "__main__":
    # Get all command line arguments (excluding the script name)
    args = sys.argv[1:]

    # Exit if no arguments are provided
    if not args:
        print("Usage: nopop [-s script.py] <command and arguments>")
        sys.exit(1)

    # Check if the first argument is '-s' and if there are at least two arguments
    if args[0] == "-s" and len(args) >= 2:
        # Get the script name from the second argument
        script_name = args[1]
        # Form the full path to the script by joining the persist directory and script name
        persist_path = os.path.join(get_persist_dir(), script_name)
        # Replace the script name with the full path and keep the remaining arguments
        args = [persist_path] + args[2:]

    # Execute the command with the modified arguments
    run_command(" ".join(args))
