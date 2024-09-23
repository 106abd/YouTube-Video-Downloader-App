# Date Created(MM/DD/YY): 08/04/2022
# Date Last Modified(MM/DD/YY): 09/06/2022
# Software Description: A program that allows videos to be downloaded from any YouTube URL.

# GUI Imports
from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import filedialog
from PIL import Image, ImageTk
from pytubefix import YouTube
from moviepy.editor import VideoFileClip
from urllib.request import urlopen
from threading import Thread
import time


# Functions
def createDownloadThread():  # Create a thread dedicated to downloading files
    # Initialize global variables
    global downloadCheck  # Initialize the download checking variable
    global linkField  # Initialize the link field widget variable

    # Get video link via URL entered in link field
    userLink = linkField.get()  # Store the link in a variable
    # Get selected path
    userPath = canvas.itemcget(pathLabel, 'text')  # Retrieve the path from the path label and store it in a variable

    if not downloadCheck and validifyLink(userLink) and validifyPath(userPath):  # Check if a download is already in
        # progress and if the YouTube link and download path are valid
        downloadCheck = True  # Set to true so download cannot be interrupted
        downloadThread = Thread(target=downloadFile, args=(userLink, userPath,))  # Initialize the download file thread
        downloadThread.start()  # Execute the thread


def createProgressBarThread(self, chunk, bytes_remaining):  # Create a thread dedicated to updating the progress bar
    progressBarThread = Thread(target=updateProgressBar, args=(bytes_remaining,))  # Initialize the progress bar update
    # thread
    progressBarThread.start()  # Execute the thread


def displayThumbnail(userLink):  # Scan, render, and display thumbnail given the YouTube video link
    thumbnailURL = YouTube(userLink).thumbnail_url  # Store the thumbnail link in a variable
    thumbnailImage = urlopen(thumbnailURL)  # Retrieve the binary data of the thumbnail
    filteredThumbnail = Image.open(thumbnailImage)  # Create image using the binary data of the thumbnail
    filteredThumbnail = filteredThumbnail.resize((260, 195), Image.LANCZOS)  # Scale image to the (x,y) dimensions
    filteredThumbnail = filteredThumbnail.crop((0, 20, 260, 175))  # Crop out black bars
    thumbnailRender = ImageTk.PhotoImage(filteredThumbnail)  # Render the filtered image
    thumbnailDisplay = Label(image=thumbnailRender)  # Create label for the rendered image
    thumbnailDisplay.image = thumbnailRender  # Assign rendered image to image property of the label
    thumbnailDisplay.pack()  # Pack rendered image
    thumbnailDisplay.place(x=12, y=535)  # Display rendered image in the following (x,y) coordinates


def downloadFile(userLink, userPath):  # Download the file
    # Reveal progress bar with 0% completion
    progressBarBookend(0)  # Calling the bookend function to reset progress bar

    # Call progress bar creation function in a new thread
    onProgressCallBack = YouTube(userLink, on_progress_callback=createProgressBarThread)  # Sends progress information
    # to the function createProgressBarThread() when downloading commences

    # Download video
    print("Commencing download")
    webVideo = onProgressCallBack.streams.get_highest_resolution().download(userPath)  # Commencing download to path
    downloadedVideo = VideoFileClip(webVideo)
    downloadedVideo.close()

    # Show progress bar with 100% completion before removal
    progressBarBookend(1)  # Calling the bookend function to complete progress bar
    print("Download complete")

    # Set global variable to true
    global downloadCheck  # Initialize global variable
    downloadCheck = False  # Set to false so download can commence again


def previewStats():  # Preview the stats of the video via the entered URL in the link field
    # Get video link via URL entered in link field
    userLink = linkField.get()  # Store the link in a variable

    if validifyLink(userLink):  # Check to see if the YouTube link is valid to inform user of errors
        # Displaying video thumbnail
        displayThumbnail(userLink)  # Calling function to display the YouTube thumbnail via its YouTube link

        # Displaying Video Title
        canvas.create_text(295, 545, text="Title:", font=('Arial', 9))  # Create "title: " label at the (x,y) coordinate
        canvas.create_text((311, 538), text=YouTube(userLink).title, font=('Arial', 9), anchor='nw', width=200)  # Place
        # the video title beside the "title: " label

        # Displaying Channel Name
        canvas.create_text(325, 592, text="Channel Name:", font=('Arial', 9))  # Create "channel name: " label at the
        # (x,y) coordinate
        canvas.create_text(372, 585, text=YouTube(userLink).author, font=('Arial', 9), anchor='nw')  # Place the channel
        # name beside the "Channel name: " label

        # Displaying Publication Date
        canvas.create_text(329, 639, text="Publication Date:", font=('Arial', 9))  # Create "Publication Date: " label
        # at the (x,y) coordinate
        publicationDate = YouTube(userLink).publish_date
        canvas.create_text(379, 639, text=publicationDate, font=('Arial', 9), anchor='w')  # Place the
        # publication date beside the "Publication Date: " label

        # Displaying View Count
        canvas.create_text(301, 686, text="Views:", font=('Arial', 9))  # Create "views: " label at the (x,y) coordinate
        canvas.create_text(320, 686, text=YouTube(userLink).views, font=('Arial', 9), anchor='w')  # Place the view
        # count number beside the "views: " label
        print("Previewing stats")


def progressBarBookend(bookend):  # Set progress bar value depending on if the progress is commencing or finishing
    if bookend == 0:  # If  the progress bar is supposed to be 0
        # Place empty progress bar
        progressBar.pack()  # Packing the progress bar
        progressBar['value'] = 0  # Set progress bar status to 0 at the beginning of the download
        progressBar.place(x=100, y=450)  # Place progress bar in the following (x,y) coordinate
    elif bookend == 1:  # If  the integer sent is supposed to be 1
        # Update and hide progress bar from screen
        progressBar['value'] = 100  # Confirm progress bar is shown to be at 100% when download is complete
        time.sleep(1)  # Wait 1 second so user can observe the progress bar
        progressBar.place(x=100, y=1000)  # Hide progress bar


def selectPath():  # Select which path the video should be downloaded to
    path = filedialog.askdirectory()  # Open window to select path from computer directories
    canvas.itemconfig(pathLabel, text=path, fill="black")  # Change text to the selected directory
    print("New path selected")


def validifyLink(userLink):  # Validify a YouTube link given the link the user has entered
    # Initialize global variables
    global linkField  # Initializing the link field global variable

    try:  # Check if the user entered link is a valid YouTube link
        YouTube(userLink)  # Checking to see if the YouTube module can access the link
        linkField.configure({"background": "white"})  # Link field background colour turns white
        return True  # The YouTube link the user has entered is valid
    except:  # If the user entered link is not valid
        print("Link Error")
        linkField.configure({"background": "pink"})  # Link field background colour turns pink
        return False  # The YouTube link the user has entered is not valid


def validifyPath(userPath):  # Validify the download path selected by the user
    # Initialize global variables
    global pathLabel  # Initializing the path field global variable

    if userPath == "Select Path For Download" or userPath == "" or userPath == "Please Choose A Path":  # If the path is
        # one of the system generated messages
        print("Path Error")
        canvas.itemconfig(pathLabel, text="Please Choose A Path", fill="Red")  # Path text turns red and displays an
        # error message
        return False  # The user selected download path is not valid
    else:
        return True  # The user selected download path is valid


def updateProgressBar(bytesRemaining):  # Update the progress bar everytime a chunk is downloaded
    # Update progress bar
    userLink = linkField.get()  # Store the link in a variable
    videoSize = YouTube(userLink).streams.get_highest_resolution().filesize  # Store video size in a variable
    if progressBar['value'] < 100:  # Update only if the progress bar isn't full
        print("Updating progress bar")
        barFilled = ((videoSize - bytesRemaining) / videoSize) * 100  # Equation representing amount of bytes downloaded
        progressBar['value'] = barFilled  # Represent downloaded bytes in the progress bar
        window.update_idletasks()  # Update the progress bar


# Initialize variables
downloadCheck = False  # Variable to keep track of if a download is already ongoing

# Creating the GUI Window
window = Tk()  # Creating the window object
iconImage = "Icon.ico"  # The image displayed on the top left of the window select bar
window.iconbitmap(iconImage)  # Display the icon image as the application's icon
title = window.title(' YouSave - YouTube Video Downloader')  # Window title on the top left
canvas = Canvas(window, width=500, height=700)  # Window size
canvas.configure(background='pink')  # Background colour
window.resizable(0, 0)  # Disable enlarging window
canvas.pack()  # Applying the GUI window properties

# Creating GUI Elements for the Window
# --Background Image
backgroundImage = PhotoImage(file='Background.png')  # Initializing the background image to use
canvas.create_image(250, 350, image=backgroundImage)  # Centering the background image in the window

# --Image Logo
logoImage = PhotoImage(file='Logo.png')  # Initializing the logo image to use
canvas.create_image(245, 80, image=logoImage)  # Centering the logo in the window

# --Link Field
linkField = Entry(window, width=50)  # Creating the link field where the user will enter the YouTube link
canvas.create_text(250, 170, text="Enter YouTube Link: ", font=('Arial bold', 15))  # Text label above the link field

# --Preview Button
previewButtonImage = PhotoImage(file="PreviewButton.png")
previewButton = Button(window, image=previewButtonImage, command=previewStats, borderwidth=0)  # Creating the preview
# button which users click to confirm video stats from entered URL

# --Download Path Selection
selectPathButtonImage = PhotoImage(file="SelectPathButton.png")
selectButton = Button(window, image=selectPathButtonImage, command=selectPath, borderwidth=0)  # Creating the select
# button which users click to select download path
pathLabel = canvas.create_text(250, 280, text="Select Path For Download", font=('Arial bold', 15))  # Text label above
# the select button

# --Download Buttons
downloadButtonImage = PhotoImage(file="DownloadButton.png")
downloadButton = Button(window, image=downloadButtonImage, command=createDownloadThread, borderwidth=0)  # Creating
# download button which users click to begin download

# -- Progress Bar
progressBar = Progressbar(window, orient=HORIZONTAL, length=300, mode='determinate')  # Creating the progress bar (not
# packed)

# --Adding GUI Elements to the Window
canvas.create_window(230, 220, window=linkField)  # Centering the link field in the window
canvas.create_window(440, 220, window=previewButton)  # Placing the preview button beside the link field
canvas.create_window(250, 330, window=selectButton)  # Centering the select button in the window
canvas.create_window(250, 390, window=downloadButton)  # Centering the download button in the window

window.mainloop()  # Execute window
