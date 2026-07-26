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

def open_file_in_photoshop():
    # Path to the file you want to open
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "sticker_test.PSD")

    # check if file exists
    if not os.path.isfile(file_path):
        print(f"File does not exist: {file_path}")
        return

    # convert POSIX path to HFS path (colon-delimited)
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
    output_name = sku
    script_dir = os.path.dirname(os.path.abspath(__file__))
    exports_dir = os.path.join(script_dir, "exports")
    
    # Create exports directory if it doesn't exist
    os.makedirs(exports_dir, exist_ok=True)
    
    output_path = os.path.join(exports_dir, f"{output_name}.psd")

    applescript = f'''
    tell application "Adobe Photoshop 2026"
        activate
        set docRef to current document
        save docRef as Photoshop format in file "{output_path}"
    end tell
    '''
    try:
        subprocess.run(["osascript", "-e", applescript], check=True)
        print(f"File saved as: {output_path}")
    except subprocess.CalledProcessError as e:
        print("Failed to save file:", e)

def set_background_color_to_black():
    apple_script = '''
        tell application "Adobe Photoshop 2026"
            tell current document
                set js to "
                    var doc = app.activeDocument;
                    try {
                        var layer = doc.artLayers.getByName('background');
                        doc.activeLayer = layer;

                        // If it's a locked background layer, unlock it
                        if (layer.isBackgroundLayer) {
                            layer.isBackgroundLayer = false;
                        }

                        // Set the fill color to blue
                        var fillColor = new SolidColor();
                        fillColor.rgb.red = 0;
                        fillColor.rgb.green = 0;
                        fillColor.rgb.blue = 0;

                        // Select entire layer
                        doc.selection.selectAll();

                        // Fill with the color
                        doc.selection.fill(fillColor, ColorBlendMode.NORMAL, 100, false);

                        // Deselect
                        doc.selection.deselect();
                    } catch(e) {
                        alert('Error setting background color: ' + e);
                    }
                "
                do javascript js
            end tell
        end tell
        '''
    subprocess.run(["osascript", "-e", apple_script])

def set_background_color_to_blue():
    apple_script = '''
        tell application "Adobe Photoshop 2026"
            tell current document
                set js to "
                    var doc = app.activeDocument;
                    try {
                        var layer = doc.artLayers.getByName('background');
                        doc.activeLayer = layer;

                        // If it's a locked background layer, unlock it
                        if (layer.isBackgroundLayer) {
                            layer.isBackgroundLayer = false;
                        }

                        // Set the fill color to blue
                        var fillColor = new SolidColor();
                        fillColor.rgb.red = 0;
                        fillColor.rgb.green = 0;
                        fillColor.rgb.blue = 255;

                        // Select entire layer
                        doc.selection.selectAll();

                        // Fill with the color
                        doc.selection.fill(fillColor, ColorBlendMode.NORMAL, 100, false);

                        // Deselect
                        doc.selection.deselect();
                    } catch(e) {
                        alert('Error setting background color: ' + e);
                    }
                "
                do javascript js
            end tell
        end tell
        '''
    subprocess.run(["osascript", "-e", apple_script])

def close_current_document():
    applescript = '''
    tell application "Adobe Photoshop 2026"
        activate
        close current document saving no
    end tell
    '''
    try:
        subprocess.run(["osascript", "-e", applescript], check=True)
        print("Current document closed.")
    except subprocess.CalledProcessError as e:
        print("Failed to close document:", e)

def create_three_up_composite(sku):
    """Create a vertically-stacked composite (RED on top, BLU middle, BLK bottom)
    using the currently open BLK document as the base."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    exports_dir = os.path.join(script_dir, "exports")

    red_path = os.path.join(exports_dir, f"{sku}-RED.psd")
    blu_path = os.path.join(exports_dir, f"{sku}-BLU.psd")
    output_path = os.path.join(exports_dir, f"{sku}-3UP.psd")

    jsx_path = os.path.join(script_dir, "_composite_temp.jsx")

    jsx_code = f'''
app.preferences.rulerUnits = Units.PIXELS;

var baseDoc = app.activeDocument;
var origWidth = baseDoc.width.value;
var origHeight = baseDoc.height.value;

var buffer = origHeight * 0.1;
var spacing = origHeight * 0.05;
var newWidth = origWidth + (buffer * 2);
var newHeight = (origHeight * 3) + (buffer * 2) + (spacing * 2);

// Flatten baseDoc (BLK) FIRST so it's a single layer too, then resize/position it
baseDoc.flatten();
baseDoc.resizeCanvas(newWidth, newHeight, AnchorPosition.TOPLEFT);

var blkOffsetX = buffer;
var blkOffsetY = buffer + (origHeight * 2) + (spacing * 2);
var blkLayer = baseDoc.layers[0];
blkLayer.isBackgroundLayer = false;
blkLayer.translate(blkOffsetX, blkOffsetY);

// RED: open, flatten to one layer, duplicate that single layer into baseDoc
var redDoc = app.open(new File("{red_path}"));
redDoc.flatten();
var redLayer = redDoc.layers[0].duplicate(baseDoc, ElementPlacement.PLACEATBEGINNING);
redDoc.close(SaveOptions.DONOTSAVECHANGES);
redLayer.isBackgroundLayer = false;
redLayer.translate(buffer, buffer);

// BLU: same treatment, middle slot
var bluDoc = app.open(new File("{blu_path}"));
bluDoc.flatten();
var bluLayer = bluDoc.layers[0].duplicate(baseDoc, ElementPlacement.PLACEATBEGINNING);
bluDoc.close(SaveOptions.DONOTSAVECHANGES);
bluLayer.isBackgroundLayer = false;
var bluOffsetY = buffer + origHeight + spacing;
bluLayer.translate(buffer, bluOffsetY);

baseDoc.flatten();
baseDoc.saveAs(new File("{output_path}"), new PhotoshopSaveOptions(), true);
'''

    with open(jsx_path, "w") as f:
        f.write(jsx_code)

    applescript = f'''
    tell application "Adobe Photoshop 2026"
        activate
        do javascript file "{jsx_path}"
    end tell
    '''

    result = subprocess.run(
        ["osascript", "-e", applescript],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("Failed to create 3-up composite.")
        print("---- AppleScript stderr ----")
        print(result.stderr)
    else:
        print(f"Vertical composite created: {output_path}")

    if os.path.exists(jsx_path):
        os.remove(jsx_path)


def process_csv_and_generate_psd_files():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "state_combinations.csv")
    with open (csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            if i >= 2:
                break
            state1 = row['State1']
            state2 = row['State2']
            sku = row['SKU']

            open_file_in_photoshop()
            time.sleep(1)  # delay for file to open
            replace_text_layer("line_1", state1.upper())
            time.sleep(0.3)
            replace_text_layer("line_2", state2.upper())
            time.sleep(0.3)
            save_psd_as(sku + "-RED")
            time.sleep(.5)
            set_background_color_to_blue()
            time.sleep(0.3)
            save_psd_as(sku + "-BLU")
            time.sleep(.5)
            set_background_color_to_black()
            time.sleep(0.3)
            save_psd_as(sku + "-BLK")
            time.sleep(.5)
            create_three_up_composite(sku)
            time.sleep(.5)
            close_current_document()

if __name__ == "__main__":
    #open_photoshop()
    # open_file_in_photoshop()
    # time.sleep(1)  # slight delay if Photoshop is still launching
    # replace_text_layer("line_1", "Hello")
    # replace_text_layer("line_2", "World")
    # save_psd_as()
    process_csv_and_generate_psd_files()
