import csv
import os
import threading
import time

import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
from PIL import Image


# scrape photo information from the website
def scrape_photo_data(url):
    """Retrieve photo titles, photographers, and categories from a web page."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # extracting photo titles
    photo_titles = [
        title.get_text(strip=True)
        for title in soup.find_all("h3", class_="photo-title")
    ]

    # extracting photographer names
    photographer_names = [
        photographer.get_text(strip=True)
        for photographer in soup.find_all("span", class_="photo-author")
    ]

    # extracting photo categories
    photo_categories = [
        category.get_text(strip=True)
        for category in soup.find_all("a", class_="photo-category")
    ]

    return photo_titles, photographer_names, photo_categories


# File Organization
def organize_photos(photo_titles, photographer_names, photo_categories):
    """Create directories based on photographer and photo category."""
    main_directory = "Photos"
    os.makedirs(main_directory, exist_ok=True)

    for _, photographer, category in zip(
        photo_titles, photographer_names, photo_categories
    ):
        photographer_directory = os.path.join(
            main_directory, photographer
        )
        category_directory = os.path.join(
            photographer_directory, category
        )

        os.makedirs(category_directory, exist_ok=True)


# resize and compress photos
def resize_and_compress_photos(
    input_directory,
    output_directory,
    target_resolution=(800, 600),
    quality=75
):
    """Resize and compress images in a directory."""
    if not os.path.isdir(input_directory):
        print(f"Input directory not found: {input_directory}")
        return

    os.makedirs(output_directory, exist_ok=True)

    for root, _, files in os.walk(input_directory):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                input_path = os.path.join(root, file)
                output_path = os.path.join(output_directory, file)

                with Image.open(input_path) as img:
                    img = img.resize(
                        target_resolution,
                        Image.Resampling.LANCZOS
                    )
                    img.save(
                        output_path,
                        optimize=True,
                        quality=quality
                    )


photo_data = [
    {
        "title": "Nature Beauty",
        "photographer": "John Doe",
        "tags": "nature, landscape, outdoors",
        "image_url": "https://example.com/photo1.jpg"
    },
    {
        "title": "Sunset Serenity",
        "photographer": "Richard Roe",
        "tags": "sunset, sky, clouds",
        "image_url": "https://example.com/photo2.jpg"
    },
]


def process_and_write_to_csv(data, output_file, lock):
    """Write photo data to a CSV file using synchronized access."""
    fieldnames = ["Title", "Photographer", "Tags", "Image URL"]

    with lock:
        file_exists = os.path.exists(output_file)

        with open(
            output_file,
            mode="a",
            newline="",
            encoding="utf-8"
        ) as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            for photo in data:
                writer.writerow({
                    "Title": photo["title"],
                    "Photographer": photo["photographer"],
                    "Tags": photo["tags"],
                    "Image URL": photo["image_url"]
                })


# generate the CSV file using multithreading
def generate_csv_file_multithreaded(data, output_file):
    """Generate a CSV file using multiple worker threads."""
    start_time = time.time()

    lock = threading.Lock()
    threads = []

    number_of_threads = min(4, len(data))

    for i in range(number_of_threads):
        thread = threading.Thread(
            target=process_and_write_to_csv,
            args=(data[i::number_of_threads], output_file, lock)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    execution_time = time.time() - start_time

    print(
        f"CSV file '{output_file}' has been generated "
        f"using multithreading in {execution_time:.2f} seconds."
    )


def create_visualizations():
    """Create visualizations of photo categories and photographers."""
    categories = [
        "Nature",
        "Cityscape",
        "Portraits",
        "Wildlife",
        "Abstract"
    ]
    category_counts = [25, 30, 20, 35, 15]

    photographers = [
        "Kimia Karimi",
        "Ali Sadeghi",
        "Maryam Ahmadi",
        "Sheida Mojtahedi"
    ]
    photographer_counts = [40, 35, 30, 25]

    plt.figure(figsize=(10, 5))
    plt.bar(categories, category_counts)
    plt.title("Number of Photographs Downloaded per Category")
    plt.xlabel("Category")
    plt.ylabel("Number of Photographs")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(8, 5))
    plt.bar(photographers, photographer_counts)
    plt.title("Number of Photographs Downloaded per Photographer")
    plt.xlabel("Photographer")
    plt.ylabel("Number of Photographs")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def main():
    # Web scraping
    url = "https://stocksnap.io/"

    try:
        photo_titles, photographer_names, photo_categories = (
            scrape_photo_data(url)
        )

        print("Photo Titles:", photo_titles)
        print("Photographer Names:", photographer_names)
        print("Photo Categories:", photo_categories)

        organize_photos(
            photo_titles,
            photographer_names,
            photo_categories
        )

    except requests.RequestException as error:
        print(f"Could not retrieve the web page: {error}")

    input_directory = "Photos/Photographer 1/Nature" # replace with the actual input directory
    output_directory = (
        "Resized_Compressed_Photos/Photographer 1/Nature" # replace with the desired output directory
    )

    resize_and_compress_photos(
        input_directory,
        output_directory,
        target_resolution=(800, 600),
        quality=75
    )

    csv_output_file = "photo_data_multithreaded.csv"
    generate_csv_file_multithreaded(
        photo_data,
        csv_output_file
    )

    create_visualizations()


if __name__ == "__main__":
    main()
