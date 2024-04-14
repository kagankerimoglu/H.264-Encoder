# A Simple FFmpeg GUI to Transcode Multiple Formats Into H.264

# Author: Kagan Kerimoglu
# Last Revision: 14.04.24

import os
import sys
import time
import platform
import requests
import webbrowser
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, Menu, Toplevel

current_version = "1.0.0"

################################################### FUNCTIONS ###################################################

def resource_path(relative_path): 
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

readme_document = resource_path('readme.pdf')

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

encoder = resource_path('ffmpeg_amd64')

def open_file():
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title='SELECT FILE', filetypes=[("MOV files", "*.mov"), ("MXF files", "*.mxf"), ("MP4 files", "*.mp4"), ("MKV files", "*.mkv")])
    if file_path:
        print("Selected file:", file_path)
        global filename
        filename = os.path.basename(file_path)  # Extract just the filename without directory
        messagebox.showinfo("Success", "Successfully Imported")  # Display selected file in a messagebox
        global input_file
        input_file = file_path
    root.deiconify()  # Show the root window after a file is selected

def encode():
    root.grab_set()  # Grab focus
    file_path = filedialog.asksaveasfilename(title='Save As', initialfile=filename[:-4] + '.mp4', filetypes=[("MP4 files", "*.mp4"), ("MOV files", "*.mov")])
    root.grab_release()  # Release focus
    root.focus_force()  # Bring focus back to the main window
    if file_path:
        print("Save as:", file_path)
        global output_file
        output_file = file_path

        # Proceed with encoding
        preset_options = ["superfast", "veryfast", "faster", "fast",
                          "medium", "slow", "slower", "veryslow", "placebo"]
        preset = preset_options.index(preset_value.get())
        crf = crf_value.get()

        # Ensure CRF is rounded to the nearest 0.5 increment
        crf = round(float(crf) * 2) / 2

        # Path to the encoder executable        
        encoder_path = os.path.join(os.path.dirname(__file__), 'ffmpeg_amd64')

        tune = tune_value.get()
        level = level_value.get()
        profile = profile_value.get()
        pixformat = subsampling_value.get()

        ffmpeg_command = [encoder_path, '-hide_banner', '-i', input_file, '-c:v', 'libx264',
                              '-preset', preset_options[preset], '-pix_fmt', subsampling_value.get(), '-color_range', '1',
                              '-tune', tune, '-profile:v', profile_value.get(), '-level:v', level_value.get(),
                              '-crf', str(crf), '-color_primaries', '1', '-color_trc', '1', '-colorspace', '1',
                              '-movflags', 'faststart', '-c:a', 'aac', '-ar', '48k', '-b:a', '320k', output_file]

        if tune == "none":
            # Find the index of '-tune' in the command and remove it along with its argument
            tune_index = ffmpeg_command.index('-tune')
            del ffmpeg_command[tune_index:tune_index + 2]

        if level == "auto":
            # Find the index of '-tune' in the command and remove it along with its argument
            tune_index = ffmpeg_command.index('-level:v')
            del ffmpeg_command[tune_index:tune_index + 2]

        if profile == "auto":
            # Find the index of '-tune' in the command and remove it along with its argument
            tune_index = ffmpeg_command.index('-profile:v')
            del ffmpeg_command[tune_index:tune_index + 2]

        if pixformat == "auto":
            # Find the index of '-tune' in the command and remove it along with its argument
            tune_index = ffmpeg_command.index('-pix_fmt')
            del ffmpeg_command[tune_index:tune_index + 2]
        
        # Execute the command and wait for it to complete
        return_code = subprocess.call(ffmpeg_command)
        if return_code == 0:
            messagebox.showinfo("Success", "Encoding successful!")
        else:
            messagebox.showerror("Error", "Encoding failed!")

def update_crf_label(value):
    # Round the value to the nearest 0.5 increment
    crf_value_rounded = round(float(value) * 2) / 2
    crf_label.config(text="CRF: " + str(crf_value_rounded))

def close_window(event=None):
    root.destroy()

def about_box():
    messagebox.showinfo("About", "H.264 Encoder v1.0.0\nFFmpeg 6.1.1\n\nCopyright © 2024 Kağan Kerimoğlu")
    root.focus_force()  # Bring focus back to the main window

def open_website():
    webbrowser.open("https://trac.ffmpeg.org/wiki/Encode/H.264")

def show_readme_dialog():
            # Path to the encoder executable        
    readme_document = os.path.join(os.path.dirname(__file__), 'readme.pdf')
    if os.name == 'posix':  # for MacOS 
        subprocess.Popen(['open', readme_document])
    else:  # for Windows
        subprocess.Popen(['start', readme_document], shell=True)

def check_for_updates():
    try:
        # Display a progress bar in a new window
        checkforupdates_window = tk.Toplevel()
        checkforupdates_window.title("")
        checkupdatebox_width = int(app_width/2)
        checkupdatebox_height = int(app_height/2.8)
        checkupdatebox_x = (screen_width/2) - (checkupdatebox_width/2)
        checkupdatebox_y = (screen_height/2) - (checkupdatebox_height/0.3)

        # Position about window
        checkforupdates_window.geometry("{}x{}+{}+{}".format(int(checkupdatebox_width),int(checkupdatebox_height),int(checkupdatebox_x),int(checkupdatebox_y)))
        checkforupdates_window.resizable(False, False)
        checkforupdates_window.focus_force()


        progress_label = ttk.Label(checkforupdates_window, text="Checking for updates...")
        progress_label.pack(pady=(10,5))

        progress_bar_checkupdate = ttk.Progressbar(checkforupdates_window, length=220)
        progress_bar_checkupdate.pack(pady=(0,10))
        
        progress_bar_checkupdate["value"] = 25
        checkforupdates_window.update()

        # Make a request to the server to get the latest version information
        response = requests.get("https://raw.githubusercontent.com/kagankerimoglu/h.264-encoder/main/version.json")

        progress_bar_checkupdate["value"] = 50
        checkforupdates_window.update()
        
        # Do further processing with response data
        progress_bar_checkupdate["value"] = 100
        checkforupdates_window.update()

        # Wait 1 seconds before closing the progress bar window
        time.sleep(1)

        # Close the progress bar window
        checkforupdates_window.destroy()

        if response.status_code == 200:
            version_info = response.json()
            latest_version = version_info.get("version")

            if current_version >= latest_version:
                messagebox.showinfo("Info", f"You are up-to-date!\n\n{current_version}\nis currently the newest version available.")

            # Compare the latest version with the current version of the app
            if latest_version > current_version:
                # Prompt the user to update
                result = messagebox.askyesno("Update Available", f"A new version is available\n{latest_version}\n\nWould you like to update now?")
                root.focus_force()

                # systeminfo
                operating_system = platform.system()
                processortype = platform.machine()
                systeminfo = operating_system+processortype
            
                if result:
                    # Open the download link for the update in a web browser
                    if systeminfo == "Darwinarm64":
                        webbrowser.open_new(f"https://github.com/kagankerimoglu/Test/releases/download/v{latest_version}/testfileupdate_{latest_version}_macos_arm64.dmg")
                        webbrowser.open_new(f"https://github.com/kagankerimoglu/Test/releases/tag/v{latest_version}")
                    if systeminfo == "Darwinx86_64":
                        webbrowser.open_new(f"https://github.com/kagankerimoglu/Test/releases/download/v{latest_version}/testfileupdate_{latest_version}_macos_arm64.dmg")
                        webbrowser.open_new(f"https://github.com/kagankerimoglu/Test/releases/tag/v{latest_version}")    

    except:
        messagebox.showinfo("Info", "Update Failed!\n\nPlease Try Later\nor\nContact Support")
        checkforupdates_window.destroy()

def check_for_updates_at_start():
    response = requests.get("https://raw.githubusercontent.com/kagankerimoglu/Test/main/version.json")
    if response.status_code == 200:
        version_info = response.json()
        latest_version = version_info.get("version")
        if current_version >= latest_version:
            pass
        if latest_version > current_version:
            # Prompt the user to update
            result = messagebox.askyesno("Update Available", f"A new version is available\n{latest_version}\n\nWould you like to update now?")
            operating_system = platform.system()
            processortype = platform.machine()
            systeminfo = operating_system+processortype
            if result:
                if systeminfo == "Darwinarm64":
                    webbrowser.open_new(f"https://github.com/kagankerimoglu/Test/releases/download/v{latest_version}/testfileupdate_{latest_version}_macos_arm64.dmg")
                    webbrowser.open_new(f"https://github.com/kagankerimoglu/Test/releases/tag/v{latest_version}")
                if systeminfo == "Darwinx86_64":
                    webbrowser.open_new(f"https://github.com/kagankerimoglu/Test/releases/download/v{latest_version}/testfileupdate_{latest_version}_macos_arm64.dmg")
                    webbrowser.open_new(f"https://github.com/kagankerimoglu/Test/releases/tag/v{latest_version}")    

############################################## GUI CONFIGURATION ##############################################

root = tk.Tk()
root.title("H.264 Encoder")

# Hide the root window initially
root.withdraw()

# Set virtual width and height for root.winfo
width = int(448)
height = int(540)

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# calculate x and y coordinates for the Tk root window to be centered on the screen
app_width = (screen_width/2) - (width/2)
app_height = (screen_height/2) - (height/2)

# Position the root window
root.geometry("+%d+%d" % (app_width, app_height))
root.resizable(False, False)

check_for_updates_at_start()

# Call open_file() to open file dialog when the program starts
open_file()

# Create a frame to contain the dropdown menus
dropdown_frame = tk.Frame(root)
dropdown_frame.pack()

# Preset and Tune Dropdown Menus (side by side)
preset_label = tk.Label(dropdown_frame, text="Preset")
preset_label.grid(row=0, column=0, padx=(0, 0), pady=(20,0))

preset_value = tk.StringVar()
preset_value.set("veryslow")
preset_menu = tk.OptionMenu(dropdown_frame, preset_value,
                            "superfast", "veryfast", "faster", "fast",
                            "medium", "slow", "slower", "veryslow", "placebo")
preset_menu.grid(row=1, column=0)

tune_label = tk.Label(dropdown_frame, text="Tune")
tune_label.grid(row=0, column=1, padx=(0,0), pady=(20,0))

tune_value = tk.StringVar()
tune_value.set("film")
tune_menu = tk.OptionMenu(dropdown_frame, tune_value,
                          "none", "film", "animation", "grain", "stillimage", "psnr", "ssim", "fastdecode", "zerolatency")
tune_menu.grid(row=1, column=1)

# Level and Profile Dropdown Menus (below, side by side)
level_profile_frame = tk.Frame(root)
level_profile_frame.pack()

level_label = tk.Label(level_profile_frame, text="Level")
level_label.grid(row=0, column=0, padx=(0, 0), pady=(5,0))

level_value = tk.StringVar()
level_value.set("4.2")
level_menu = tk.OptionMenu(level_profile_frame, level_value,
                           "auto", "3.0", "3.1", "3.2", "4.0", "4.1", "4.2", "5.0", "5.1", "5.2")
level_menu.grid(row=1, column=0)

profile_label = tk.Label(level_profile_frame, text="Profile")
profile_label.grid(row=0, column=1, padx=(0, 0), pady=(5,0))

profile_value = tk.StringVar()
profile_value.set("high")
profile_menu = tk.OptionMenu(level_profile_frame, profile_value,
                             "auto", "baseline", "main", "high", "high10", "high422", "high444")
profile_menu.grid(row=1, column=1, padx=(0, 0))

# Subsampling Dropdown Menu
subsampling_label = tk.Label(level_profile_frame, text="Pixel Format")
subsampling_label.grid(row=0, column=2, padx=(0, 0), pady=(5,0))

subsampling_value = tk.StringVar()
subsampling_value.set("yuv420p")
subsampling_menu = tk.OptionMenu(level_profile_frame, subsampling_value,
                                 "auto", "yuv420p", "yuv422p", "yuv444p", "yuv420p10le", "yuv422p10le", "yuv444p10le")
subsampling_menu.grid(row=1, column=2, padx=(0, 0))

# CRF Slider
crf_label = tk.Label(root, text="CRF: 15")
crf_label.pack(pady=(8,0), padx=(25,25))

crf_value = tk.StringVar(value="15")  # Set default value to 15
crf_slider = ttk.Scale(root, from_=0, to=30, orient=tk.HORIZONTAL,
                       length=400, variable=crf_value, command=update_crf_label)
crf_slider.pack(padx=(25,25), pady=(0,5))


selectedfile_label = tk.Label(root, text="Clip Name", foreground="#1988F7")
selectedfile_label.pack(pady=(0,0))

filename_label = tk.Label(root, text=filename)
if len(filename) > 48:
    filename = filename[:45] + "..."
filename_label.config(text=filename)
filename_label.pack(pady=(0,10))

################################################### MENU BAR ###################################################

# Encode Button
encode_button = tk.Button(root, text="Encode", command=encode)
encode_button.pack(pady=(0,25))

# Create the menu bar
menubar = Menu(root)

# Default app menu override
app_menu = Menu(menubar, name='apple', tearoff=0)
menubar.add_cascade(menu=app_menu)

# Add custom file menu
file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File",menu=file_menu)

# Add options to file menu
file_menu.add_command(label="Open File..."+" "*43+"⌘ O",command=lambda: open_file())
file_menu.add_command(label="Save As..."+" "*45+"⌘ S", command=lambda:encode())
file_menu.add_separator()
file_menu.add_command(label="Minimize"+" "*47+"⌘ M", command=root.iconify)
file_menu.add_command(label="Close"+" "*52+"⌘ W", command=lambda: close_window())

root.bind("<Command-O>", lambda event: open_file())
root.bind("<Command-o>", lambda event: open_file())
root.bind("<Command-S>", lambda event: encode())
root.bind("<Command-s>", lambda event: encode())
root.bind("<Command-W>", lambda event: close_window())
root.bind("<Command-w>", lambda event: close_window())
root.bind("<Command-M>", lambda event: root.iconify())
root.bind("<Command-m>", lambda event: root.iconify())

# Default about dialog override
app_menu.add_command(label='About ', command=about_box)
app_menu.add_separator()

app_menu.add_command(label='Check for Updates...', command=check_for_updates)

# Add custom help menu
help_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=help_menu)

# Add an "About" option to the "Help" menu
help_menu.add_command(label="Documentation", command=lambda: show_readme_dialog())
help_menu.add_command(label="H.264 Encoding Guide", command=lambda: open_website())

root.config(menu=menubar)

root.mainloop()