import os
import sys
from pathlib import Path
import codecs
import chardet
import argparse
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import time

# 设置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('encoding_fix.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def detect_encoding(file_path):
    """Detect the encoding of a file using chardet with retry mechanism"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            with open(file_path, 'rb') as f:
                raw = f.read()
            result = chardet.detect(raw)
            confidence = result.get('confidence', 0)
            encoding = result.get('encoding')
            
            if confidence > 0.8 and encoding:
                return encoding
            elif attempt < max_retries - 1:
                logger.warning(f"Low confidence ({confidence}) for {file_path}, retrying...")
                time.sleep(0.1)  # Short delay before retry
            else:
                logger.warning(f"Could not detect encoding with high confidence for {file_path}")
                return None
        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"Error detecting encoding for {file_path}, attempt {attempt + 1}: {e}")
                time.sleep(0.1)
            else:
                logger.error(f"Failed to detect encoding for {file_path} after {max_retries} attempts: {e}")
                return None

def fix_file_encoding(file_path, target_encoding='utf-8', dry_run=False):
    """Fix the encoding of a single file"""
    try:
        # First detect the encoding
        detected_encoding = detect_encoding(file_path)
        logger.info(f"Detected encoding for {file_path}: {detected_encoding}")
        
        if dry_run:
            logger.info(f"[DRY RUN] Would process {file_path} from {detected_encoding} to {target_encoding}")
            return True
            
        # Read the file content in binary mode
        with open(file_path, 'rb') as f:
            content = f.read()
            
        # Try to decode with the detected encoding first
        decoded_content = None
        if detected_encoding:
            try:
                decoded_content = content.decode(detected_encoding)
                logger.debug(f"Successfully decoded with detected encoding: {detected_encoding}")
            except (UnicodeDecodeError, TypeError) as e:
                logger.debug(f"Failed to decode with detected encoding: {e}")
        
        # If that fails, try other encodings
        if decoded_content is None:
            encodings = [
                'utf-8-sig', 'utf-8', 'gbk', 'gb2312', 'gb18030', 
                'big5', 'cp936', 'cp950', 'cp1252', 'latin1',
                'ascii', 'iso-8859-1'
            ]
            
            for encoding in encodings:
                try:
                    decoded_content = content.decode(encoding)
                    logger.info(f"Successfully decoded with {encoding}")
                    break
                except UnicodeDecodeError:
                    continue
                    
        if decoded_content is None:
            logger.error(f"Failed to decode {file_path} with any encoding")
            return False
            
        # Clean up the content
        # Remove BOM if present
        if decoded_content.startswith('\ufeff'):
            decoded_content = decoded_content[1:]
            logger.debug("Removed BOM marker")
            
        # Normalize line endings
        decoded_content = decoded_content.replace('\r\n', '\n').replace('\r', '\n')
        
        # Replace problematic characters
        replacements = {
            '\u20ac': '',  # Euro sign
            '\ufffd': '',  # Replacement character
            '\u200b': '',  # Zero width space
            '\u200e': '',  # Left-to-right mark
            '\u200f': '',  # Right-to-left mark
        }
        for old, new in replacements.items():
            if old in decoded_content:
                decoded_content = decoded_content.replace(old, new)
                logger.debug(f"Replaced character {ord(old)}")
            
        # Write back with target encoding
        with open(file_path, 'w', encoding=target_encoding, newline='\n') as f:
            f.write(decoded_content)
            
        logger.info(f"Successfully processed {file_path}")
        return True
            
    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")
        return False

def process_files_parallel(files, target_encoding, dry_run, max_workers=None):
    """Process multiple files in parallel"""
    success_count = 0
    failure_count = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(fix_file_encoding, file_path, target_encoding, dry_run): file_path 
            for file_path in files
        }
        
        with tqdm(total=len(files), desc="Processing files") as pbar:
            for future in as_completed(futures):
                file_path = futures[future]
                try:
                    success = future.result()
                    if success:
                        success_count += 1
                    else:
                        failure_count += 1
                except Exception as e:
                    logger.error(f"Unexpected error processing {file_path}: {e}")
                    failure_count += 1
                pbar.update(1)
    
    return success_count, failure_count

def main():
    parser = argparse.ArgumentParser(description='Fix file encodings in a project')
    parser.add_argument('--path', default='.', help='Path to process (default: current directory)')
    parser.add_argument('--target-encoding', default='utf-8', help='Target encoding (default: utf-8)')
    parser.add_argument('--file-types', default='.py,.txt,.md', help='Comma-separated list of file extensions to process')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    parser.add_argument('--workers', type=int, default=None, help='Number of worker threads (default: CPU count)')
    args = parser.parse_args()
    
    start_time = time.time()
    file_types = args.file_types.split(',')
    files_to_process = []
    
    # Collect all files to process
    for root, dirs, files in os.walk(args.path):
        # Skip common directories to ignore
        dirs[:] = [d for d in dirs if d not in {'.git', '.venv', '__pycache__', 'node_modules'}]
        
        for file in files:
            if any(file.endswith(ext) for ext in file_types):
                file_path = Path(root) / file
                files_to_process.append(file_path)
    
    if not files_to_process:
        logger.warning("No files found to process!")
        return
    
    logger.info(f"Found {len(files_to_process)} files to process")
    if args.dry_run:
        logger.info("Running in dry-run mode - no changes will be made")
    
    success_count, failure_count = process_files_parallel(
        files_to_process,
        args.target_encoding,
        args.dry_run,
        args.workers
    )
    
    duration = time.time() - start_time
    logger.info(f"\nProcessing complete in {duration:.2f} seconds")
    logger.info(f"Successfully processed: {success_count} files")
    if failure_count > 0:
        logger.warning(f"Failed to process: {failure_count} files")

if __name__ == '__main__':
    main() 