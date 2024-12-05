import customtkinter as ctk
from tkinter import messagebox
import time
import threading
import pygame
import os
from mutagen.mp3 import MP3
from track_library import increment_play_count, get_name

class MediaPlayer:
    def __init__(self, playlist, parent_window):
        # Ensure pygame mixer is initialized
        pygame.mixer.init()

        # Create new window
        self.window = ctk.CTkToplevel(parent_window)
        self.window.lift()  # Bring to front
        self.window.attributes('-topmost', True)  # Force to top of the stack
        self.window.focus_set()  # Set focus
        self.window.grab_set()  # Make it modal
        self.window.attributes('-topmost', False)  # Restore default behavior
        self.window.title("Media Player")
        self.window.geometry("500x400")

        # Store playlist from CreateTrackList
        self.playlist = playlist
        self.current_track_index = 0
        self.is_playing = False
        self.progress = 0
        self.current_track_length = 0

        # Configure grid
        self.window.grid_columnconfigure(0, weight=1)

        # Now Playing Label
        self.now_playing_label = ctk.CTkLabel(
            self.window,
            text="Now Playing:",
            font=("Helvetica", 16, "bold")
        )
        self.now_playing_label.pack(pady=(20, 5))

        # Track Info Label
        self.track_info = ctk.CTkLabel(
            self.window,
            text="",
            font=("Helvetica", 14)
        )
        self.track_info.pack(pady=(0, 20))

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(
            self.window,
            width=400,
            height=10,
            corner_radius=5
        )
        self.progress_bar.pack(pady=20)
        self.progress_bar.set(0)

        self.manually_skipped = False  # Flag to indicate a manual skip has occurred
        self.skip_position = 0  # Track the position when manually skipping
        self.start_time = 0  # Track when the skip happened
        self.elapsed_time = 0  # Track the time since the skip
        self.progress_bar.bind("<Button-1>", self.skip_in_track)

        # Time Labels
        self.time_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        self.time_frame.pack(fill="x", padx=50)

        self.current_time = ctk.CTkLabel(
            self.time_frame,
            text="0:00",
            font=("Helvetica", 12)
        )
        self.current_time.pack(side="left")

        self.total_time = ctk.CTkLabel(
            self.time_frame,
            text="0:00",
            font=("Helvetica", 12)
        )
        self.total_time.pack(side="right")

        # Volume Control
        self.volume_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        self.volume_frame.pack(pady=10)

        self.volume_label = ctk.CTkLabel(
            self.volume_frame,
            text="🔊",
            font=("Helvetica", 14)
        )
        self.volume_label.pack(side="left", padx=5)

        self.volume_slider = ctk.CTkSlider(
            self.volume_frame,
            from_=0,
            to=1,
            number_of_steps=100,
            width=200,
            command=self.update_volume
        )
        self.volume_slider.pack(side="left", padx=5)
        self.volume_slider.set(0.5)  # Set default volume to 50%

        # Control Buttons Frame
        self.controls_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        self.controls_frame.pack(pady=20)

        # Previous Button
        self.prev_button = ctk.CTkButton(
            self.controls_frame,
            text="⏮",
            width=60,
            command=self.previous_track,
            corner_radius=20
        )
        self.prev_button.pack(side="left", padx=10)

        # Play/Pause Button
        self.play_button = ctk.CTkButton(
            self.controls_frame,
            text="⏸",
            width=60,
            command=self.toggle_play_pause,
            corner_radius=20,
            fg_color="green"
        )
        self.play_button.pack(side="left", padx=10)

        # Next Button
        self.next_button = ctk.CTkButton(
            self.controls_frame,
            text="⏭",
            width=60,
            command=self.next_track,
            corner_radius=20
        )
        self.next_button.pack(side="left", padx=10)

        # Bind window close event
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Start playing the first track
        self.play_current_track()
        self.start_progress_thread()

    def get_track_path(self, track_number):
        """Get the full path for the track MP3 file"""
        return os.path.join("tracks", f"{track_number}.mp3")

    def play_current_track(self):
        self.reset_progress()  # **Reset progress before playing a new track**

        """Play the current track from the MP3 file"""
        if 0 <= self.current_track_index < len(self.playlist):
            track_number = self.playlist[self.current_track_index]
            track_path = self.get_track_path(track_number)

            if os.path.exists(track_path):
                # Load track info
                track_name = get_name(track_number)
                self.track_info.configure(text=f"{track_number}: {track_name}")

                # Get track length using mutagen
                audio = MP3(track_path)
                self.current_track_length = audio.info.length

                # Update total time label
                total_min = int(self.current_track_length) // 60
                total_sec = int(self.current_track_length) % 60
                self.total_time.configure(text=f"{total_min}:{total_sec:02d}")

                # Stop any currently playing music
                pygame.mixer.music.stop()

                # **RESET PROGRESS BAR AND CURRENT TIME WHEN A NEW TRACK STARTS**
                self.progress_bar.set(0)  # Reset progress bar
                self.current_time.configure(text="0:00")  # Reset current time label

                # Load and play the new track
                pygame.mixer.music.load(track_path)
                pygame.mixer.music.play()

                # Update state and UI
                self.is_playing = True
                self.play_button.configure(text="⏸")
                self.progress = 0
                self.progress_bar.set(0)

                # Increment play count
                increment_play_count(track_number)
            else:
                messagebox.showerror("Error", f"Track file not found: {track_path}")
                self.next_track()

    def toggle_play_pause(self):
        """Toggle between play and pause states"""
        if self.is_playing:
            pygame.mixer.music.pause()
            self.play_button.configure(text="▶")
        else:
            pygame.mixer.music.unpause()
            self.play_button.configure(text="⏸")
        self.is_playing = not self.is_playing

    def reset_progress(self):
        """Reset the progress bar and time when switching tracks"""
        self.progress = 0
        self.progress_bar.set(0)
        self.current_time.configure(text="0:00")
        self.manually_skipped = False  # Reset manual skip flag
        self.elapsed_time = 0  # Reset elapsed time from manual skip
        self.start_time = 0  # Reset start time for manual skip

    def next_track(self):
        """Play next track in playlist."""
        if self.current_track_index < len(self.playlist) - 1:
            # Move to the next track
            self.current_track_index += 1
        else:
            # Loop back to the first track if we've reached the end of the playlist
            self.current_track_index = 0

        self.play_current_track()  # Play the new track (whether next or first)

    def previous_track(self):
        """Play previous track in playlist"""
        if self.current_track_index > 0:
            self.current_track_index -= 1
            self.play_current_track()

    def update_volume(self, value):
        """Update the volume of playback"""
        pygame.mixer.music.set_volume(float(value))

    def skip_in_track(self, event):
        """Skip to a position in the current track based on the progress bar click."""
        if self.current_track_length > 0:
            # Get the width of the progress bar
            progress_width = self.progress_bar.winfo_width()

            # Calculate the fraction of the click position
            click_x = event.x
            fraction = click_x / progress_width

            # Calculate the new time in the track
            new_time = fraction * self.current_track_length

            # Set the position in pygame mixer
            pygame.mixer.music.set_pos(new_time)

            # Update the progress bar and time labels manually
            self.progress = fraction  # Update the fraction for manual progress
            self.progress_bar.set(self.progress)

            current_min = int(new_time) // 60
            current_sec = int(new_time) % 60
            self.current_time.configure(text=f"{current_min}:{current_sec:02d}")

            # Set the flag and store the new position
            self.manually_skipped = True
            self.skip_position = new_time  # Save the skip position
            self.start_time = time.time()  # Track when the skip happens

    def update_progress(self):
        """Update progress bar and time labels based on actual playback position."""
        while True:
            if self.is_playing and self.current_track_length > 0:
                if self.manually_skipped:
                    # Calculate elapsed time since the skip
                    self.elapsed_time = time.time() - self.start_time
                    current_pos = self.skip_position + self.elapsed_time  # Track position after the skip
                else:
                    # Otherwise, get the position from pygame
                    current_pos = pygame.mixer.music.get_pos() / 1000

                # Check if the widget still exists before updating
                if self.window.winfo_exists():  # Check if the window is still open
                    # Update the progress based on current position
                    self.progress = current_pos / self.current_track_length

                    # Update the progress bar and current time
                    if self.progress_bar.winfo_exists():  # Check if progress bar exists
                        self.progress_bar.set(self.progress)

                    current_min = int(current_pos) // 60
                    current_sec = int(current_pos) % 60
                    if self.current_time.winfo_exists():  # Check if current time label exists
                        self.current_time.configure(text=f"{current_min}:{current_sec:02d}")

                    # Check if the track has ended and play the next one
                    if not pygame.mixer.music.get_busy() and self.is_playing:
                        self.next_track()

            # Small delay to avoid overloading the CPU
            time.sleep(0.1)

    def start_progress_thread(self):
        """Start a separate thread for updating progress"""
        progress_thread = threading.Thread(target=self.update_progress, daemon=True)
        progress_thread.start()

    def on_closing(self):
        """Handle window closing"""
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        self.window.destroy()
