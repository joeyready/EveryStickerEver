import subprocess
import os
import time

def open_photoshop():
    # AppleScript command to open Adobe Photoshop
    applescript = '''
    tell application "Adobe Photoshop 2025"
        activate
    end tell
    '''

    try:
        subprocess.run(["osascript", "-e", applescript], check=True)
        print("Adobe Photoshop launched successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to launch Photoshop:", e)

def open_file_in_photoshop():
    # Path to the file you want to open\
    file_path = os.path.expanduser("~/Desktop/DSC04328.PSD")


    # check if file exists
    if not os.path.isfile(file_path):
        print(f"File does not exist: {file_path}")
        return

    # convert POSIX path to HFS path (colon-delimited)
    hfs_path = file_path.replace("/", ":")[1:]

    #applescript to open file in photoshop
    applescript = f'''
    tell application "Adobe Photoshop 2025"
        open alias "{hfs_path}"
        activate
    end tell
    '''

    try:
        subprocess.run(["osascript", "-e", applescript], check=True)
        print(f"File opened in Photoshop: {file_path}")
    except subprocess.CalledProcessError as e:
        print("Failed to open file in Photoshop:", e)

def replace_text_layer(layer_name="line_1", new_text="Hello"):
    applescript = f'''
    tell application "Adobe Photoshop 2025"
        activate
        try
            tell current document
                set contents of text object of layer "{layer_name}" to "{new_text}"
            end tell
            display notification "Layer '{layer_name}' updated to '{new_text}'" with title "Photoshop Automation"
        on error errMsg
            display dialog "Error: " & errMsg
        end try
    end tell
    '''
    try:
        subprocess.run(["osascript", "-e", applescript], check=True)
        print(f"Layer '{layer_name}' updated to '{new_text}'")
    except subprocess.CalledProcessError as e:
        print("Failed to update layer text:", e)

if __name__ == "__main__":
    #open_photoshop()
    open_file_in_photoshop()
    time.sleep(1)  # slight delay if Photoshop is still launching
    replace_text_layer("line_1", "Hello")
    replace_text_layer("line_2", "World")
