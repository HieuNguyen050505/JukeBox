import csv
from library_item import LibraryItem

def save_library_to_csv(file_path, library):
    """
    Save the library dictionary to a CSV file.
    """
    with open(file_path, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["track_id", "name", "artist", "rating", "play_count"])
        for key, item in library.items():
            writer.writerow([key, item.name, item.artist, item.rating, item.play_count])

def load_library_from_csv(file_path):
    """
    Load the library dictionary from a CSV file.
    """
    library = {}
    with open(file_path, mode="r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            library[row["track_id"]] = LibraryItem(
                row["name"], 
                row["artist"], 
                int(row["rating"]) if row["rating"] else 0
            )
            library[row["track_id"]].play_count = int(row["play_count"]) if row["play_count"] else 0
    return library
