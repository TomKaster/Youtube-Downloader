"""Simple YouTube video/audio downloader.

Uses yt-dlp (the maintained successor to youtube-dl). The original version used
pytube, which stopped working after YouTube changed how it serves videos.
"""

import os
import shutil
import sys
from pathlib import Path

import yt_dlp
from yt_dlp.utils import DownloadError

DOWNLOAD_DIR = Path.home() / "Downloads"


def app_dir() -> Path:
    """Folder the program lives in (next to the .exe when packaged with PyInstaller)."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent


def find_ffmpeg():
    """Return a folder containing ffmpeg, or None.

    Looks next to the program first (so ffmpeg.exe can ship alongside the .exe),
    then on the system PATH.
    """
    exe = "ffmpeg.exe" if os.name == "nt" else "ffmpeg"
    if (app_dir() / exe).exists():
        return str(app_dir())
    found = shutil.which("ffmpeg")
    return str(Path(found).parent) if found else None


def pause_and_exit(code: int = 0):
    # Keeps the console window open when the .exe is double-clicked.
    input("Press Enter to exit")
    sys.exit(code)


def ask(prompt: str, choices) -> str:
    while True:
        answer = input(prompt).strip().lower()
        if answer in choices:
            return answer
        print(f"Please type one of: {', '.join(choices)}")


def build_options(mode: str, ffmpeg_dir):
    opts = {
        "outtmpl": str(DOWNLOAD_DIR / "%(title)s.%(ext)s"),
        "noplaylist": True,          # a URL with &list=... downloads just that video
        "windowsfilenames": True,    # strip characters Windows doesn't allow
    }
    if ffmpeg_dir:
        opts["ffmpeg_location"] = ffmpeg_dir

    if mode == "video":
        if ffmpeg_dir:
            # Best quality: separate video + audio streams merged into one .mp4
            opts["format"] = "bv*[ext=mp4]+ba[ext=m4a]/bv*+ba/b"
            opts["merge_output_format"] = "mp4"
        else:
            # No ffmpeg: fall back to a single pre-merged file (usually lower resolution)
            print("Note: ffmpeg not found, so video quality may be limited.")
            opts["format"] = "b[ext=mp4]/b"
    else:  # audio
        opts["format"] = "bestaudio/best"
        opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    return opts


def main():
    mode = ask("Do you want to download video or audio? Type 'video' or 'audio': ",
               ("video", "audio"))
    noun = "video" if mode == "video" else "video whose audio"
    url = input(f"Enter the URL for the YouTube {noun} you want to download: ").strip()

    ffmpeg_dir = find_ffmpeg()
    if mode == "audio" and not ffmpeg_dir:
        print("ffmpeg is required to convert audio to mp3, but it wasn't found.")
        print("Put ffmpeg.exe next to this program or install it and add it to PATH.")
        pause_and_exit(1)

    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    print("Connecting...")
    try:
        with yt_dlp.YoutubeDL(build_options(mode, ffmpeg_dir)) as ydl:
            ydl.download([url])
    except DownloadError as e:
        print(f"\nDownload failed: {e}")
        print("If this keeps happening, YouTube may have changed something: "
              "update yt-dlp and make sure Deno is installed (see README).")
        pause_and_exit(1)

    print("Finished downloading to your 'Downloads' folder.")
    pause_and_exit(0)


if __name__ == "__main__":
    main()
