from icrawler.builtin import GoogleImageCrawler
import os

def download_images(title, output_folder, max_images=3):
    """
    Downloads images related to the given title.
    
    :param title: Title to search for images.
    :param output_folder: Folder to save the downloaded images.
    :param max_images: Number of images to download.
    """
    os.makedirs(output_folder, exist_ok=True)

    google_crawler = GoogleImageCrawler(storage={'root_dir': output_folder})
    google_crawler.crawl(keyword=f"{title} scene", max_num=max_images)
    #print(f"Images downloaded for '{title}' into '{output_folder}'.")

# if __name__ == "__main__":
#     # Example usage
#     download_images("Tatami Galaxy", "images")