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

def download_video():
    url = link.get()
    if not is_valid_youtube_url(url):
        finished_label.configure(text="Invalid YouTube link", text_color="red")
        return
    try:
        yt_obj = YouTube(url, on_progress_callback = on_progress)
        finished_label.configure(text="Downloading video...")
        title.configure(text=yt_obj.title)

        video = yt_obj.streams.get_highest_resolution() #Gets the highest resolution video stream
        video.download() #Downloads the video

        finished_label.configure(text="Download finished!")
    except Exception as e:
        finished_label.configure(text="Unable to download video", text_color="red")
    
#System settings
customtkinter.set_appearance_mode("System") #Makes the window appearance follow the system appearance
customtkinter.set_default_color_theme("blue") #Sets the default color theme to green

#App frame settings
app = customtkinter.CTk()
app.geometry("800x400") #Sets the window size to 800x600
app.title("YouTube Downloader") #Sets the window title to "YouTube Downloader"

#Adding ui elements
title = customtkinter.CTkLabel(app, text="Insert YouTube link:", font=("Arial", 20))
title.pack(padx=10, pady=10)

url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, font=("Arial", 20), textvariable=url_var)
link.pack(padx=10, pady=10)

finished_label = customtkinter.CTkLabel(app, text="", font=("Arial", 20))
finished_label.pack(padx=10, pady=10)

download_button = customtkinter.CTkButton(app, text="Download", font=("Arial", 20), command=lambda: download_video())
download_button.pack(padx=10, pady=10)

#Run app
app.mainloop()