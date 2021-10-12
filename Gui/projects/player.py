from tkinter import *
import pygame
from tkinter import filedialog
from PIL import ImageTk, Image
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title('MP3 Player')
root.geometry('460x330')

# Initialize Pygame Mixer
pygame.mixer.init()

song_length = 0
current_song, current_song_name = "", ""
song_list = []
paused, stopped, changed = False, False, False


def play_time():
    global song_length, stopped
    song = song_box.get(ACTIVE)
    for i in song_list:
        if f'{song}.mp3' in i:
            song = MP3(i)
            song_length = song.info.length
            converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
            slider_position = int(song_length)
            my_slider.config(to=slider_position, value=0)
            current_time = (pygame.mixer.music.get_pos() / 1000)
            converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
            status_bar.config(
                text=f'Song:  {current_song_name}     Time Elapsed: {converted_current_time}  of  {converted_song_length}  ')

    def change():
        if stopped:
            return
        current_time = (pygame.mixer.music.get_pos() // 1000)
        if pygame.mixer.music.get_busy() and current_time > 0:
            if int(my_slider.get()) == int(song_length):
                status_bar.config(
                    text=f'Song:  {current_song_name}     Time Elapsed: {converted_song_length}  of  {converted_song_length}  ')
            elif paused:
                pass
            elif int(my_slider.get()) == int(current_time):
                my_slider.config(value=int(current_time))
                # status_bar.config(
                #     text=f'Song:  {current_song_name}     Time Elapsed: {converted_current_time}  of  {converted_song_length}  ')

            else:
                # my_slider.config(value=int(my_slider.get()))
                converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))
                status_bar.config(
                    text=f'Song:  {current_song_name}     Time Elapsed: {converted_current_time}  of  {converted_song_length}  ')

                next_time = int(my_slider.get()) + 1
                my_slider.config(value=next_time)
        if converted_song_length == time.strftime('%M:%S', time.gmtime(song_length)):
            status_bar.after(1000, change)

    stopped = False
    change()


def add_song():
    global song_list

    song = filedialog.askopenfilename(initialdir='F:/vishal/python files/PycharmProjects/Gui/songs',
                                      title='Choose A Song', filetypes=(("MP3 Files", "*.mp3"),))
    if song and song not in song_list:
        song_list.append(song)
        song_name = song.split('/')[len(song.split('/')) - 1]
        song_name = song_name.replace(".mp3", "")
        song_box.insert(END, song_name)


def add_many_song():
    global song_list
    songs = filedialog.askopenfilenames(initialdir='F:/vishal/python files/PycharmProjects/Gui/songs',
                                        title='Choose Songs', filetypes=(("MP3 Files", "*.mp3"),))
    for song in songs:
        if song not in song_list:
            song_list.append(song)
            song_name = song.split('/')[len(song.split('/')) - 1]
            song_name = song_name.replace(".mp3", "")
            song_box.insert(END, song_name)


def play():
    global paused, stopped, current_song, current_song_name
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    elif song_box.get(ACTIVE):
        song = song_box.get(ACTIVE)
        for i in song_list:
            if f'{song}.mp3' in i:
                current_song, current_song_name = i, song
                pygame.mixer.music.load(i)
                pygame.mixer.music.play(loops=0)
        my_slider.config(value=0)
        play_time()


def stop():
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)
    status_bar.config(text='')
    my_slider.config(value=0)
    global stopped, song_length
    stopped = True
    song_length = 0


def pause():
    global paused
    pygame.mixer.music.pause()
    paused = True


def next_song():
    global current_song, current_song_name, stopped
    stop()
    status_bar.config(text='')
    my_slider.config(value=0)
    index_ = 0
    for index, i in enumerate(song_list):
        if i == current_song:
            index_ = index
    next_one = index_ + 1
    if song_box.get(next_one):
        song = song_box.get(next_one)
        for i in song_list:
            if f'{song}.mp3' in i:
                current_song, current_song_name = i, song
                pygame.mixer.music.load(i)
                pygame.mixer.music.play(loops=0)
                song_box.selection_clear(0, END)
                song_box.activate(next_one)
                song_box.selection_set(next_one, last=None)
        play_time()
    else:
        next_one = 0
        song = song_list[next_one]
        current_song, current_song_name = song, song_box.get(next_one)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        song_box.selection_clear(0, END)
        song_box.activate(next_one)
        song_box.selection_set(next_one, last=None)
        play_time()


def previous_song():
    global current_song, current_song_name, stopped
    stop()
    status_bar.config(text='')
    my_slider.config(value=0)
    index_ = 0
    for index, i in enumerate(song_list):
        if i == current_song:
            index_ = index
    previous_one = index_ - 1
    if song_box.get(previous_one):
        song = song_box.get(previous_one)
        for i in song_list:
            if f'{song}.mp3' in i:
                current_song, current_song_name = i, song
                pygame.mixer.music.load(i)
                pygame.mixer.music.play(loops=0)
                song_box.selection_clear(0, END)
                song_box.activate(previous_one)
                song_box.selection_set(previous_one, last=None)

        play_time()
    else:
        previous_one = len(song_list) - 1
        song = song_list[previous_one]
        current_song, current_song_name = song, song_box.get(previous_one)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        song_box.selection_clear(0, END)
        song_box.activate(previous_one)
        song_box.selection_set(previous_one, last=None)

        play_time()


def forward():
    global current_song
    current_time = int(my_slider.get())
    set_time = current_time + 15
    my_slider.config(value=set_time)
    pygame.mixer.music.load(current_song)
    pygame.mixer.music.play(loops=0, start=set_time)


def backward():
    global current_song
    current_time = int(my_slider.get())
    set_time = current_time - 15
    my_slider.config(value=set_time)
    pygame.mixer.music.load(current_song)
    pygame.mixer.music.play(loops=0, start=set_time)


def delete_song():
    global song_list
    stop()
    song = song_box.get(ANCHOR)
    for i in song_list:
        if f'{song}.mp3' in i:
            song_list.remove(i)
    song_box.delete(ACTIVE)
    pygame.mixer.music.stop()


def delete_all_songs():
    global song_list
    stop()
    song_box.delete(0, END)
    pygame.mixer.music.stop()
    song_list = []


def slide(x):
    if not paused:
        song = song_box.get(ACTIVE)
        for i in song_list:
            if f'{song}.mp3' in i:
                    pygame.mixer.music.load(i)
                    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))
                    # play_time()


def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())


# Create Master Frame
master_frame = Frame(root)
master_frame.pack(pady=20)

# Create Playlist Box
song_box = Listbox(master_frame, width=60)
song_box.grid(row=0, column=0)

# Define player control Buttons Image

back_btn_img = Image.open('Images//backward.png')
back_btn_img = back_btn_img.resize((40, 37))
back_btn_img = ImageTk.PhotoImage(back_btn_img)

forward_btn_img = Image.open('Images//forward.png')
forward_btn_img = forward_btn_img.resize((40, 37))
forward_btn_img = ImageTk.PhotoImage(forward_btn_img)

play_btn_img = Image.open('Images//play.jpg')
play_btn_img = play_btn_img.resize((40, 37))
play_btn_img = ImageTk.PhotoImage(play_btn_img)

pause_btn_img = Image.open('Images//pause.jpg')
pause_btn_img = pause_btn_img.resize((40, 37))
pause_btn_img = ImageTk.PhotoImage(pause_btn_img)

stop_btn_img = Image.open('Images//stop.jpg')
stop_btn_img = stop_btn_img.resize((40, 37))
stop_btn_img = ImageTk.PhotoImage(stop_btn_img)

next_btn_img = Image.open('Images//next.jpg')
next_btn_img = next_btn_img.resize((40, 37))
next_btn_img = ImageTk.PhotoImage(next_btn_img)

previous_btn_img = Image.open('Images//previous.jpg')
previous_btn_img = previous_btn_img.resize((40, 37))
previous_btn_img = ImageTk.PhotoImage(previous_btn_img)

# Create Player Control Frame
control_frame = Frame(master_frame)
control_frame.grid(row=1, columnspan=3, pady=20)

# Create Volume Frame
volume_frame = LabelFrame(master_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=10)

# Create Player Control Buttons
backward_button = Button(control_frame, image=back_btn_img, borderwidth=0, command=backward)
forward_btn = Button(control_frame, image=forward_btn_img, borderwidth=0, command=forward)
play_btn = Button(control_frame, image=play_btn_img, borderwidth=0, command=play)
pause_btn = Button(control_frame, image=pause_btn_img, borderwidth=0, command=pause)
stop_btn = Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop)
next_btn = Button(control_frame, image=next_btn_img, borderwidth=0, command=next_song)
pre_btn = Button(control_frame, image=previous_btn_img, borderwidth=0, command=previous_song)

pre_btn.grid(row=0, column=0, padx=7)
backward_button.grid(row=0, column=1, padx=7)
stop_btn.grid(row=0, column=2, padx=7)
play_btn.grid(row=0, column=3, padx=7)
pause_btn.grid(row=0, column=4, padx=7)
forward_btn.grid(row=0, column=5, padx=7)
next_btn.grid(row=0, column=6, padx=7)

# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add Song Menu
add_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Add Song", menu=add_song_menu)
add_song_menu.add_command(label="Add One song to Playlist", command=add_song)
add_song_menu.add_command(label="Add Many song to Playlist", command=add_many_song)

remove_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A song From Playlist", command=delete_song)
remove_song_menu.add_command(label="Delete All song From Playlist", command=delete_all_songs)

# options = Menu(my_menu, tearoff=0)
# my_menu.add_cascade(label="options", menu=options)
# options.add_command(label="Loop the current song", command=loop)

status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=0)

my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.grid(row=3, columnspan=2, padx=20)

volume_slider = ttk.Scale(volume_frame, from_=1, to=0, orient=VERTICAL, value=1, command=volume, length=125)
volume_slider.pack(pady=10)

# slider_label = Label(root, text='')
# slider_label.pack()

root.mainloop()
