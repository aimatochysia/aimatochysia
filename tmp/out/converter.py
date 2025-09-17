from moviepy import VideoFileClip
from PIL import Image
from tqdm import tqdm

def video_to_gif(input_video_path, output_gif_path, start_time=0, end_time=None, fps=15, colors=128):
    clip = VideoFileClip(input_video_path)
    if end_time is None:
        end_time = clip.duration
    subclip = clip.subclipped(start_time, end_time)
    video_frames = [frame for frame in subclip.iter_frames(fps=fps, dtype='uint8', logger=None)]
    
    frames_as_pil = []
    for i, frame in tqdm(enumerate(video_frames), total=len(video_frames), desc="Converting frames", unit="frame"):
        pil_frame = Image.fromarray(frame)
        if pil_frame.mode == 'RGBA':
            frames_as_pil.append(pil_frame.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=colors))
        else:
            frames_as_pil.append(pil_frame.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=colors))
    
    frames_as_pil[0].save(output_gif_path, save_all=True, append_images=frames_as_pil[1:], optimize=False, duration=1000/fps, loop=0, dither=Image.FLOYDSTEINBERG)
    print(f"GIF saved to {output_gif_path}")

video_to_gif("final.mkv", "output.gif", fps=24, colors=256)
