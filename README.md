# Youtube-Downloader
Downloader for YouTube video and audio.

The downloader asks whether you want video or just audio. Video is saved as **mp4**, audio as **mp3**, both to your `Downloads` folder.

> The original version used `pytube`, which stopped working after YouTube changes. It now uses [yt-dlp](https://github.com/yt-dlp/yt-dlp), which is actively maintained. `pydub` and `libav` are no longer needed.

## Requirements

1. **Python packages**
   ```
   py -m pip install -U -r requirements.txt
   ```
   (`yt-dlp[default]` includes `yt-dlp-ejs`, which YouTube downloads now need.)

2. **Deno** (JavaScript runtime yt-dlp uses to solve YouTube's player challenges):
   ```
   winget install --id=DenoLand.Deno
   ```

3. **ffmpeg**: needed for mp3 conversion and for merging high-quality video with its audio. Either install it and add it to PATH, or put `ffmpeg.exe` in the same folder as the program / `.exe`.

## Run

```
py ytdownloader.py
```

## Build the .exe

```
py -m PyInstaller --onefile --collect-data yt_dlp_ejs ytdownloader.py
```

The executable is written to `dist\ytdownloader.exe`. Copy `ffmpeg.exe` next to it if ffmpeg isn't on PATH. Deno still needs to be installed on the machine that runs it.

## If it stops working again

YouTube changes frequently. Usually the fix is just updating yt-dlp and rebuilding:

```
py -m pip install -U "yt-dlp[default]"
py -m PyInstaller --onefile --collect-data yt_dlp_ejs ytdownloader.py
```
