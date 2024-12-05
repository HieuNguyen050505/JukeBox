from library_item import LibraryItem
from file_operations import save_library_to_csv, load_library_from_csv

CSV_FILE_PATH = "library.csv"

def list_all():
    library = load_library_from_csv(CSV_FILE_PATH)
    output = ""
    for key in library:
        item = library[key]
        output += f"{key} {item.info()}\n"
    return output


def get_name(key):
    library = load_library_from_csv(CSV_FILE_PATH)
    try:
        item = library[key]
        return item.name
    except KeyError:
        return None


def get_artist(key):
    library = load_library_from_csv(CSV_FILE_PATH)
    try:
        item = library[key]
        return item.artist
    except KeyError:
        return None


def get_rating(key):
    library = load_library_from_csv(CSV_FILE_PATH)
    try:
        item = library[key]
        return item.rating
    except KeyError:
        return -1


def set_rating(key, rating):
    library = load_library_from_csv(CSV_FILE_PATH)
    try:
        item = library[key]
        item.rating = rating
        save_library_to_csv(CSV_FILE_PATH, library)
    except KeyError:
        return


def get_play_count(key):
    library = load_library_from_csv(CSV_FILE_PATH)
    try:
        item = library[key]
        return item.play_count
    except KeyError:
        return -1


def increment_play_count(key):
    library = load_library_from_csv(CSV_FILE_PATH)
    try:
        item = library[key]
        item.play_count += 1
        save_library_to_csv(CSV_FILE_PATH, library)
    except KeyError:
        return

def remove_track(track_id):
    library = load_library_from_csv(CSV_FILE_PATH)

    if track_id in library:
        del library[track_id]
        save_library_to_csv(CSV_FILE_PATH, library)
    else:
        raise ValueError(f"Track {track_id} not found in library")
    