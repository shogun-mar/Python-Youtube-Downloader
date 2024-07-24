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

def get_video_resolutions(url):
    #Fetch available resolutions for a YouTube video.
    global yt_obj
    yt_obj = YouTube(url)
    resolutions = set()  # Use a set to avoid duplicate resolutions
    for stream in yt_obj.streams.filter(progressive=True):
        resolutions.add(stream.resolution)
    for stream in yt_obj.streams.filter(only_video=True, file_extension='mp4'):
        resolutions.add(stream.resolution)
    return sorted(resolutions, reverse = True)  # Return a sorted list of resolutions

def download_video():
    if not is_valid_youtube_url(link_input.get()):
        finished_label.configure(text="Invalid YouTube link", text_color="red")
    else:
        try:
            finished_label.configure(text="Downloading video...", text_color="white")
            title.configure(text=yt_obj.title)
            video = yt_obj.streams.get_highest_resolution() #Gets the highest resolution video stream
            video.download() #Downloads the video
            finished_label.configure(text="Download finished!", text_color="white")
        except Exception as e:
            print(e)
            finished_label.configure(text="Unable to download video", text_color="red")
    
def update_resolutions_dropdown(*args):
    #Update resolutions dropdown based on the YouTube link input.
    url = link_input.get()
    if is_valid_youtube_url(url):
        resolutions = get_video_resolutions(url)
        resolution_dropdown['values'] = resolutions
        resolution_dropdown.set(resolutions[0])  # Set the first resolution as the default selection
        resolution_dropdown.pack(padx=10, pady=10)  # Ensure the dropdown is visible
    else:
        resolution_dropdown.pack_forget()  # Hide the dropdown if the URL is invalid

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
url_entry.trace_add("write", update_resolutions_dropdown)
link_input = customtkinter.CTkEntry(app, width=350, height=40, font = custom_font, textvariable=url_entry)
link_input.pack(padx=10, pady=10)

finished_label = customtkinter.CTkLabel(app, text="", font = custom_font)
finished_label.pack(padx=10, pady=10)

download_button = customtkinter.CTkButton(app, text="Download", font = custom_font, command = download_video)
download_button.pack(padx=10, pady=10)

progress_percentage = customtkinter.CTkLabel(app, text="Thanks for using my youtube downloader <3", font = custom_font)
progress_percentage.pack(padx=10, pady=10)

progress_bar = customtkinter.CTkProgressBar(app, width=350, height=10)
progress_bar.set(0)
progress_bar.pack(padx=10, pady=10)

resolution_dropdown = customtkinter.CTkComboBox(app)

#global yt object
yt_obj = None

#Run app
app.mainloop()

#        https://www.youtube.com/watch?v=PzvPPXdASWo