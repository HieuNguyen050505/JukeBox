import os
import yt_dlp
from library_item import LibraryItem
from file_operations import save_library_to_csv, load_library_from_csv

class YouTubeDownloader:
    def __init__(self, library_path="library.csv", tracks_folder="tracks"):
        self.library_path = library_path
        self.tracks_folder = tracks_folder
        self.library = load_library_from_csv(library_path)
        
        # Create tracks folder if it doesn't exist
        if not os.path.exists(tracks_folder):
            os.makedirs(tracks_folder)
        
        # Create temp folder if it doesn't exist
        if not os.path.exists("temp"):
            os.makedirs("temp")
            
        # Set up FFmpeg path - adjust this to your actual FFmpeg path
        self.ffmpeg_path = os.path.join(os.path.dirname(__file__), 'ffmpeg', 'bin')
            
    def get_next_track_id(self):
        """
        Generates the next sequential track ID based on the current library.
        Ignores non-numeric keys in the library.
        """
        numeric_ids = [
            int(k) for k in self.library.keys() if k.isdigit()
        ]
        if not numeric_ids:
            return "01"  # Start from "01" if no numeric IDs are present
        max_id = max(numeric_ids)
        return f"{max_id + 1:02d}"  # Zero-padded to 2 digits

    def download_and_save(self, video_id, video_title, artist=""):
        """
        Downloads YouTube video audio, converts to MP3, and adds to library
        Returns: track_id if successful, None if failed
        """
        try:
            # Generate the next sequential track ID
            track_id = self.get_next_track_id()

            # Get video URL
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            print(f"Attempting to download: {video_url}")

            # Configure yt-dlp options with FFmpeg path
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'temp/temp_{track_id}.%(ext)s',
                'ffmpeg_location': self.ffmpeg_path,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'progress_hooks': [self._progress_hook],
                'quiet': False,
                'no_warnings': False
            }

            print("Starting download...")
            # Download the audio
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get video info first
                info = ydl.extract_info(video_url, download=False)
                uploader = info.get('uploader', '')

                # Download the video
                ydl.download([video_url])

            # The file will be downloaded as MP3 already
            temp_file = f'temp/temp_{track_id}.mp3'
            final_path = os.path.join(self.tracks_folder, f"{track_id}.mp3")

            # Move the file to the final location
            os.rename(temp_file, final_path)

            print("Adding to library...")
            # Add to library
            self.library[track_id] = LibraryItem(
                name=video_title,
                artist=artist if artist else uploader,
                rating=0
            )

            # Save updated library
            save_library_to_csv(self.library_path, self.library)

            print(f"Successfully downloaded and saved track: {track_id}")
            return track_id

        except Exception as e:
            print(f"Error in download_and_save: {e}")
            return None
    
    def _progress_hook(self, d):
        """Progress hook for download progress"""
        if d['status'] == 'downloading':
            try:
                percent = d['_percent_str']
                print(f"Download Progress: {percent}")
            except KeyError:
                pass
        elif d['status'] == 'finished':
            print("Download completed, processing file...")
    
    def get_library(self):
        """Returns the current library dictionary"""
        return self.library