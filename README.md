# PyTubeGet 📥

PyTubeGet is a simple desktop application developed in Python that allows you to download videos, playlists, and entire channel content from YouTube quickly and easily. With an intuitive graphical interface, users can download content with just a few clicks.

![image](https://github.com/user-attachments/assets/cf394dba-a149-4854-a27d-ebfa434ebac6)

## Features ✨
- 🎥 Individual video downloads
- 📋 Complete playlist downloads
- 🖥️ Full channel video downloads
- 🎧 Audio-only download option (.m4a)
- 🌈 Modern and clean interface
- 💾 Custom destination folder selection

## Prerequisites 🔧

### Windows
- Windows 7 (with UCRT update) or Windows 10/11
- Optional: Python 3.8+ (if you want run it from main.py)
    - `pytubefix`
    - `Pillow`
### Others
- Python 3.8+
- `python-pytubefix`
- `python-pillow`
- Tkinter
    - `python3-tk` (Debian or Ubuntu)
    - `tk` (Arch)
    - `python3-tkinter` (Fedora)
    - `python-tk` (MacOS)

## Installation and Setup 🚀

### Dependencies
Install the necessary dependencies:

```bash
pip install -r requirements.txt
```

## Usage 🖱️
1. Run `PyTubeGet.exe` or `main.py`
2. Paste the YouTube URL (video, playlist, or channel)
3. Select the destination folder
4. Optional: Check the "Download audio only" checkbox
5. Click "Download"

### Building the Executable (Windows)
1. Clone the repository
2. Install the build dependencies
   - `pyinstaller` and `pyinstaller-versionfile`
4. Navigate to the project directory
5. Run the `build.bat` script

## Contributions 🤝
Contributions are welcome. Please open an issue or submit a pull request.

## License 📄
This project is licensed under the MIT License. See the LICENSE file for more details.

## Disclaimer ⚠️
This project is for educational purposes only. Respect YouTube's terms of service and copyright.
