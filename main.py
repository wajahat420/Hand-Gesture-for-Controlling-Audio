
import vlc 
import subprocess

song1 = vlc.MediaPlayer("/home/wajahat/Downloads/sham_tayariyan.mp3")
song2 = vlc.MediaPlayer("/home/wajahat/Downloads/hussain_badshah.mp3")



playlist = ["/home/wajahat/Downloads/sham_tayariyan.mp3", "/home/wajahat/Downloads/hussain_badshah.mp3"]
"""

#for song in playlist:
player = vlc.MediaPlayer(playlist[0])
player.play()

while True:
    inp =  input("Do you want to play audio: ")
    if(inp == "play"):
        player.play()
    elif inp == "stop":            
        player.stop()
    elif inp == "prev":
        player.previous_chapter()
    elif  inp == "next":
        player.previous_chapter()
    else:
        break
"""

#player = vlc.MediaPlayer()
#song1.play()
#time.sleep(10)


import time

inst = vlc.Instance()
sub_player = inst.media_player_new()
player = inst.media_list_player_new()
mediaList = inst.media_list_new(playlist)
player.set_media_list(mediaList)
volume = 150
sub_player.audio_set_volume(volume)
sub_player.play()
playing = set([1,2,3,4])
player.play()
while player.get_state() in playing:
    time.sleep(1)

