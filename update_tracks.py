import customtkinter as ctk
from tkinter import messagebox
from track_library import get_name, set_rating, get_play_count
import font_manager as fonts

class UpdateTracks:
    def __init__(self, window):
        window.title("Update Tracks")
        window.geometry("500x400")

        # Configure appearance mode (Light/Dark)
        ctk.set_appearance_mode("System")  # Alternatives: "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Alternatives: "green", "dark-blue"

        # Entry for track number
        self.track_label = ctk.CTkLabel(window, text="Enter Track Number (e.g., 01):")
        self.track_label.pack(pady=(10, 5))

        self.track_entry = ctk.CTkEntry(window, placeholder_text="Track Number")
        self.track_entry.pack(pady=5)

        # Entry for new rating
        self.rating_label = ctk.CTkLabel(window, text="Enter New Rating (1-5):")
        self.rating_label.pack(pady=(10, 5))

        self.rating_entry = ctk.CTkEntry(window, placeholder_text="Rating")
        self.rating_entry.pack(pady=5)

        # Button to update the track's rating
        self.update_button = ctk.CTkButton(window, text="Update Rating", command=self.update_rating)
        self.update_button.pack(pady=(15, 5))

        # Frame for result display with scrollbars
        self.result_frame = ctk.CTkFrame(window)
        self.result_frame.pack(pady=(10, 5), fill="both", expand=True)

        # Scrollable text area for results
        self.result_display = ctk.CTkTextbox(self.result_frame, height=10, width=50, wrap="word")
        self.result_display.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Vertical scrollbar
        self.scrollbar = ctk.CTkScrollbar(self.result_frame, command=self.result_display.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.result_display.configure(yscrollcommand=self.scrollbar.set)

    def update_rating(self):
        """Update the rating of the track and display the result."""
        track_number = self.track_entry.get()

        # Validate that the track number is numeric
        if not track_number.isdigit():
            messagebox.showerror("Error", "Track number must be numeric.")
            self.clear_entries()
            return

        # Validate the rating input
        try:
            new_rating = int(self.rating_entry.get())
            if not (1 <= new_rating <= 5):
                messagebox.showerror("Error", "Rating must be between 1 and 5.")
                self.clear_entries()
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid rating.")
            self.clear_entries()
            return

        # Check if the track number is valid
        track_name = get_name(track_number)
        if track_name:
            set_rating(track_number, new_rating)
            play_count = get_play_count(track_number)
            self.result_display.delete("1.0", "end")
            self.result_display.insert("1.0", f"Track: {track_name}\nNew Rating: {new_rating}\nPlay Count: {play_count}")
            messagebox.showinfo("Success", f"Track {track_number}: {track_name} rating has been updated.")
        else:
            messagebox.showerror("Error", "Invalid track number")

        # Clear the entries in all cases
        self.clear_entries()

    def clear_entries(self):
        """Clear the track number and rating entry fields."""
        self.track_entry.delete(0, "end")
        self.rating_entry.delete(0, "end")


# GUI initialization
if __name__ == "__main__":
    root = ctk.CTk()
    fonts.configure()
    gui = UpdateTracks(root)
    root.mainloop()
