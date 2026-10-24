import sys
import subprocess
import os
from moviepy import VideoFileClip

# --- AUTO-INSTALLER (Comment this out if already installed)---
# This forces the exact Python environment running this script to install the library to itself, bypassing Windows terminal glitches.
# print("Syncing environment and checking for moviepy...")
# try:
#     subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy", "--quiet"])
# except Exception as e:
#     print(f"Warning: Auto-install failed, but we will try to proceed: {e}")

def convert_avi_to_mp4(input_path, output_path):
    print(f"\nLoading '{input_path}'...")
    
    try:
        clip = VideoFileClip(input_path)
        
        # Calculate size limits (20,000 KB target)
        max_size_kb = 20000 
        max_bits = max_size_kb * 1024 * 8 
        allowed_bps = max_bits / clip.duration
        audio_bps = 128000
        
        video_bps = allowed_bps - audio_bps
        video_kbps = int(video_bps / 1000)
        
        if video_kbps < 100:
            print("Warning: Video is too long to fit in 20,000 KB with good quality.")
            video_kbps = 100 
            
        high_quality_kbps = 5000
        
        if video_kbps < high_quality_kbps:
            print(f"Targeting 20,000 KB limit! Dynamically shrinking video quality to {video_kbps}k...")
            final_bitrate = f"{video_kbps}k"
        else:
            print("Video will naturally fall under 20,000 KB. Using maximum quality...")
            final_bitrate = f"{high_quality_kbps}k"
            
        # Convert and write the file
        clip.write_videofile(
            output_path, 
            codec="libx264", 
            audio_codec="aac",
            preset="slow",             
            bitrate=final_bitrate,     
            audio_bitrate="128k"       
        )
        
        clip.close()
        print(f"Success! Saved to '{output_path}'")
        
    except Exception as e:
        print(f"An error occurred while processing '{input_path}': {e}")

# Folder Setup
input_folder = "."
output_folder = "converted_mp4s"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

processed_count = 0

# Scan and convert
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".avi"):
        input_path = os.path.join(input_folder, filename)
        
        base_name = os.path.splitext(filename)[0]
        output_filename = f"{base_name}.mp4"
        output_path = os.path.join(output_folder, output_filename)
        
        print(f"\n--- Starting conversion for: {filename} ---")
        convert_avi_to_mp4(input_path, output_path)
        processed_count += 1

print(f"\nBatch conversion complete! Processed {processed_count} files.")