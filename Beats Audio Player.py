import os
import threading
import time
import tkinter.messagebox
from tkinter import *
#this statement imports tkinter ie make is usable in python,tkinter is a preinstalled GUI application with python.
from tkinter import filedialog

from tkinter import ttk
from ttkthemes import themed_tk as tk
import pygame
from mutagen.mp3 import MP3
from pygame import mixer
#pygame is Python package full of game modules we are using a bg audio player module named mixer

root = tk.ThemedTk()
root.get_themes()
# Returns a list of all themes that can be set
root.set_theme("radiance")
# Sets an available theme

# Fonts - Arial (corresponds to Helvetica), Courier New (Courier), Comic Sans MS, Fixedsys,
# MS Sans Serif, MS Serif, Symbol, System, Times New Roman (Times), and Verdana
#
# Styles - normal, bold, roman, italic, underline, and overstrike.

statusbar = ttk.Label(root, text="Welcome to Beats Music Player", relief=SUNKEN, anchor=W, font='Times 14 roman',foreground='cyan')
statusbar.pack(side=BOTTOM, fill=X)

# Create the menubar
menubar = Menu(root)
root.config(menu=menubar)

# Create the submenu

subMenu = Menu(menubar, tearoff=0)
i=0
playlist = []
index=0

# playlist - contains the full path + filename
# playlistbox - contains just the filename
# Fullpath + filename is required to play the music inside play_music load function

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

    mixer.music.queue(filename_path)


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)   
    index += 1
    

menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo('About Beats', 'This is a music player build using Python Tkinter by @dhruvohra')


subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)

mixer.init()  # initializing the mixer

root.title("Beats")
root.iconbitmap(r'C:\Users\DHRUV VOHRA\Desktop\Beats Audio Player\images\beats.ico')

# Root Window - StatusBar, LeftFrame, RightFrame
# LeftFrame - The listbox (playlist)
# RightFrame - TopFrame,MiddleFrame and the BottomFrame

leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=30, pady=30)

playlistbox = Listbox(leftframe)
playlistbox.pack()

addBtn = ttk.Button(leftframe, text="+ Add", command=browse_file)
addBtn.pack(side=LEFT)


def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)
    statusbar['text'] = "Music deleted"

delBtn = ttk.Button(leftframe, text="- Del", command=del_song)
delBtn.pack(side=LEFT)

rightframe = Frame(root)
rightframe.pack(pady=30)

topframe = Frame(rightframe)
topframe.pack()

lengthlabel = ttk.Label(topframe, text='Total Length : --:--')
lengthlabel.pack(pady=5)

currenttimelabel = ttk.Label(topframe, text='Current Time : --:--', relief=GROOVE)
currenttimelabel.pack()

TimeLeftlabel = Label(topframe, text='Time Left : --:--', relief=GROOVE)
TimeLeftlabel.pack()


def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()
    t2 = threading.Thread(target=TimeLeft_count, args=(total_length,))
    t2.start()

def start_count(t):
    global paused
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    # Continue - Ignores all of the statements below it. We check if music is paused or not.
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1

def TimeLeft_count(t):
    global paused
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    # Continue - Ignores all of the statements below it. We check if music is paused or not.
    while t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(t, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            TimeLeftlabel['text'] = "Time Left" + ' - ' + timeformat
            time.sleep(1)
            t -= 1

def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'Beats could not find the file. Please check again.')


def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"


def nextsong():
    global paused
    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    stop_music()
    time.sleep(1)
    global play_it
    global selected_song
    global i
    
    
    #print(index)
    if i<len(playlist)-1:
        i+=1
        pygame.mixer.music.load(playlist[i])
        pygame.mixer.music.play()
        play_it=playlist[i]
        statusbar['text'] = "Playing next song" + ' - ' + os.path.basename(play_it)
        time.sleep(1)
        show_details(play_it)
    else:
        i=0
        pygame.mixer.music.load(playlist[i])
        pygame.mixer.music.play()
        play_it=playlist[i]
        statusbar['text'] = "Playing next song" + ' - ' + os.path.basename(play_it)
        time.sleep(1)
        show_details(play_it)
    '''updatelabel()
    selected_song +=1
    play_it = playlist[selected_song]
    mixer.music.load(play_it)
    mixer.music.play()
    '''
 
def prevsong():
    stop_music()
    time.sleep(1)
    global index
    global i
    if i>0:
        i-=1
        pygame.mixer.music.load(playlist[i])
        pygame.mixer.music.play()
        play_it=playlist[i]
        statusbar['text'] = "Playing prev song" + ' - ' + os.path.basename(play_it)
        show_details(play_it)
    else:
        i=len(playlist)-1
        pygame.mixer.music.load(playlist[i])
        pygame.mixer.music.play()
        play_it=playlist[i]
        statusbar['text'] = "Playing next song" + ' - ' + os.path.basename(play_it)
        time.sleep(1)
        show_details(play_it)
    '''
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    index -= 1
    mixer.music.load(selected_song[index])
    mixer.music.play()
    '''
    
paused = FALSE


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"


def replay_music():
    play_music()
    statusbar['text'] = "Music Replayed"


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)
    # set_volume of mixer takes value only from 0 to 1. Example - 0, 0.1,0.55,0.54.0.99,1


muted = FALSE


def mute_music():
    global muted
    if muted:  # Unmute the music
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image=volumePhoto)
        scale.set(70)
        muted = FALSE
        statusbar['text'] = "Music Unmuted"
    else:  # mute the music
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE
        statusbar['text'] = "Music Muted"


middleframe = Frame(rightframe)
middleframe.pack(pady=30, padx=30)

playPhoto = PhotoImage(file=r'C:\Users\DHRUV VOHRA\Desktop\Beats Audio Player\images\play.png')
playBtn = ttk.Button(middleframe, image=playPhoto, command=play_music)
playBtn.grid(row=0, column=0, padx=10)

stopPhoto = PhotoImage(file=r'C:\Users\DHRUV VOHRA\Desktop\Beats Audio Player\images\stop.png')
stopBtn = ttk.Button(middleframe, image=stopPhoto, command=stop_music)
stopBtn.grid(row=0, column=1, padx=10)

pausePhoto = PhotoImage(file=r'C:\Users\DHRUV VOHRA\Desktop\Beats Audio Player\images\pause.png')
pauseBtn = ttk.Button(middleframe, image=pausePhoto, command=pause_music)
pauseBtn.grid(row=0, column=2, padx=10)

photo1= PhotoImage(file=r"C:\Users\DHRUV VOHRA\Desktop\Beats Audio Player\images\next song.png")
#photoimage=photo.subsample(1,1)
nextbutton = ttk.Button(middleframe,text = 'Next Song',image=photo1,command=nextsong)
nextbutton.grid(row=0, column=3, padx=10)
 
photo2= PhotoImage(file=r"C:\Users\DHRUV VOHRA\Desktop\Beats Audio Player\images\prev song.png")
#photoimage=photo.subsample(1,1)
previousbutton = ttk.Button(middleframe,text = 'Previous Song',image=photo2,command=prevsong)
previousbutton.grid(row=0, column=4, padx=10)

#nextbutton.bind("<Button-1>",nextsong)
#previousbutton.bind("<Button-1>",prevsong)

# Bottom Frame for volume, replay, mute etc.

bottomframe = Frame(rightframe)
bottomframe.pack()

replayPhoto = PhotoImage(file=r'C:\Users\DHRUV VOHRA\Desktop\Beats Audio Player\images\rewind.png')
replayBtn = ttk.Button(bottomframe, image=replayPhoto, command=replay_music)
replayBtn.grid(row=0, column=0)

mutePhoto = PhotoImage(file=r'C:\Users\DHRUV VOHRA\Desktop\Beats Audio Player\images\mute.png')
volumePhoto = PhotoImage(file=r'C:\Users\DHRUV VOHRA\Desktop\Beats Audio Player\images\volume.png')
volumeBtn = ttk.Button(bottomframe, image=volumePhoto, command=mute_music)
volumeBtn.grid(row=0, column=1)

scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)  # implement the default value of scale when music player starts
mixer.music.set_volume(0.7)
scale.grid(row=0, column=2, pady=15, padx=30)


def on_closing():
    stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
#mainloop is infinite loop which doesnt allows the window to get closed after execution.

