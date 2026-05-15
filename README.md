# Anime Recommender

This repository builds a **neural collaborative filtering** model on public **MyAnimeList** user–anime ratings: it learns embeddings for users and titles, then predicts how someone would score a show on a normalized 0–1 scale (aligned with the original 1–10 ratings after scaling).

## What’s in the repo

| Piece | Purpose |
|--------|--------|
| **`main.ipynb`** | End-to-end notebook: download the MAL dataset, preprocess ~24M `(user_id, anime_id, rating)` rows, train a PyTorch **`RecommenderNet`** (user/anime embeddings + small MLP + biases, NCF-style), and evaluate on a held-out test split. |
| **`top200.ipynb`** | Derives the **top 200 anime** by popularity (`Scored By`) from the Kaggle anime metadata CSV and writes **`top_200_anime.csv`** in the notebook’s working directory (often `scrapers/top_200_anime.csv` if you run it from `scrapers/`). |
| **`scrapers/`** | Optional helpers: **scene images** via Google Image crawl (`icrawler`), and **music clips** from YouTube search + `yt-dlp` (requires **ffmpeg** for audio extraction). |

The core dataset is **[dbdmobile/myanimelist-dataset](https://www.kaggle.com/datasets/dbdmobile/myanimelist-dataset)** on Kaggle, fetched in-notebook with **`kagglehub`**.

## Setup

**Conda (recommended)** — matches the pinned stack in `environment.yml` (Python 3.11 on macOS arm64 when that file was exported):

```bash
conda create --name anime --file environment.yml
conda activate anime
```

**Kaggle API** — `kagglehub` needs credentials so the dataset can download (e.g. `~/.kaggle/kaggle.json` or the `KAGGLE_USERNAME` / `KAGGLE_KEY` environment variables). See [Kaggle’s API docs](https://www.kaggle.com/docs/api).

**Optional scrapers**

- Images: `pip install icrawler` (and any dependencies for `GoogleImageCrawler`).
- Music: `youtube-search`, `yt-dlp`, and a working **ffmpeg** on your `PATH`.

> **Note:** `requirements.txt` in this repo is a **pip freeze / export** (including build-specific local paths), not a minimal install list. Prefer `environment.yml` for a clean environment unless you maintain a trimmed `requirements.txt` yourself.

## Running the model

1. Activate the environment above.
2. Open **`main.ipynb`** in Jupyter and run cells in order. The first cells download and cache the Kaggle dataset (large download, ~1.8 GB compressed as of the notebook output).
3. Training uses **PyTorch** and will pick **CUDA**, **Apple MPS**, or **CPU** automatically when possible. Full training on all user ratings is memory- and compute-heavy; the notebook is set up for that scale, so use GPU/MPS when you can.

## Project layout (high level)

- **`main.ipynb`** — dataset load (`users-score-2023.csv`), `MinMaxScaler` on ratings, `LabelEncoder` for user/anime IDs, `RecommenderNet` + MSE, train/eval helpers.
- **`top200.ipynb`** — popularity ranking from `anime-dataset-2023.csv`.
- **`scrapers/image_scraper.py`**, **`scrapers/manual_images.py`** — download reference images for a title.
- **`scrapers/music_scraper.py`**, **`scrapers/manual_music.py`** — search and clip OST-related audio from YouTube.

## License / data

Model code is yours to use per your repo license. **MyAnimeList** and **Kaggle** dataset terms apply to the downloaded data; scrape only in line with site terms and applicable law.
