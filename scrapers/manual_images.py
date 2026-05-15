from pathlib import Path

from icrawler.builtin import GoogleImageCrawler


def download_images(title: str, max_images: int = 3) -> Path:
    """Download scene images into `scrapers/scenes/<slug>/`."""
    base = Path(__file__).resolve().parent
    folder = base / "scenes" / title.replace(" ", "_")
    folder.mkdir(parents=True, exist_ok=True)

    crawler = GoogleImageCrawler(storage={"root_dir": str(folder)})
    crawler.crawl(keyword=f"{title} scene", max_num=max_images)
    print(
        f"Downloaded up to {max_images} images for '{title} scene' into '{folder}'."
    )
    return folder


if __name__ == "__main__":
    t = input("Enter a title to search for images: ").strip()
    if t:
        download_images(t)
