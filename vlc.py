import vlc
# from time import sleep



Instance = vlc.Instance()

player = vlc.MediaPlayer("r-1.mp3")
player.play()

# player = Instance.media_player_new()
# Media = Instance.media_new('http://fsi.stanford.edu/sites/default/files/video_4.mp4')
# Media.get_mrl()
# player.set_media(Media)
# player.play()


# sleep(5) # Or however long you expect it to take to open vlc
# while player.is_playing():
#      sleep(1)