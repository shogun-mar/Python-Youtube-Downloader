import tkinter, customtkinter, re
from pytubefix import YouTube
from pytubefix.cli import on_progress

def is_valid_youtube_url(url):
    # Simple validation for a YouTube URL
    youtube_regex = ( #The r'string' is a raw string, which means that the backslashes are treated as literal characters
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    
    return bool(re.match(youtube_regex, url))

def sort_resolutions(resolutions):
    # Parse resolutions to extract the numerical part and sort them in descending order
    sorted_resolutions = sorted(resolutions, key=lambda x: int(x[:-1]), reverse=True)
    return sorted_resolutions

def get_video_resolutions(url):
    #Fetch available resolutions for a YouTube video.
    global yt_obj
    yt_obj = YouTube(url, on_progress_callback=on_progress)
    resolutions = []
    for stream in yt_obj.streams.filter(progressive=True, only_audio=False):
        temp = stream.resolution + "Progressive" #Adds the word "Progressive" to the resolution to differentiate it from the other resolutions
        resolutions.append(temp)  # Add the resolution to the set
    for stream in yt_obj.streams.filter(adaptive=True, only_audio=False):
        temp = stream.resolution + "Adaptive" #Adds the word "Adaptive" to the resolution to differentiate it from the other resolutions
        resolutions.append(temp)  # Add the resolution to the set
    print(resolutions)
    #return sort_resolutions(resolutions)  # Return a sorted list of resolutions

def download_video():
    try:
        finished_label.configure(text="Downloading video...", text_color="white")
        title.configure(text=yt_obj.title)
        video = yt_obj.streams.get_highest_resolution() #Gets the highest resolution video stream
        video.download() #Downloads the video
        finished_label.configure(text="Download finished!", text_color="white")
    except Exception as e:
        finished_label.configure(text="Unable to download video", text_color="red")
    
def update_settings_widgets(*args):
    #Update resolutions dropdown based on the YouTube link input.
    global resolution_dropdown
    url = link_input.get()
    if is_valid_youtube_url(url):
        resolutions = get_video_resolutions(url)
        resolution_dropdown.configure(values=resolutions)  # Update the dropdown values
        resolution_dropdown.set(resolutions[0])  # Set the first resolution as the default selection
        resolution_dropdown.pack(padx=10, pady=10)  # Make the dropdown is visible
        resolution_dropdown.update()  # Forcefully update the dropdown
        finished_label.configure(text="", text_color="white") # Clear the finished label
        download_button.configure(state="normal")  # Enable the download button
    else:
        resolution_dropdown['values'] = [] # Clear the dropdown values
        resolution_dropdown.pack_forget()  # Hide the dropdown if the URL is invalid
        download_button.configure(state="disabled")
        finished_label.configure(text="Invalid YouTube link", text_color="red")

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize #Total size of the video in bytes
    bytes_downloaded = total_size - bytes_remaining #Bytes downloaded so far
    completion_percentage = int((bytes_downloaded / total_size) * 100) #Percentage of the video downloaded
    progress_percentage.configure(text=str(completion_percentage) + "%") #Sets the progress percentage label to the completion percentage
    progress_percentage.update() #Updates the progress percentage label
    progress_bar.set(completion_percentage / 100) #Sets the progress bar to the completion percentage
    progress_bar.update() #Updates the progress bar

#System settings
customtkinter.set_appearance_mode("System") #Makes the window appearance follow the system appearance
customtkinter.set_default_color_theme("blue") #Sets the default color theme to green

#App frame settings
app = customtkinter.CTk()
app.geometry("800x400") #Sets the window size to 800x600
app.title("YouTube Downloader") #Sets the window title to "YouTube Downloader"

#Custom font
custom_font = customtkinter.CTkFont(family="Cabin-Regular.ttf", size=20)

#Adding ui elements
title = customtkinter.CTkLabel(app, text="Insert YouTube link:", font = custom_font)
title.pack(padx=10, pady=10)

url_entry = tkinter.StringVar()
url_entry.trace_add("write", update_settings_widgets)
link_input = customtkinter.CTkEntry(app, width=400, height=40, font = custom_font, textvariable=url_entry)
link_input.pack(padx=10, pady=10)

finished_label = customtkinter.CTkLabel(app, text="", font = custom_font)
finished_label.pack(padx=10, pady=10)

download_button = customtkinter.CTkButton(app, text="Download", font = custom_font, command = download_video, state="disabled")
download_button.pack(padx=10, pady=10)

progress_percentage = customtkinter.CTkLabel(app, text="Thanks for using my youtube downloader <3", font = custom_font)
progress_percentage.pack(padx=10, pady=10)

progress_bar = customtkinter.CTkProgressBar(app, width=400, height=15)
progress_bar.set(0)
progress_bar.pack(padx=10, pady=10)

resolution_dropdown = customtkinter.CTkComboBox(app)

#global yt object
yt_obj = None

#Run app
app.mainloop()

#        https://www.youtube.com/watch?v=3pdVtlBYtrc