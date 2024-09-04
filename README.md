# Python Youtube Downloader

Simple Python Youtube video and audio downloader with the option of choosing the quality of the downloaded file.

# Installation

Run this command:
sh
pip install -r requirements.txt

while in the directory folder.

NOTE: Python 3+ required.

## Usage

To use the tool just start main.py in any IDE or CLI environments.
You can then paste any Youtube link into the text bar and the available audio and video streams will show up at the bottom of the window, you can then select the one you want from the dropdown menu and click download to select the download file destination.
The progress of the procedure will be visible in the included progress bar and eventual errors will show up just above the download button.

NOTE: Available video streams may be of low quality because of the tool's capacity to only download streams which include both audio and video, this is because Youtube handles higher quality video streams by combining two different streams, one for audio and one for video.

## Example images  

Valid link:  
![valid link](https://github.com/user-attachments/assets/8f332ccc-94e5-4c86-bcc7-46c5a527ed7a)

Invalid link:  
![invalid link](https://github.com/user-attachments/assets/0add8bf8-1ec8-4bf5-bb54-551ba204d625)

Video downloaded:  
![video downloaded](https://github.com/user-attachments/assets/ac61f3fa-8819-44ef-8956-6c8d8641e609)
