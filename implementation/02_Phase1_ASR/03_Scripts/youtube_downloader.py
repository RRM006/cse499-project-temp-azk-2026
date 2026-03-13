#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube Audio Downloader for CSE499 Project
Downloads audio from YouTube for dataset collection
"""

import os
import yt_dlp
import argparse
import json
import csv
from datetime import datetime
from tqdm import tqdm


class YouTubeDownloader:
    """Download audio from YouTube videos."""
    
    def __init__(
        self,
        output_dir: str,
        format='wav',
        quality='192',
        verbose=False
    ):
        """
        Initialize YouTube downloader.
        
        Args:
            output_dir: Directory to save downloaded files
            format: Audio format (wav, mp3, etc.)
            quality: Audio quality
            verbose: Print verbose output
        """
        self.output_dir = output_dir
        self.format = format
        self.quality = quality
        self.verbose = verbose
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
    
    def get_video_info(self, url: str) -> dict:
        """
        Get video information without downloading.
        
        Args:
            url: YouTube video URL
        
        Returns:
            dict: Video information
        """
        ydl_opts = {'quiet': True, 'no_warnings': True}
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', ''),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', ''),
                    'upload_date': info.get('upload_date', ''),
                    'description': info.get('description', ''),
                    'id': info.get('id', ''),
                }
            except Exception as e:
                return {'error': str(e)}
    
    def download_audio(
        self,
        url: str,
        filename: str = None,
        metadata: dict = None
    ) -> dict:
        """
        Download audio from a single YouTube video.
        
        Args:
            url: YouTube video URL
            filename: Output filename (without extension)
            metadata: Additional metadata to save
        
        Returns:
            dict: Download result
        """
        if filename is None:
            filename = "%(title)s"
        
        output_template = os.path.join(self.output_dir, f"{filename}.%(ext)s")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': self.format,
                'preferredquality': self.quality,
            }],
            'quiet': not self.verbose,
            'no_warnings': not self.verbose,
        }
        
        result = {
            'url': url,
            'filename': None,
            'success': False,
            'error': None,
            'duration': 0,
            'metadata': metadata or {}
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract info first
                info = ydl.extract_info(url, download=False)
                result['duration'] = info.get('duration', 0)
                result['metadata']['title'] = info.get('title', '')
                result['metadata']['uploader'] = info.get('uploader', '')
                
                # Download
                ydl.download([url])
                
                # Get actual filename
                actual_filename = f"{filename}.{self.format}"
                if os.path.exists(os.path.join(self.output_dir, actual_filename)):
                    result['filename'] = actual_filename
                    result['success'] = True
        
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def download_batch(
        self,
        urls_file: str,
        results_file: str = None,
        start_index: int = 0
    ) -> list:
        """
        Download audio from multiple URLs.
        
        Args:
            urls_file: CSV file with URLs (column: url)
            results_file: File to save results
            start_index: Starting index for filenames
        
        Returns:
            list: List of download results
        """
        # Load URLs
        urls = []
        with open(urls_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                urls.append(row)
        
        results = []
        
        for i, row in enumerate(tqdm(urls, desc="Downloading")):
            url = row.get('url', '')
            if not url:
                continue
            
            # Get filename from row or use index
            filename = row.get('filename', f"audio_{start_index + i:04d}")
            
            # Get metadata
            metadata = {
                'dialect': row.get('dialect', ''),
                'source': row.get('source', 'youtube'),
                'source_url': url,
                'category': row.get('category', ''),
            }
            
            # Download
            result = self.download_audio(url, filename, metadata)
            results.append(result)
            
            # Save progress
            if results_file:
                self.save_results(results, results_file)
        
        return results
    
    def download_from_search(
        self,
        search_query: str,
        max_results: int = 10,
        filename_prefix: str = None
    ) -> list:
        """
        Search and download from YouTube.
        
        Args:
            search_query: Search query
            max_results: Maximum number of results
            filename_prefix: Prefix for filenames
        
        Returns:
            list: List of download results
        """
        # Use YouTube search URL
        search_url = f"ytsearch{max_results}:{search_query}"
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(
                self.output_dir,
                f"{filename_prefix or '%(title)s'}.%(ext)s"
            ),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': self.format,
                'preferredquality': self.quality,
            }],
            'quiet': not self.verbose,
        }
        
        results = []
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([search_url])
                results.append({'success': True, 'query': search_query})
        except Exception as e:
            results.append({'success': False, 'error': str(e)})
        
        return results
    
    def save_results(self, results: list, filepath: str) -> None:
        """Save download results to JSON file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
    
    def create_url_spreadsheet_template(self, filepath: str) -> None:
        """Create a template CSV for URL collection."""
        headers = ['url', 'dialect', 'category', 'filename', 'notes']
        
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows([
                {
                    'url': 'https://youtube.com/watch?v=EXAMPLE',
                    'dialect': 'dhaka',
                    'category': 'symptom',
                    'filename': 'dhaka_symptom_001',
                    'notes': 'Patient describing symptoms'
                }
            ])
        
        print(f"Template created: {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description="Download audio from YouTube"
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Output directory"
    )
    parser.add_argument(
        "--url", "-u",
        help="Single YouTube URL to download"
    )
    parser.add_argument(
        "--urls-file", "-f",
        help="CSV file with URLs"
    )
    parser.add_argument(
        "--format",
        default="wav",
        choices=["wav", "mp3", "flac", "ogg"],
        help="Audio format"
    )
    parser.add_argument(
        "--quality",
        default="192",
        help="Audio quality (bitrate)"
    )
    parser.add_argument(
        "--template", "-t",
        action="store_true",
        help="Create URL template file"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    if args.template:
        downloader = YouTubeDownloader(args.output)
        downloader.create_url_spreadsheet_template("youtube_urls_template.csv")
        return
    
    downloader = YouTubeDownloader(
        args.output,
        format=args.format,
        quality=args.quality,
        verbose=args.verbose
    )
    
    if args.url:
        # Download single URL
        result = downloader.download_audio(args.url)
        print(f"Download {'successful' if result['success'] else 'failed'}")
        if result['error']:
            print(f"Error: {result['error']}")
    
    elif args.urls_file:
        # Download batch from file
        results = downloader.download_batch(args.urls_file)
        print(f"\nDownloaded {len(results)} videos")
        success_count = sum(1 for r in results if r['success'])
        print(f"Success: {success_count}")
        print(f"Failed: {len(results) - success_count}")
    
    else:
        print("Please provide --url or --urls-file")


if __name__ == "__main__":
    main()
