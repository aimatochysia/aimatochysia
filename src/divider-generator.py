import argparse
import math
import os
from pathlib import Path
from typing import List

def sine_path(width: float, height: float, amplitude: float, frequency: float, phase: float, samples: int = 240, y_center: float | None = None) -> str:
	yc = y_center if y_center is not None else height / 2.0
	parts = []
	for i in range(samples + 1):
		t = i / samples
		x = t * width
		y = yc + amplitude * math.sin(2 * math.pi * frequency * t + phase)
		parts.append((x, y))
	d = f"M {parts[0][0]:.2f} {parts[0][1]:.2f}"
	for x, y in parts[1:]:
		d += f" L {x:.2f} {y:.2f}"
	return d

def build_svg(width: int, height: int, colors: List[str], speed: float, layers: int = 3, cycles: float = 2.0, fade_ratio: float = 0.08) -> str:
	amp_base = max(2.0, height * 0.30)
	stroke_w0 = max(1.5, height * 0.08)
	viewBox = f"0 0 {width} {height}"
	grad_id = "grad"
	glow_id = "glow"
	mask_grad_id = "edgeMaskGrad"
	mask_id = "edgeMask"

	grad = f"""
	<linearGradient id="{grad_id}" x1="0" y1="0" x2="{width}" y2="0" gradientUnits="userSpaceOnUse">
		{''.join(f'<stop offset="{i/(len(colors)-1):.3f}" stop-color="{c.strip()}" />' for i,c in enumerate(colors))}
		<animateTransform attributeName="gradientTransform" type="translate" values="0 0; {width} 0; 0 0" keyTimes="0;0.5;1" dur="{max(1.0, speed*3):.2f}s" repeatCount="indefinite" />
	</linearGradient>
	"""

	filter_glow = f"""
	<filter id="{glow_id}" x="-20%" y="-300%" width="140%" height="700%">
		<feGaussianBlur in="SourceGraphic" stdDeviation="{max(0.6, stroke_w0*0.7):.2f}" result="blur"/>
		<feMerge>
			<feMergeNode in="blur"/>
			<feMergeNode in="SourceGraphic"/>
		</feMerge>
	</filter>
	"""

	fade_ratio = max(0.0, min(0.45, float(fade_ratio)))
	left_pct = fade_ratio * 100.0
	right_pct = 100.0 - left_pct
	mask_grad = f"""
	<linearGradient id="{mask_grad_id}" x1="0" y1="0" x2="{width}" y2="0" gradientUnits="userSpaceOnUse">
		<stop offset="0%" stop-color="black" />
		<stop offset="{left_pct:.3f}%" stop-color="white" />
		<stop offset="{right_pct:.3f}%" stop-color="white" />
		<stop offset="100%" stop-color="black" />
	</linearGradient>
	"""
	mask = f"""
	<mask id="{mask_id}">
		<rect x="0" y="0" width="{width}" height="{height}" fill="url(#{mask_grad_id})" />
	</mask>
	"""

	wave_paths = []
	for i in range(layers):
		amp = amp_base * (0.7 ** i)
		phase = i * math.pi / 3.0
		d = sine_path(width, height, amp, cycles, phase)
		wave_paths.append(d)

	paths_svg = []
	for i, d in enumerate(wave_paths):
		sw = stroke_w0 * (1.0 - 0.18 * i)
		dash = max(5.0, 14.0 - 3.0 * i)
		gap = max(5.0, 12.0 - 2.0 * i)
		offset_cycle = dash + gap
		dur = max(0.8, speed * (0.9 + 0.25 * i))
		paths_svg.append(f'''
		<path d="{d}" fill="none" stroke="url(#{grad_id})" stroke-width="{sw*1.6:.2f}" stroke-linecap="round" stroke-linejoin="round" opacity="0.4" filter="url(#{glow_id})" stroke-dasharray="{dash:.1f} {gap:.1f}">
			<animate attributeName="stroke-dashoffset" values="0; {offset_cycle:.1f}" dur="{dur:.2f}s" repeatCount="indefinite" />
		</path>''')
		paths_svg.append(f'''
		<path id="wave{i}" d="{d}" fill="none" stroke="url(#{grad_id})" stroke-width="{sw:.2f}" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="{dash:.1f} {gap:.1f}">
			<animate attributeName="stroke-dashoffset" values="0; {offset_cycle:.1f}" dur="{dur:.2f}s" repeatCount="indefinite" />
		</path>''')

	spark_dur = max(1.0, speed * 2.2)
	spark = f"""
	<g opacity="0.85">
		<circle r="{max(0.9, stroke_w0*0.5):.2f}" fill="white" filter="url(#{glow_id})" opacity="0.8">
			<animateMotion dur="{spark_dur:.2f}s" rotate="auto" repeatCount="indefinite">
				<mpath xlink:href="#wave0" />
			</animateMotion>
		</circle>
	</g>
	"""

	svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="{viewBox}" preserveAspectRatio="xMidYMid meet">
	<title>Animated Divider</title><desc>Looping gradient waves as a heading divider</desc>
	<defs>
		{grad}
		{filter_glow}
		{mask_grad}
		{mask}
	</defs>
	<g pointer-events="none" mask="url(#{mask_id})">
		{''.join(paths_svg)}
		{spark}
	</g>
</svg>'''
	return svg

def parse_colors(s: str) -> List[str]:
	cols = [c.strip() for c in s.split(",") if c.strip()]
	if len(cols) < 2:
		cols = ["#59DBE0", "#7A9CF5", "#B2F0FF"]
	return cols

def main():
	parser = argparse.ArgumentParser(description="Generate an animated SVG divider.")
	parser.add_argument("--out", default=None, help="Output path (default: ../assets/divider.svg)")
	parser.add_argument("--width", type=int, default=1200)
	parser.add_argument("--height", type=int, default=60)
	parser.add_argument("--colors", type=str, default="#59DBE0,#7A9CF5,#B2F0FF", help="Comma-separated gradient colors")
	parser.add_argument("--speed", type=float, default=1.6, help="Base animation speed in seconds")
	parser.add_argument("--layers", type=int, default=3, help="Number of wave layers (1-5)")
	parser.add_argument("--cycles", type=float, default=2.0, help="Number of sine cycles across width")
	parser.add_argument("--fade", type=float, default=0.08, help="Edge fade ratio (0..0.5) of width per side")
	args = parser.parse_args()

	layers = max(1, min(5, args.layers))
	colors = parse_colors(args.colors)

	here = Path(__file__).resolve().parent
	default_out = (here / ".." / "assets" / "divider.svg").resolve()
	out_path = Path(args.out).resolve() if args.out else default_out
	out_path.parent.mkdir(parents=True, exist_ok=True)

	svg = build_svg(args.width, args.height, colors, args.speed, layers=layers, cycles=args.cycles, fade_ratio=args.fade)
	out_path.write_text(svg, encoding="utf-8")
	print(f"Wrote divider SVG -> {out_path}")

if __name__ == "__main__":
	main()
