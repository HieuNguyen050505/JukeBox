import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from googleapiclient.discovery import build
from youtube_downloader import YouTubeDownloader
import font_manager as fonts

class SearchTracks:
    def __init__(self, window):
        # Initialize main window
        self.window = window
        window.title("Search Tracks")
        window.geometry("800x600")
        
        # YouTube API setup
        self.API_KEY = 'AIzaSyB25-wtp04Ri3r-iasPyI3lWABo0RP0OC8'
        self.youtube = build('youtube', 'v3', developerKey=self.API_KEY)
        
        # Initialize downloader
        self.downloader = YouTubeDownloader()
        
        self.setup_gui()
        
    def setup_gui(self):
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Search frame
        self.search_frame = ctk.CTkFrame(self.main_frame)
        self.search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Search entry
        self.search_var = tk.StringVar()
        self.search_entry = ctk.CTkEntry(
            self.search_frame, 
            width=400,
            placeholder_text="Search for songs...",
            textvariable=self.search_var
        )
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        # Search button
        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="Search",
            command=self.search_videos
        )
        self.search_button.pack(side=tk.LEFT, padx=5)
        
        # Results frame
        self.results_frame = ctk.CTkFrame(self.main_frame)
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            wraplength=400
        )
        self.status_label.pack(fill=tk.X, padx=5, pady=5)
        
        # Bind keyboard shortcuts
        self.window.bind('<Return>', lambda e: self.search_videos())
        
    def search_videos(self):
        query = self.search_var.get()
        if not query:
            return
            
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        try:
            # Search for videos
            request = self.youtube.search().list(
                part="snippet",
                maxResults=5,
                q=query,
                type="video"
            )
            response = request.execute()
            
            # Display results
            for item in response['items']:
                video_frame = ctk.CTkFrame(self.results_frame)
                video_frame.pack(fill=tk.X, padx=5, pady=2)
                
                # Load and display thumbnail
                thumbnail_url = item['snippet']['thumbnails']['default']['url']
                response = requests.get(thumbnail_url)
                img = Image.open(BytesIO(response.content))
                photo = ImageTk.PhotoImage(img)
                
                thumbnail_label = tk.Label(video_frame, image=photo)
                thumbnail_label.image = photo
                thumbnail_label.pack(side=tk.LEFT, padx=5, pady=5)
                
                # Video title and add button
                title = item['snippet']['title']
                title_label = ctk.CTkLabel(
                    video_frame,
                    text=title,
                    wraplength=400
                )
                title_label.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.BOTH)
                
                add_button = ctk.CTkButton(
                    video_frame,
                    text="Add to Library",
                    width=100,
                    command=lambda vid_id=item['id']['videoId'], 
                            title=title: self.add_to_library(vid_id, title)
                )
                add_button.pack(side=tk.RIGHT, padx=5)
                
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.results_frame,
                text=f"Error searching videos: {str(e)}"
            )
            error_label.pack(padx=5, pady=5)
    
    def add_to_library(self, video_id, title):
        self.status_label.configure(text=f"Downloading: {title}")
        self.window.update()
        
        track_id = self.downloader.download_and_save(video_id, title)
        
        if track_id:
            self.status_label.configure(
                text=f"Successfully added to library with ID: {track_id}"
            )
        else:
            self.status_label.configure(
                text="Error adding track to library"
            )
            
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    fonts.configure()
    app = SearchTracks(root)
    root.mainloop()