import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder):
        self.playlist = [f for f in os.listdir(music_folder) if f.endswith(('.wav', '.mp3'))]
        self.folder = music_folder
        self.current_index = 0
        self.is_playing = False
        
        pygame.mixer.init()

    def play_track(self):
        if self.playlist:
            track_path = os.path.join(self.folder, self.playlist[self.current_index])
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.play()
            self.is_playing = True

    def stop_track(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play_track()

    def prev_track(self):
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play_track()

    def get_current_track_name(self):
        if self.playlist:
            return self.playlist[self.current_index]
        return "No tracks found"