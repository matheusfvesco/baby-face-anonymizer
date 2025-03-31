from googleapiclient.discovery import build
import os
from pathlib import Path
import requests
from dotenv import load_dotenv
import filecmp
from tqdm import tqdm

load_dotenv()

def download_image(url, filename, save_dir):
    """Download an image from a URL and save it to the specified directory."""
    save_dir = Path(save_dir)
    try:
        save_dir.mkdir(parents=True, exist_ok=True)
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        
        ext = save_dir.suffix
        if not ext or ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            ext = '.jpg'
        
        full_path = save_dir / f"{filename}{ext}"
        
        with open(full_path, 'wb') as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)
        return True
    except Exception as e:
        tqdm.write(f"Error thrown: {e}")
        return False

def main():
    SAVE_DIR = Path('data/mined')


    terms = [line.replace("\n","") for line  in open("queries.txt").readlines()]

    with build('customsearch', 'v1', developerKey=os.getenv("G_API_KEY")) as service:
        def google_image_search(query, num_results=10, img_size='imgSizeUndefined', img_type='photo'):
            try:
                result = service.cse().list(
                    q=query,
                    cx=os.getenv("SEARCH_ENGINE_ID"),
                    searchType='image',
                    num=num_results,
                    imgSize=img_size,
                    imgType=img_type,
                    safe='high'
                ).execute()
                return result.get('items', [])
            except Exception as e:
                tqdm.write(f"Error thrown: {e}")
                return []

        idx = 0
        main_pbar = tqdm(terms)
        for term in main_pbar:
            main_pbar.set_description(f"Querying '{term}'")
            image_results = google_image_search(term)
            sec_pbar = tqdm(image_results)
            for item in sec_pbar:
                title = f"baby{idx}"
                image_url = item['link']
                if download_image(image_url, title, SAVE_DIR):
                    idx += 1
            sec_pbar.close()

    # removes duplicates
    for file1 in SAVE_DIR.iterdir():
        for file2 in SAVE_DIR.iterdir():
            if file1 == file2:
                continue
            if not filecmp.cmp(file1, file2, shallow=False):
                continue
            print(file1, file2)

            os.remove(file1)
            break

if __name__ == "__main__":
    main()