import customtkinter as ctk
import tkinter.scrolledtext as tkst
import track_library as lib
import font_manager as fonts
import os

class TrackViewer:
    def __init__(self, window):
        window.title("View Tracks")
        window.geometry("900x350")  # Slightly larger to accommodate new button

        # Configure grid
        window.grid_columnconfigure(0, weight=3)
        window.grid_columnconfigure(1, weight=1)

        # List Tracks Button
        self.list_tracks_btn = ctk.CTkButton(
            window, 
            text="List All Tracks", 
            command=self.list_tracks_clicked,
            corner_radius=10
        )
        self.list_tracks_btn.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        # Track Number Label and Entry
        self.enter_lbl = ctk.CTkLabel(
            window, 
            text="Enter Track Number",
            font=("Helvetica", 14)
        )
        self.enter_lbl.grid(row=0, column=1, padx=20, pady=10)

        self.input_txt = ctk.CTkEntry(
            window, 
            width=50,
            corner_radius=10
        )
        self.input_txt.grid(row=0, column=2, padx=20, pady=10)

        # View Track Button
        self.check_track_btn = ctk.CTkButton(
            window, 
            text="View Track", 
            command=self.view_tracks_clicked,
            corner_radius=10
        )
        self.check_track_btn.grid(row=0, column=3, padx=20, pady=10)

        # Remove Track Button
        self.remove_track_btn = ctk.CTkButton(
            window, 
            text="Remove Track", 
            command=self.remove_track_clicked,
            fg_color="red",  # Red color to indicate removal
            corner_radius=10
        )
        self.remove_track_btn.grid(row=0, column=4, padx=20, pady=10)

        # Track List Display (Scrolled Text)
        self.list_txt = tkst.ScrolledText(
            window, 
            width=70, 
            height=15, 
            wrap="none",
            font=("Consolas", 10)
        )
        self.list_txt.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=20, pady=10)

        # Individual Track Details
        self.track_txt = ctk.CTkTextbox(
            window, 
            width=250, 
            height=150,
            corner_radius=10
        )
        self.track_txt.grid(row=1, column=4, sticky="nsew", padx=20, pady=10)

        # Status Label
        self.status_lbl = ctk.CTkLabel(
            window, 
            text="", 
            font=("Helvetica", 12)
        )
        self.status_lbl.grid(row=2, column=0, columnspan=5, sticky="ew", padx=20, pady=10)

        # Tracks folder path (adjust as needed)
        self.tracks_folder = "tracks"

        # Initial track list display
        self.list_tracks_clicked()

    def view_tracks_clicked(self):
        # Get the track ID/key from the input text field
        key = self.input_txt.get()
        
        # Clear previous text
        self.track_txt.delete("1.0", ctk.END)
        
        # Try to find the track name using the provided key
        name = lib.get_name(key)
        
        # If the track exists in the library
        if name is not None:
            # Retrieve additional track details from the library
            artist = lib.get_artist(key)
            rating = lib.get_rating(key)
            play_count = lib.get_play_count(key)
                     
            # Format the track details into a multi-line string
            track_details = f"Track: {name}\nArtist: {artist}\nRating: {rating}\nPlay Count: {play_count}"
            
            # Display the track details in the track text area
            self.track_txt.insert(ctk.END, track_details)
        else:
            # Display error message if track is not found
            self.track_txt.insert(ctk.END, f"Track {key} not found")
        
        # Update status label to confirm button click
        self.status_lbl.configure(text="View Track button was clicked!")

    def remove_mp3_file(self, track_id):
        # Construct the full path to the MP3 file
        mp3_path = os.path.join(self.tracks_folder, f"{track_id}.mp3")
        
        # Check if the file exists
        if os.path.exists(mp3_path):
            try:
                # Remove the file
                os.remove(mp3_path)
                return True
            except Exception as e:
                # Log or handle any errors during file removal
                print(f"Error removing MP3 file: {e}")
                return False
        
        return False

    def remove_track_clicked(self):
        # Get the track ID/key from the input text field
        key = self.input_txt.get()
        
        # Clear previous text
        self.track_txt.delete("1.0", ctk.END)
        
        # Try to find the track name using the provided key
        name = lib.get_name(key)
        
        # If the track exists in the library
        if name is not None:
            try:
                # Remove the track from the library
                lib.remove_track(key)
                
                # Remove the MP3 file
                file_removed = self.remove_mp3_file(key)
                
                # Prepare file removal status message
                file_removal_status = "MP3 file removed successfully" if file_removed else "No MP3 file found"
                
                # Refresh the track list
                self.list_tracks_clicked()
                
                # Update track details text area
                self.track_txt.insert(ctk.END, f"Track {key} removed successfully\n{file_removal_status}")
                
                # Update status label
                self.status_lbl.configure(text=f"Track {key} removed!")
            
            except Exception as e:
                # Handle any errors during removal
                self.track_txt.insert(ctk.END, f"Error removing track: {str(e)}")
                self.status_lbl.configure(text="Track removal failed!")
        else:
            # Display error message if track is not found
            self.track_txt.insert(ctk.END, f"Track {key} not found")
            self.status_lbl.configure(text="Invalid track ID!")

    def list_tracks_clicked(self):
        # Get a list of all tracks from the library
        track_list = lib.list_all()
        
        # Clear previous list
        self.list_txt.delete("1.0", ctk.END)
        
        # Display the full track list in the list text area
        self.list_txt.insert(ctk.END, track_list)
        
        # Update status label to confirm button click
        self.status_lbl.configure(text="List Tracks button was clicked!")

# Stand-alone execution
if __name__ == "__main__":
    window = ctk.CTk()
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    fonts.configure()
    TrackViewer(window)
    window.mainloop()