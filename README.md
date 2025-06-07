# Audio Tag Fixer

A cross-platform tool to fix separator issues in audio file metadata (Title and Artist tags).

## What it fixes

The tool automatically detects and fixes these separator issues in audio metadata:
- **Null bytes** (`\x00`) → replaced with `", "`
- **Double backslashes** (`\\`) → replaced with `", "`  
- **Single backslashes** (`\`) → replaced with `", "`

### Example fixes:
- `"Nova\x00Mike"` → `"Nova, Mike"`
- `"KSHMR\x00DallasK\x00JAKE\larry"` → `"KSHMR, DallasK, JAKE, larry"`
- `"Artist1\\Artist2"` → `"Artist1, Artist2"`

## Supported formats
- MP3, FLAC, M4A, WAV, OGG, WMA, AAC

## Downloads

### Mac (macOS)
- **File**: `AudioTagFixer-Mac`
- **Requirements**: macOS 10.12+ (compatible with both Intel and Apple Silicon)

### Windows
- **File**: `AudioTagFixer-Windows.exe` 
- **Requirements**: Windows 7+ (64-bit)

## How to use

### Mac:
1. Download `AudioTagFixer-Mac`
2. Open Terminal and navigate to the folder containing your audio files
3. Run: `./AudioTagFixer-Mac`
4. The tool will process all audio files in the current directory

### Windows:
1. Download `AudioTagFixer-Windows.exe`
2. Place the executable in the folder containing your audio files
3. Double-click `AudioTagFixer-Windows.exe` or run it from Command Prompt
4. The tool will process all audio files in the current directory

## Features

- ✅ **Automatic backup**: Creates backup copies before making changes
- ✅ **UTF-8 safe**: Properly handles international characters
- ✅ **Smart detection**: Only fixes actual separator issues
- ✅ **Multiple formats**: Supports all major audio formats
- ✅ **Standalone**: No installation required, no external dependencies

## Building from source

If you want to build the executables yourself:

### Prerequisites:
```bash
pip install mutagen pyinstaller
```

### Mac version:
```bash
pyinstaller AudioTagFixer.spec --clean
cp dist/AudioTagFixer dist/AudioTagFixer-Mac
```

### Windows version (on Windows):
```bash
pyinstaller AudioTagFixer-Windows.spec --clean
```

## Technical details

The tool uses the `mutagen` library to read and write audio metadata. It creates a `backup` folder in the working directory and saves original files before making any changes.

## License

Free to use and distribute.

---

**⚠️ Note**: Always keep backups of your audio files before running any metadata modification tools! 