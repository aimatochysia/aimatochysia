from PIL import Image, ImageDraw, ImageFont
import random, math, os, base64
import argparse
import sys
import xml.etree.ElementTree as ET

NAME = "Petra Michael"
W, H = 1200, 420
BUBBLE_COUNT = 1000
DURATION = 1.0
BUBBLE_MIN_R, BUBBLE_MAX_R = 3, 8
OUTPUT_PATH = "banner.svg"

SHOW_GHOST_LABEL = False
SHOW_FINAL_TEXT = False

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

def load_font(size: int) -> ImageFont.FreeTypeFont:
	paths = [
		"/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
		"/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
		"/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
		"C:/Windows/Fonts/arialbd.ttf",
		"C:/Windows/Fonts/Arialbd.ttf",
		"C:/Windows/Fonts/segoeuib.ttf",
	]
	for p in paths:
		if os.path.exists(p):
			return ImageFont.truetype(p, size=size)
	return ImageFont.load_default()

def _measure(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont):
	try:
		x0, y0, x1, y1 = draw.textbbox((0, 0), text, font=font)
		return x1 - x0, y1 - y0
	except Exception:
		return draw.textsize(text, font=font)

def sample_text_points(name: str, w: int, h: int, target: int):
	scale = 4
	img = Image.new("L", (w * scale, h * scale), color=0)
	draw = ImageDraw.Draw(img)

	font_size = int(h * 0.8 * scale)
	font = load_font(font_size)
	txt_w, txt_h = _measure(draw, name, font)
	while txt_w > w * scale * 0.92 and font_size > 10:
		font_size = int(font_size * 0.95)
		font = load_font(font_size)
		txt_w, txt_h = _measure(draw, name, font)

	x = (w * scale - txt_w) / 2
	y = (h * scale - txt_h) / 2 - int(0.04 * h * scale)
	draw.text((x, y), name, fill=255, font=font)

	px = img.load()
	points = []
	step = max(1, scale)
	for iy in range(0, h * scale, step):
		for ix in range(0, w * scale, step):
			if px[ix, iy] > 128:
				points.append((ix / scale, iy / scale))

	if not points:
		return [(w / 2, h / 2)] * max(1, target)

	random.shuffle(points)
	if len(points) > target:
		points = points[:target]
	elif len(points) < target:
		extras = target - len(points)
		points.extend(random.choices(points, k=extras))
	return points

def hsl_to_hex(h, s, l):
	import colorsys
	r, g, b = colorsys.hls_to_rgb(h / 360.0, l / 100.0, s / 100.0)
	return '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))

def make_svg(name, w, h, bubble_count, duration, out_path):
	final_positions = sample_text_points(name, w, h, bubble_count)
	if len(final_positions) < bubble_count:
		extras = bubble_count - len(final_positions)
		for _ in range(extras):
			final_positions.append((random.uniform(0, w), random.uniform(0, h)))
	random.shuffle(final_positions)

	starts = [(random.uniform(-0.2 * w, 1.2 * w), random.uniform(-0.2 * h, 1.2 * h)) for _ in range(bubble_count)]
	radii = [random.uniform(BUBBLE_MIN_R, BUBBLE_MAX_R) for _ in range(bubble_count)]

	colors = []
	base_h = random.uniform(180, 300)
	for _ in range(bubble_count):
		hue = (base_h + random.uniform(-30, 30)) % 360
		sat = random.uniform(40, 75)
		lig = random.uniform(55, 85)
		colors.append(hsl_to_hex(hue, sat, lig))

	svg_parts = []
	svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet">')
	svg_parts.append(f'<title>{name} — particle reveal</title><desc>Animated particles coalescing to form the name</desc>')
	svg_parts.append(f'<rect width="100%" height="100%" fill="#0f1724"/>')
	svg_parts.append('<defs><style>.bubble{mix-blend-mode:screen;}</style></defs>')
	if SHOW_GHOST_LABEL:
		svg_parts.append(f'<text x="{w/2}" y="{h/2}" font-family="DejaVu Sans, Arial" font-size="{int(h*0.65)}" text-anchor="middle" fill="#ffffff" opacity="0.03">{name}</text>')

	for i in range(bubble_count):
		sx, sy = starts[i]
		fx, fy = final_positions[i]
		r = radii[i]
		color = colors[i]
		cx = (sx + fx) / 2 + random.uniform(-0.25 * w, 0.25 * w)
		cy = (sy + fy) / 2 + random.uniform(-0.25 * h, 0.25 * h)
		path = f"M {sx:.2f} {sy:.2f} Q {cx:.2f} {cy:.2f} {fx:.2f} {fy:.2f}"
		delay = random.uniform(0, duration * 0.5)
		ind_dur = duration * random.uniform(0.85, 1.15)
		begin = f"{delay:.2f}s"

		svg_parts.append('<g class="bubble" transform="translate(0,0)">')
		svg_parts.append(f'  <circle cx="0" cy="0" r="{r:.2f}" fill="{color}" opacity="0.95">')
		svg_parts.append(f'    <animateMotion begin="{begin}" dur="{ind_dur:.2f}s" fill="freeze" calcMode="spline" keySplines="0.42 0 0.58 1" path="{path}"/>')
		svg_parts.append(f'    <animate attributeName="r" begin="{begin}" dur="{ind_dur:.2f}s" fill="freeze" values="{r*0.2:.2f};{r*1.15:.2f};{r:.2f}" keyTimes="0;0.92;1" calcMode="spline" keySplines="0.3 0 0.1 1;0.4 0 0.2 1"/>')
		svg_parts.append(f'    <animate attributeName="opacity" begin="{begin}" dur="{ind_dur:.2f}s" fill="freeze" values="0;0.9;0.95" keyTimes="0;0.7;1"/>')
		svg_parts.append('  </circle>')
		svg_parts.append('</g>')

	if SHOW_FINAL_TEXT:
		svg_parts.append(f'<text x="{w/2}" y="{h/2 + h*0.05}" font-family="DejaVu Sans, Arial" font-weight="700" font-size="{int(h*0.55)}" text-anchor="middle" fill="white" opacity="0">')
		svg_parts.append(f'  <animate attributeName="opacity" begin="{duration*0.85:.2f}s" dur="{duration*0.25:.2f}s" fill="freeze" values="0;1"/>')
		svg_parts.append(f'  {name}')
		svg_parts.append('</text>')

	svg_parts.append('</svg>')

	svg_content = "\n".join(svg_parts)
	with open(out_path, "w", encoding="utf-8") as f:
		f.write(svg_content)
	return out_path, svg_content

def _local(tag: str) -> str:
	return tag.rsplit("}", 1)[-1] if "}" in tag else tag

def remove_animated_overlays(root: ET.Element, keep_overlays: bool = False) -> int:
	if keep_overlays:
		return 0
	removed = 0
	for parent in list(root.iter()):
		children = list(parent)
		for child in children:
			if _local(child.tag) != "rect":
				continue
			opacity_attr = child.attrib.get("opacity")
			try:
				base_opacity = float(opacity_attr) if opacity_attr is not None else 1.0
			except ValueError:
				base_opacity = 1.0
			has_animation = any(_local(gc.tag).startswith("animate") for gc in list(child))
			if has_animation and base_opacity <= 0.1:
				parent.remove(child)
				removed += 1
	return removed

def process(in_path: str, out_path: str, keep_overlays: bool = False) -> int:
	tree = ET.parse(in_path)
	root = tree.getroot()
	removed = remove_animated_overlays(root, keep_overlays=keep_overlays)
	tree.write(out_path, encoding="utf-8", xml_declaration=False)
	return removed

def main(argv=None) -> int:
	parser = argparse.ArgumentParser(description="Sanitize SVG: remove animated low-opacity overlay rects (shimmer).")
	parser.add_argument("--in", dest="in_path", default=r"c:\Assignments\Coding\aimatochysia\assets\banner.svg", help="Input SVG path.")
	parser.add_argument("--out", dest="out_path", default=None, help="Output SVG path (default: overwrite input).")
	parser.add_argument("--keep-overlays", action="store_true", help="Keep animated overlay rects (do not remove).")
	args = parser.parse_args(argv)

	out_path = args.out_path or args.in_path
	removed = process(args.in_path, out_path, keep_overlays=args.keep_overlays)
	print(f"Removed {removed} overlay rect(s)." if not args.keep_overlays else "Kept overlays (no removals).")
	return 0

if __name__ == "__main__":
	out, svg = make_svg(NAME, W, H, BUBBLE_COUNT, DURATION, OUTPUT_PATH)
	print("Saved:", out)
	sys.exit(main())
