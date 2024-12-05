import pytest
from library_item import LibraryItem

# Fixture to create a sample LibraryItem object
@pytest.fixture
def sample_item():
    """Fixture to create a sample LibraryItem object with default values."""
    return LibraryItem("Shape of You", "Ed Sheeran", 3)

def test_library_item_init(sample_item):
    """Test initialization of LibraryItem."""
    assert sample_item.name == "Shape of You"
    assert sample_item.artist == "Ed Sheeran"
    assert sample_item.rating == 3
    assert sample_item.play_count == 0

def test_info_method(sample_item):
    """Test the info method returns the correct string."""
    assert sample_item.info() == "Shape of You - Ed Sheeran ***"

def test_stars_method(sample_item):
    """Test the stars method returns the correct number of stars."""
    assert sample_item.stars() == "***"

    # Test with different ratings
    item_high_rating = LibraryItem("Another Brick in the Wall", "Pink Floyd", 5)
    assert item_high_rating.stars() == "*****"

    item_zero_rating = LibraryItem("Track Without Stars", "Unknown Artist", 0)
    assert item_zero_rating.stars() == ""

def test_increment_play_count(sample_item):
    """Test manually incrementing play count."""
    sample_item.play_count += 1
    assert sample_item.play_count == 1

    sample_item.play_count += 1
    assert sample_item.play_count == 2
