import os
import glob
import imageio

frames_dir = "/config/Desktop/Session1/smart-recipe-assistant/scratch/frames"
output_file = "/config/Desktop/Session1/smart-recipe-assistant/scratch/demo_video.mp4"

frame_files = sorted(glob.glob(os.path.join(frames_dir, "frame_*.png")))
print(f"Compiling {len(frame_files)} frames into {output_file}...")

writer = imageio.get_writer(output_file, fps=5, codec="libx264", quality=8)
for ff in frame_files:
    img = imageio.v3.imread(ff)
    writer.append_data(img)
writer.close()

print(f"Video compiled successfully at {output_file}! File size: {os.path.getsize(output_file)} bytes")
