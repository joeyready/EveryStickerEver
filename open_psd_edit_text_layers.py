import subprocess
import os
import time
import csv

def open_photoshop():
    # AppleScript command to open Adobe Photoshop
    applescript = '''
    tell application "Adobe Photoshop 2026"
        activate
    end tell
    '''

    try:
        subprocess.run(["osascript", "-e", applescript], check=True)
        print("Adobe Photoshop launched successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to launch Photoshop:", e)

def open_file_in_photoshop(file_path):
    if not os.path.isfile(file_path):
        print(f"File does not exist: {file_path}")
        return

    hfs_path = file_path.replace("/", ":")[1:]

    #applescript to open file in photoshop
    applescript = f'''
    tell application "Adobe Photoshop 2026"
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
    tell application "Adobe Photoshop 2026"
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

def save_psd_as(sku):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    exports_dir = os.path.join(script_dir, "sticker_test", "exports")
    os.makedirs(exports_dir, exist_ok=True)

    output_path = os.path.join(exports_dir, f"{sku}.psd")

    applescript = f'''
    tell application "Adobe Photoshop 2026"
        activate
        set outputFile to POSIX file "{output_path}"
        save current document in outputFile as Photoshop format
    end tell
    '''
    try:
        subprocess.run(["osascript", "-e", applescript], check=True)
        print(f"File saved as: {output_path}")
    except subprocess.CalledProcessError as e:
        print("Failed to save file:", e)

def close_current_document():
    applescript = '''
    tell application "Adobe Photoshop 2026"
        activate
        if (count of documents) > 0 then
            close document 1 saving no
        end if
    end tell
    '''
    try:
        subprocess.run(["osascript", "-e", applescript], check=True)
        print("Current document closed.")
    except subprocess.CalledProcessError as e:
        print("Failed to close document:", e)

def process_csv_and_generate_psd_files():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "sticker_test", "state_combinations.csv")
    file_path = os.path.join(script_dir, "sticker_test", "sticker_test.psd")

    with open(csv_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            if i >= 5:
                break

            state1 = row["State1"]
            state2 = row["State2"]
            sku = row["SKU"]

            open_file_in_photoshop(file_path)
            time.sleep(1)  # slight delay if Photoshop is still launching
            replace_text_layer("line_1", state1)
            replace_text_layer("line_2", state2)
            save_psd_as(sku)
            close_current_document()

if __name__ == "__main__":
    #open_photoshop()
    # open_file_in_photoshop()
    # time.sleep(1)  # slight delay if Photoshop is still launching
    # replace_text_layer("line_1", "Hello")
    # replace_text_layer("line_2", "World")
    # save_psd_as()
    process_csv_and_generate_psd_files()
