import customtkinter as ctk
from tkinter import messagebox
from track_library import get_name
import font_manager as fonts
from play_tracks import MediaPlayer

class CreateTrackList:
    def __init__(self, window):
        self.window = window  # Store the window reference
        window.title("Create Track List")
        window.geometry("400x550")

        # Configure grid
        window.grid_columnconfigure(0, weight=1)

        self.playlist = []

        # Track Number Label and Entry
        self.track_label = ctk.CTkLabel(
            window, 
            text="Enter Track Number (e.g., 01):",
            font=("Helvetica", 14)
        )
        self.track_label.pack(pady=(20, 5))

        self.track_entry = ctk.CTkEntry(
            window, 
            width=200,
            corner_radius=10
        )
        self.track_entry.pack(pady=10)

        # Add to Playlist Button
        self.add_button = ctk.CTkButton(
            window, 
            text="Add to Playlist", 
            command=self.add_to_playlist,
            corner_radius=10
        )
        self.add_button.pack(pady=10)

        # Playlist Display
        self.playlist_display = ctk.CTkTextbox(
            window, 
            width=400, 
            height=250,
            corner_radius=10
        )
        self.playlist_display.pack(pady=10)

        # Play Playlist Button
        self.play_button = ctk.CTkButton(
            window, 
            text="Play Playlist", 
            command=self.play_playlist,
            corner_radius=10,
            fg_color="green"
        )
        self.play_button.pack(pady=10)

        # Reset Playlist Button
        self.reset_button = ctk.CTkButton(
            window, 
            text="Reset Playlist", 
            command=self.reset_playlist,
            corner_radius=10,
            fg_color="red"
        )
        self.reset_button.pack(pady=10)

    def add_to_playlist(self):
        """Adds a track to the playlist if it's valid and not already in the list."""
        track_number = self.track_entry.get()

        # Check if track number is numeric
        if not track_number.isdigit():
            messagebox.showerror("Error", "Track number must be numeric.")
            return

        track_name = get_name(track_number)

        if track_name:
            if track_number in self.playlist:
                messagebox.showwarning("Warning", f"Track {track_number} is already in the playlist.")
            else:
                self.playlist.append(track_number)
                self.update_playlist_display()
                messagebox.showinfo("Success", f"Track {track_number}: {track_name} added to playlist.")
        else:
            messagebox.showerror("Error", "Invalid track number")
            
        # Clear the track number entry after adding
        self.track_entry.delete(0, ctk.END)

    def update_playlist_display(self):
        """Updates the playlist display in the text area."""
        self.playlist_display.delete("1.0", ctk.END)
        for track_number in self.playlist:
            track_name = get_name(track_number)
            if track_name:
                self.playlist_display.insert(ctk.END, f"{track_number}: {track_name}\n")

    def play_playlist(self):
        """Opens the media player window to play the playlist."""
        if not self.playlist:
            messagebox.showwarning("Warning", "Playlist is empty!")
        else:
            # Create and show the media player window
            media_player = MediaPlayer(self.playlist, self.window)

    def reset_playlist(self):
        """Resets the playlist and clears the display."""
        self.playlist.clear()
        self.playlist_display.delete("1.0", ctk.END)
        messagebox.showinfo("Playlist Reset", "The playlist has been cleared.")

        # Clear the track number entry after reset
        self.track_entry.delete(0, ctk.END)

# GUI initialization
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    fonts.configure()
    gui = CreateTrackList(root)
    root.mainloop()