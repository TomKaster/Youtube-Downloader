# Youtube-Downloader
Downloader for YouTube video and audio.

The downloader asks whether you want video or just audio. Video is saved as **mp4**, audio as **mp3**, both to your `Downloads` folder.

> The original version used `pytube`, which stopped working after YouTube changes. It now uses [yt-dlp](https://github.com/yt-dlp/yt-dlp), which is actively maintained. `pydub` and `libav` are no longer needed.

## Requirements (only for running from source — see below for the standalone .exe)

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

## Build the standalone .exe

```
powershell -ExecutionPolicy Bypass -File build.ps1
```

This downloads Deno and ffmpeg into `bin\` (first time only), installs the Python packages, and builds `dist\ytdownloader.exe` with Deno and ffmpeg packed inside. **Users only need that one file** — no Python, Deno or ffmpeg install.

Notes:
- The .exe is large (roughly 100–150 MB) because it carries Deno and ffmpeg, and it takes a few seconds to start while it unpacks them.
- ffmpeg is GPL-licensed; if you distribute the .exe publicly, include a note that it bundles ffmpeg and link to its source (https://ffmpeg.org). Deno is MIT-licensed.

## If it stops working again

YouTube changes frequently. Usually the fix is just rebuilding, which pulls the latest yt-dlp:

```
powershell -ExecutionPolicy Bypass -File build.ps1
```

(Delete `bin\` first if you also want fresh copies of Deno and ffmpeg.)
