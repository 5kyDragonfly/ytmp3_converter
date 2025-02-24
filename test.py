import streamlit as st
import yt_dlp
import os
import time
import tkinter as tk
from tkinter import filedialog

# Set default save folder (Desktop)
if 'save_folder' not in st.session_state:
    st.session_state['save_folder'] = os.path.join(os.path.expanduser("~"), "Desktop")

def download_audio(youtube_urls, save_folder):
    for url in youtube_urls:
        try:
            # Set up yt_dlp options for audio extraction
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192'
                }],
                'outtmpl': os.path.join(save_folder, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'quiet': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = os.path.splitext(ydl.prepare_filename(info))[0] + ".mp3"
                if os.path.exists(filename):
                    st.write(f"✅ Downloaded: {filename}")
                else:
                    st.error(f"❌ Failed to download: {url}")
        except Exception as e:
            st.error(f"Error downloading {url}: {e}")

# --- Streamlit UI ---
st.title("YouTube to MP3 Converter")

# Allow user to select a folder using tkinter
st.write("**Save Folder:**")
def select_folder():
    root = tk.Tk()
    root.attributes('-topmost', True)  # Bring dialog to front.
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        st.session_state['save_folder'] = folder_selected

if st.button("Choose Folder"):
    select_folder()
st.write("Save Folder:", st.session_state['save_folder'])

# Get YouTube URLs from the user.
links = st.text_area("Enter YouTube URLs (one per line)")
urls = [url.strip() for url in links.split('\n') if url.strip()]

# When the "Download MP3s" button is pressed:
if st.button("Download MP3s"):
    if urls:
        with st.spinner("Downloading..."):
            download_audio(urls, st.session_state['save_folder'])
        st.success("✅ All downloads processed!")
    else:
        st.warning("Please enter at least one valid YouTube URL.")
