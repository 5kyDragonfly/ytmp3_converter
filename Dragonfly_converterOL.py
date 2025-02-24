import streamlit as st
import yt_dlp
import os
import subprocess
import sys

# Set default save folder (Downloads)
if 'save_folder' not in st.session_state:
    if os.name == 'nt':  # Windows
        st.session_state['save_folder'] = os.path.join(os.environ['USERPROFILE'], 'Downloads')
    else:  # macOS & Linux
        st.session_state['save_folder'] = os.path.join(os.path.expanduser("~"), "Downloads")

def download_audio(youtube_urls, save_folder):
    for url in youtube_urls:
        try:
            # Set up yt_dlp options for audio extraction without 'keepvideo'
            ydl_opts = {
                'format': 'bestaudio/best',
                'updatetime': False,  # Disable preserving upload timestamp
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192'
                }],
                'outtmpl': os.path.join(save_folder, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'quiet': False,
                'nocheckcertificate': True,
                'noprogress': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = os.path.splitext(ydl.prepare_filename(info))[0] + ".mp3"
                if not os.path.exists(filename):
                    st.error(f"❌ Failed to download: {url}")
                else:
                    st.write(f"✅ Downloaded: {filename}")
        except Exception as e:
            st.error(f"Error downloading {url}: {e}")

# --- Streamlit UI ---
st.title("YouTube to MP3 Converter")

st.write("**Save Folder:**")
st.session_state['save_folder'] = st.text_input("Enter custom save folder (default: Downloads):", st.session_state['save_folder'])
st.write("Save Folder:", st.session_state['save_folder'])

links = st.text_area("Enter YouTube URLs (one per line)")
urls = [url.strip() for url in links.split('\n') if url.strip()]

if st.button("Download MP3s"):
    if urls:
        with st.spinner("Downloading..."):
            if not os.path.exists(st.session_state['save_folder']):
                os.makedirs(st.session_state['save_folder'], exist_ok=True)
            if not os.access(st.session_state['save_folder'], os.W_OK):
                st.error(f"❌ No write permission for: {st.session_state['save_folder']}. Please choose a different folder.")
            else:
                download_audio(urls, st.session_state['save_folder'])
    else:
        st.warning("Please enter at least one valid YouTube URL.")
