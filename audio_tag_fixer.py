#!/usr/bin/env python3
"""
Audio Tag Fixer - Fix separator issues in Title and Artist tags
Fixes: null bytes (\x00), double backslashes (\\), and single backslashes (\)
Replaces them with proper comma-space separators (", ")
Supports: MP3, FLAC, M4A, WAV, OGG, WMA, AAC

Cross-platform standalone executable - no external dependencies required
Works on Windows, Mac, and Linux
"""

import os
import sys
import shutil
from pathlib import Path
import argparse
import re

try:
    from mutagen import File
    from mutagen.id3 import TIT2, TPE1
    from mutagen.mp3 import MP3
    from mutagen.flac import FLAC
    from mutagen.mp4 import MP4
    from mutagen.oggvorbis import OggVorbis
    from mutagen.asf import ASF
except ImportError:
    print("ERROR: mutagen library not found!")
    print("Please install it with: pip install mutagen")
    print("Or if creating exe: pip install mutagen pyinstaller")
    input("Press Enter to exit...")
    sys.exit(1)

def create_backup_dir(audio_dir):
    """Create backup directory if it doesn't exist"""
    backup_dir = audio_dir / "backup"
    backup_dir.mkdir(exist_ok=True)
    return backup_dir

def backup_file(file_path, backup_dir):
    """Create backup of the original file"""
    backup_path = backup_dir / f"{file_path.name}.backup"
    shutil.copy2(file_path, backup_path)
    return backup_path

def fix_tag_value(value):
    """Replace problematic separators with proper comma-space separators"""
    if isinstance(value, list):
        return [fix_single_value(v) if isinstance(v, str) else v for v in value]
    elif isinstance(value, str):
        return fix_single_value(value)
    return value

def fix_single_value(text):
    """Fix separators in a single text value"""
    if not isinstance(text, str):
        return text
    
    # Replace null bytes with comma-space
    text = text.replace('\x00', ', ')
    
    # Replace double backslashes with comma-space
    text = text.replace('\\\\', ', ')
    
    # Replace single backslashes with comma-space (but be careful with paths)
    # Only replace if it's clearly a separator (surrounded by letters/numbers)
    text = re.sub(r'([a-zA-Z0-9])\\\s*([a-zA-Z])', r'\1, \2', text)
    
    # Clean up any double commas or extra spaces
    text = re.sub(r',\s*,', ',', text)  # Remove double commas
    text = re.sub(r',\s+', ', ', text)  # Standardize comma spacing
    text = re.sub(r'\s+', ' ', text)    # Remove extra spaces
    
    return text.strip()

def has_formatting_issues(text):
    """Check if text has formatting issues that need fixing"""
    if not isinstance(text, str):
        return False
    return ('\x00' in text or '\\\\' in text or 
            bool(re.search(r'[a-zA-Z0-9]\\\s*[a-zA-Z]', text)))

def process_file(file_path, backup_dir):
    """Process a single audio file"""
    print(f"Processing: {file_path.name}")
    
    try:
        # Load the audio file
        audio_file = File(file_path)
        if audio_file is None:
            print(f"  ✗ Could not read file: {file_path.name}")
            return False
        
        modified = False
        changes = []
        
        # Variables to store current metadata
        current_title = "Unknown"
        current_artist = "Unknown"
        
        # Check different tag formats
        if isinstance(audio_file, MP3):
            # MP3 ID3 tags
            title_tag = audio_file.get('TIT2')
            artist_tag = audio_file.get('TPE1')
            
            if title_tag:
                current_title = str(title_tag.text[0])
            if artist_tag:
                current_artist = str(artist_tag.text[0])
            
            if title_tag and has_formatting_issues(str(title_tag)):
                backup_file(file_path, backup_dir)
                old_title = str(title_tag)
                new_title = fix_single_value(old_title)
                audio_file['TIT2'] = TIT2(encoding=3, text=[new_title])
                changes.append(f"Title: '{old_title}' → '{new_title}'")
                modified = True
                current_title = new_title
            
            if artist_tag and has_formatting_issues(str(artist_tag)):
                if not modified:  # Only backup once
                    backup_file(file_path, backup_dir)
                old_artist = str(artist_tag)
                new_artist = fix_single_value(old_artist)
                audio_file['TPE1'] = TPE1(encoding=3, text=[new_artist])
                changes.append(f"Artist: '{old_artist}' → '{new_artist}'")
                modified = True
                current_artist = new_artist
                
        elif isinstance(audio_file, MP4):
            # M4A tags
            title_tag = audio_file.get('©nam')
            artist_tag = audio_file.get('©ART')
            
            if title_tag:
                current_title = str(title_tag[0])
            if artist_tag:
                current_artist = str(artist_tag[0])
            
            if title_tag and has_formatting_issues(str(title_tag[0])):
                backup_file(file_path, backup_dir)
                old_title = str(title_tag[0])
                new_title = fix_single_value(old_title)
                audio_file['©nam'] = [new_title]
                changes.append(f"Title: '{old_title}' → '{new_title}'")
                modified = True
                current_title = new_title
            
            if artist_tag and has_formatting_issues(str(artist_tag[0])):
                if not modified:
                    backup_file(file_path, backup_dir)
                old_artist = str(artist_tag[0])
                new_artist = fix_single_value(old_artist)
                audio_file['©ART'] = [new_artist]
                changes.append(f"Artist: '{old_artist}' → '{new_artist}'")
                modified = True
                current_artist = new_artist
                
        else:
            # Generic tags (FLAC, OGG, etc.)
            title_tag = audio_file.get('TITLE') or audio_file.get('title')
            artist_tag = audio_file.get('ARTIST') or audio_file.get('artist')
            
            if title_tag:
                current_title = str(title_tag[0] if isinstance(title_tag, list) else title_tag)
            if artist_tag:
                current_artist = str(artist_tag[0] if isinstance(artist_tag, list) else artist_tag)
            
            title_text = str(title_tag[0] if isinstance(title_tag, list) else title_tag) if title_tag else ""
            artist_text = str(artist_tag[0] if isinstance(artist_tag, list) else artist_tag) if artist_tag else ""
            
            if title_tag and has_formatting_issues(title_text):
                backup_file(file_path, backup_dir)
                old_title = title_text
                new_title = fix_single_value(old_title)
                audio_file['TITLE'] = [new_title]
                changes.append(f"Title: '{old_title}' → '{new_title}'")
                modified = True
                current_title = new_title
            
            if artist_tag and has_formatting_issues(artist_text):
                if not modified:
                    backup_file(file_path, backup_dir)
                old_artist = artist_text
                new_artist = fix_single_value(old_artist)
                audio_file['ARTIST'] = [new_artist]
                changes.append(f"Artist: '{old_artist}' → '{new_artist}'")
                modified = True
                current_artist = new_artist
        
        # Print current metadata
        print(f"  🎵 Song: {current_title}")
        print(f"  🎤 Artist: {current_artist}")
        
        if modified:
            audio_file.save()
            for change in changes:
                print(f"  ✓ {change}")
            return True
        else:
            print("  - No changes needed")
            return False
            
    except Exception as e:
        print(f"  ✗ Error processing {file_path.name}: {str(e)}")
        return False

def main():
    print("Audio Tag Fixer - Python Version")
    print("=" * 50)
    print("This script fixes separator issues in Title and Artist tags:")
    print("• Replaces null bytes (\\x00) with ', '")
    print("• Replaces double backslashes (\\\\) with ', '") 
    print("• Replaces single backslashes (\\) with ', '")
    print()
    
    # Get the directory where the script is located
    if getattr(sys, 'frozen', False):
        # If running as exe
        script_dir = Path(sys.executable).parent
    else:
        # If running as Python script
        script_dir = Path(__file__).parent
    
    print(f"Processing audio files in: {script_dir}")
    print()
    
    # Create backup directory
    backup_dir = create_backup_dir(script_dir)
    
    # Supported audio extensions
    audio_extensions = {'.mp3', '.flac', '.m4a', '.wav', '.ogg', '.wma', '.aac'}
    
    # Find audio files in current directory only
    audio_files = []
    for ext in audio_extensions:
        audio_files.extend(script_dir.glob(f"*{ext}"))
        audio_files.extend(script_dir.glob(f"*{ext.upper()}"))
    
    if not audio_files:
        print("No audio files found in the current directory.")
        input("Press Enter to exit...")
        return
    
    print(f"Found {len(audio_files)} audio file(s)")
    print()
    
    # Process files
    processed = 0
    modified = 0
    
    for audio_file in sorted(audio_files):
        processed += 1
        if process_file(audio_file, backup_dir):
            modified += 1
        print()
    
    # Summary
    print("=" * 50)
    print("Processing complete!")
    print(f"Files processed: {processed}")
    print(f"Files modified: {modified}")
    print(f"Backups saved in: {backup_dir}")
    print("=" * 50)
    
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()