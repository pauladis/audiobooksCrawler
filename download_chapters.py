import requests
import os
import re

file_path = 'audio_src_urls.txt'
downloads_dir = 'downloads'

os.makedirs(downloads_dir, exist_ok=True)

with open(file_path, 'r') as file:
    urls = file.readlines()

def download_file(url):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        filename = None
        if 'content-disposition' in response.headers:
            cd = response.headers['content-disposition']
            fname_match = re.findall('filename="([^"]+)"', cd)
            if fname_match:
                filename = fname_match[0]
            else:
                fname_match = re.findall("filename\*=UTF-8''(.+)", cd)
                if fname_match:
                    filename = requests.utils.unquote(fname_match[0])

        if not filename:
            filename = os.path.basename(url)

        filename = re.sub(r'[\\/*?:"<>|]', "", filename)

        file_path = os.path.join(downloads_dir, filename)
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f'Downloaded: {filename}')
    except requests.RequestException as e:
        print(f'Failed to download {url}: {e}')

for url in urls:
    url = url.strip()
    if url:
        download_file(url)
