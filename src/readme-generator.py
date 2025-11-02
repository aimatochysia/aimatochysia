from pathlib import Path
from datetime import datetime
import textwrap

PROFILE = {
    "name": "Petra Michael",
    "title": "Software Developer — Jakarta, Indonesia",
    "tagline": "Dedicated to the development of tools and systems that combine innovation, functionality, and user-focused design.",
    "open_to": "Open to collaboration in software engineering, automation, and applied machine learning.",
    "profile_points": [
        "Current Role: Software Development Engineering Intern at IDEMIA IST",
        "Academic Status: Undergraduate Student at Bina Nusantara University, Computer Science",
        "Primary Focus: Full-stack, data-driven apps, ML systems, workflow optimization",
        "Additional Interests: Creative coding, UI/UX, browser extensions, system integrations",
    ],
    "quote": "“The end of law is not to abolish or restrain, but to preserve and enlarge freedom.”",
}

PROJECTS = [
    {
        "name": "Q-Safe Vault",
        "url": "https://github.com/aimatochysia/qsafevault",
        "desc": "Quantum safe cross-platform password manager",
    },
    {
        "name": "Stock-Screener",
        "url": "https://github.com/aimatochysia/stock-screener",
        "desc": "Screening Indonesian stocks using techniques across fundamentals and technicals; finance + data engineering.",
    },
    {
        "name": "Wallpaper-Engine-Code-Clock",
        "url": "https://github.com/aimatochysia/Wallpaper-Engine-Code-Clock",
        "desc": "Customizable clock wallpaper in a code-language style; aesthetics + practicality.",
    },
    {
        "name": "FicBatch",
        "url": "https://github.com/aimatochysia/ficbatch",
        "desc": "Mobile app for bulk download and reading of AO3 fanfiction; practical and community-driven.",
    },
    {
        "name": "Pinoted",
        "url": "https://github.com/aimatochysia/Discord-RPC",
        "desc": "Sticky note-taking app (Java) with multi-note organization.",
    },
    {
        "name": "Color Picker Extension",
        "url": "https://github.com/aimatochysia/color-picker-extension",
        "desc": "Chrome extension for precise color selection, dynamic backgrounds, and HEX/RGB toggling.",
    },
    {
        "name": "Discord RPC",
        "url": "https://github.com/aimatochysia/Discord-RPC",
        "desc": "Rich presence tool with dynamic app cycling and GIF support.",
    },
]

SKILLS = {
    "Programming Languages": ["Python", "JavaScript", "Dart (Flutter)", "Java", "Jython", "HTML/CSS", "APDU Protocol", "Javacard"],
    "Frameworks and Technologies": ["ReactJS", "Flask", "Flutter", "Jupyter", "Chrome Extension APIs", "NextJS"],
    "Development Practices": ["Git", "GitHub Actions", "VS Code", "Automation workflows", "UI/UX workflows"],
    "Creative and Design": ["Blender3D", "Pixel Art", "Interactive Systems", "Applied ML (YOLO, CNN)"],
}

CONTACTS = [
    {"label": "Instagram @azraelhael", "url": "https://www.instagram.com/azraelhael"},
    {"label": "LinkedIn aimatochysia", "url": "https://www.linkedin.com/in/aimatochysia"},
    {"label": "Twitter @michaelxpetra", "url": "https://x.com/michaelxpetra"},
]

INTERESTS = [
    "Astrophysics and material science",
    "Polishing frontend design and experience",
    "More IoT projects",
    "Taking care of my plants 🌱",
]

def svg_escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def wrap_lines(text: str, width: int = 56):
    lines = []
    for para in text.splitlines():
        if not para.strip():
            lines.append("")
            continue
        lines.extend(textwrap.wrap(para.strip(), width=width))
    return lines

def chip_layout(items, max_width, start_x, start_y, h_pad=14, v_pad=8, gap=10, row_gap=12, font_size=16):
    x, y = start_x, start_y
    res = []
    for label in items:
        w = len(label) * (font_size * 0.6) + h_pad * 2
        h = font_size + v_pad * 2
        if x + w > max_width:
            x = start_x
            y += h + row_gap
        res.append((x, y, w, h, label))
        x += w + gap
    next_y = y + (font_size + v_pad * 2)
    return res, next_y

def build_svg():
    width = 1200
    pad = 40
    y = pad
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    svg = []

    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="2000" viewBox="0 0 {width} 2000">')

    svg.append(f"""
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0f0c29">
        <animate attributeName="stop-color" values="#0f0c29;#24243e;#0f0c29" dur="14s" repeatCount="indefinite"/>
      </stop>
      <stop offset="100%" stop-color="#24243e">
        <animate attributeName="stop-color" values="#24243e;#302b63;#24243e" dur="14s" repeatCount="indefinite"/>
      </stop>
    </linearGradient>

    <linearGradient id="strokeGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00eaff"/>
      <stop offset="50%" stop-color="#ff00ff"/>
      <stop offset="100%" stop-color="#00eaff"/>
    </linearGradient>

    <filter id="neon" x="-50%" y="-50%" width="200%" height="200%">
      <feDropShadow dx="0" dy="0" stdDeviation="2" flood-color="#00eaff" flood-opacity="0.85"/>
      <feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="#ff00ff" flood-opacity="0.65"/>
      <feDropShadow dx="0" dy="0" stdDeviation="10" flood-color="#00eaff" flood-opacity="0.35"/>
    </filter>

    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#00eaff" stroke-opacity="0.12" stroke-width="1"/>
    </pattern>

    <linearGradient id="scanGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="50%" stop-color="#ffffff" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>

    <style><![CDATA[
      :root {{
        --fg: #dff8ff;
        --muted: #9ad7ff;
        --cyan: #00eaff;
        --mag: #ff00ff;
        --y: #fffb00;
        --card: rgba(255,255,255,0.02);
        --card-hover: rgba(0, 234, 255, 0.08);
        font-family: "Segoe UI", system-ui, -apple-system, "Inter", Roboto, Arial, sans-serif;
      }}
      .heading {{ fill: var(--fg); letter-spacing: 1px; }}
      .subtle {{ fill: var(--muted); }}
      .card {{ fill: var(--card); stroke: url(#strokeGrad); stroke-width: 2; rx: 14; }}
      .card:hover {{ fill: var(--card-hover); }}
      .chip {{ fill: rgba(0,0,0,0.2); stroke: url(#strokeGrad); stroke-width: 1.2; rx: 10; }}
      .chip-text {{ fill: var(--fg); font-size: 16px; }}
      .section-title {{ fill: var(--fg); font-size: 26px; letter-spacing: .5px; }}
      .scan {{ animation: scan 7s linear infinite; }}
      @keyframes scan {{
        0% {{ transform: translateY(-100%); }}
        100% {{ transform: translateY(100%); }}
      }}
      .flicker {{ animation: flick 6s infinite; }}
      @keyframes flick {{
        0%,97%,100% {{ opacity: 1; }}
        98% {{ opacity: .45; }}
        99% {{ opacity: .8; }}
      }}
      a {{ cursor: pointer; text-decoration: none; }}
    ]]></style>
  </defs>
""")

    svg.append(f'<rect x="0" y="0" width="100%" height="100%" fill="url(#bg)"/>')
    svg.append(f'<rect x="0" y="0" width="100%" height="100%" fill="url(#grid)" opacity="0.35"/>')
    svg.append(f'<rect class="scan" x="0" y="0" width="100%" height="220" fill="url(#scanGrad)" style="mix-blend-mode: screen;"/>')

    svg.append(f'<rect x="{pad}" y="{y}" width="{width - 2*pad}" height="3" fill="url(#strokeGrad)"/>')
    y += 40

    svg.append(f'<text x="{width/2}" y="{y+10}" text-anchor="middle" font-size="56" class="heading flicker" filter="url(#neon)">{svg_escape(PROFILE["name"])}</text>')
    y += 52
    svg.append(f'<text x="{width/2}" y="{y+14}" text-anchor="middle" font-size="22" class="subtle">{svg_escape(PROFILE["title"])}</text>')
    y += 40

    for line in wrap_lines(PROFILE["tagline"], 86):
        svg.append(f'<text x="{pad}" y="{y}" font-size="18" class="subtle">{svg_escape(line)}</text>')
        y += 24
    for line in wrap_lines(PROFILE["open_to"], 86):
        svg.append(f'<text x="{pad}" y="{y}" font-size="18" class="subtle">{svg_escape(line)}</text>')
        y += 24

    y += 10
    svg.append(f'<rect x="{pad}" y="{y}" width="{width - 2*pad}" height="2" fill="url(#strokeGrad)" opacity="0.8"/>')
    y += 36

    svg.append(f'<text x="{pad}" y="{y}" class="section-title" filter="url(#neon)">Profile</text>')
    y += 18
    y += 16
    for p in PROFILE["profile_points"]:
        svg.append(f'<text x="{pad+8}" y="{y}" font-size="18" class="heading">• {svg_escape(p)}</text>')
        y += 26

    y += 12
    svg.append(f'<text x="{pad}" y="{y+6}" class="section-title" filter="url(#neon)">Projects</text>')
    y += 28

    card_x = pad
    card_w = width - 2 * pad
    for proj in PROJECTS:
        name = proj["name"]; url = proj["url"]; desc = proj["desc"]
        title_lines = wrap_lines(name, 42)
        desc_lines = wrap_lines(desc, 90)
        card_h = 30 + len(title_lines)*24 + len(desc_lines)*20 + 16

        svg.append(f'<a xlink:href="{svg_escape(url)}" target="_blank" rel="noopener noreferrer">')
        svg.append(f'  <rect class="card" x="{card_x}" y="{y}" width="{card_w}" height="{card_h}" />')
        ty = y + 26
        for i, tl in enumerate(title_lines):
            svg.append(f'  <text x="{card_x+16}" y="{ty}" font-size="22" class="heading">{svg_escape(tl)}</text>')
            ty += 24
        ty += 2
        for dl in desc_lines:
            svg.append(f'  <text x="{card_x+16}" y="{ty}" font-size="16" class="subtle">{svg_escape(dl)}</text>')
            ty += 20
        svg.append(f'</a>')
        y += card_h + 12

    y += 8
    svg.append(f'<rect x="{pad}" y="{y}" width="{width - 2*pad}" height="2" fill="url(#strokeGrad)" opacity="0.8"/>')
    y += 36
    svg.append(f'<text x="{pad}" y="{y}" class="section-title" filter="url(#neon)">Skills</text>')
    y += 26

    max_w = width - pad
    for group, items in SKILLS.items():
        svg.append(f'<text x="{pad}" y="{y}" font-size="18" class="heading">{svg_escape(group)}:</text>')
        y += 10
        chips, next_y = chip_layout(items, max_w, pad, y)
        for x, cy, w, h, label in chips:
            svg.append(f'<rect class="chip" x="{x}" y="{cy}" width="{w}" height="{h}"/>')
            svg.append(f'<text class="chip-text" x="{x + 12}" y="{cy + h/2 + 6}">{svg_escape(label)}</text>')
        y = next_y + 20

    svg.append(f'<rect x="{pad}" y="{y}" width="{width - 2*pad}" height="2" fill="url(#strokeGrad)" opacity="0.8"/>')
    y += 36
    svg.append(f'<text x="{pad}" y="{y}" class="section-title" filter="url(#neon)">Contact</text>')
    y += 28
    for c in CONTACTS:
        svg.append(f'<a xlink:href="{svg_escape(c["url"])}" target="_blank" rel="noopener noreferrer">')
        svg.append(f'  <text x="{pad+8}" y="{y}" font-size="18" class="heading">⟶ {svg_escape(c["label"])}</text>')
        svg.append(f'</a>')
        y += 26

    y += 8
    svg.append(f'<rect x="{pad}" y="{y}" width="{width - 2*pad}" height="2" fill="url(#strokeGrad)" opacity="0.8"/>')
    y += 36
    svg.append(f'<text x="{pad}" y="{y}" class="section-title" filter="url(#neon)">Interests</text>')
    y += 26
    for i in INTERESTS:
        svg.append(f'<text x="{pad+8}" y="{y}" font-size="18" class="heading">• {svg_escape(i)}</text>')
        y += 26

    y += 18
    q_lines = wrap_lines(PROFILE["quote"], 78)
    for q in q_lines:
        svg.append(f'<text x="{pad}" y="{y}" font-size="16" class="subtle"> {svg_escape(q)}</text>')
        y += 20
    y += 8
    svg.append(f'<text x="{width - pad}" y="{y}" text-anchor="end" font-size="12" class="subtle">Generated {svg_escape(now)}</text>')

    y += 18
    svg.append(f'<rect x="{pad}" y="{y}" width="{width - 2*pad}" height="3" fill="url(#strokeGrad)"/>')

    total_h = int(y + 60)
    svg.append(f'</svg>')
    svg_str = "\n".join(svg).replace(f'height="2000"', f'height="{total_h}"').replace(f'viewBox="0 0 {width} 2000"', f'viewBox="0 0 {width} {total_h}"')
    return svg_str

def write_outputs():
    root = Path(__file__).resolve().parents[1]
    assets = root / "assets"
    assets.mkdir(parents=True, exist_ok=True)

    svg_path = assets / "profile.svg"
    svg_path.write_text(build_svg(), encoding="utf-8")

    readme_path = root / "README.md"
    readme_md = """<p align="center">
  <img src="assets/profile.svg" alt="Petra Michael — Neon Cyberpunk Profile" width="100%" />
</p>

<p align="center">
  <a href="assets/profile.svg">View the animated profile SVG</a>
</p>
"""
    readme_path.write_text(readme_md, encoding="utf-8")

if __name__ == "__main__":
    write_outputs()
    print("Generated assets/profile.svg and updated README.md")
