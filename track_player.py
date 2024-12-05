import customtkinter as ctk
import font_manager as fonts
from view_tracks import TrackViewer
from create_track_list import CreateTrackList
from update_tracks import UpdateTracks
from search_tracks import SearchTracks  # Import YouTubePlayer

# Set the appearance mode and color theme
ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class JukeBoxApp:
    def __init__(self):
        # Configure the main window
        self.window = ctk.CTk()
        self.window.geometry("600x250")
        self.window.title("JukeBox")

        # Configure the grid layout
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_columnconfigure(2, weight=1)

        # Header Label
        self.header_lbl = ctk.CTkLabel(
            self.window, 
            text="Select an option by clicking one of the buttons below",
            font=("Helvetica", 16)
        )
        self.header_lbl.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky="ew")

        # Buttons with modern styling
        self.view_tracks_btn = ctk.CTkButton(
            self.window, 
            text="View Tracks", 
            command=self.view_tracks_clicked,
            corner_radius=10
        )
        self.view_tracks_btn.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.create_track_list_btn = ctk.CTkButton(
            self.window, 
            text="Create Track List", 
            command=self.create_track_list_clicked,
            corner_radius=10
        )
        self.create_track_list_btn.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        self.update_tracks_btn = ctk.CTkButton(
            self.window, 
            text="Update Tracks", 
            command=self.update_tracks_clicked,
            corner_radius=10
        )
        self.update_tracks_btn.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.search_tracks_btn = ctk.CTkButton(  # Add Search Tracks Button
            self.window, 
            text="Search Tracks", 
            command=self.search_tracks_clicked,
            corner_radius=10
        )
        self.search_tracks_btn.grid(row=2, column=2, padx=10, pady=10, sticky="ew")

        # Status Label
        self.status_lbl = ctk.CTkLabel(
            self.window, 
            text="", 
            font=("Helvetica", 12)
        )
        self.status_lbl.grid(row=3, column=0, columnspan=3, padx=20, pady=10, sticky="ew")

    def view_tracks_clicked(self):
        self.status_lbl.configure(text="View Tracks button was clicked!")
        self.create_and_show_toplevel(TrackViewer)

    def create_track_list_clicked(self):
        self.status_lbl.configure(text="Create Track List button was clicked!")
        self.create_and_show_toplevel(CreateTrackList)

    def update_tracks_clicked(self):
        self.status_lbl.configure(text="Update Tracks button was clicked!")
        self.create_and_show_toplevel(UpdateTracks)

    def search_tracks_clicked(self):
        self.status_lbl.configure(text="Search Tracks button was clicked!")
        self.create_and_show_toplevel(SearchTracks)

    def create_and_show_toplevel(self, view_class):
        """Create a CTkToplevel window and ensure it stays on top."""
        new_window = ctk.CTkToplevel(self.window)
        new_window.lift()  # Bring to front
        new_window.attributes('-topmost', True)  # Force to top of the stack
        new_window.focus_set()  # Set focus
        new_window.grab_set()  # Make it modal
        new_window.attributes('-topmost', False)  # Restore default behavior
        view_class(new_window)

    def run(self):
        self.window.mainloop()

# Run the application
if __name__ == "__main__":
    app = JukeBoxApp()
    fonts.configure()
    app.run()
