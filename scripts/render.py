#!/usr/bin/env python3
"""渲染中文思维导图 PNG 与中英对照 Markdown（Linux/Windows 通用）。"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone

from PIL import Image, ImageDraw, ImageFont

CST = timezone(timedelta(hours=8))
SITE_TZ = timezone(timedelta(hours=-4))

PALETTE = [
    ("#DCE9FB", "#2F6FD0"),
    ("#DFF2E6", "#2E8B57"),
    ("#FCEBD7", "#C46A12"),
    ("#EDE4FA", "#6A45B5"),
    ("#DDF0F4", "#177E8C"),
    ("#FADFE3", "#C0392B"),
    ("#EAF1DB", "#5C7A20"),
    ("#E4E8F2", "#45507A"),
]

# (路径, ttc 内索引, 是否粗体)
FONT_CANDIDATES = [
    (os.environ.get("CJK_FONT_REG", ""), 0, False),
    (os.environ.get("CJK_FONT_BOLD", ""), 0, True),
    (r"C:\Windows\Fonts\msyh.ttc", 0, False),
    (r"C:\Windows\Fonts\msyhbd.ttc", 0, True),
    ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 2, False),
    ("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 2, True),
    ("/usr/share/fonts/opentype/noto/NotoSansCJKsc-Regular.otf", 0, False),
    ("/usr/share/fonts/opentype/noto/NotoSansCJKsc-Bold.otf", 0, True),
    ("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", 0, False),
    ("/usr/share/fonts/truetype/wqy/wqy-microhei.ttc", 0, False),
]

_FONTS: dict[str, tuple[str, int]] = {}


def _resolve() -> None:
    if _FONTS:
        return
    for path, index, bold in FONT_CANDIDATES:
        if not path or not os.path.exists(path):
            continue
        try:
            f = ImageFont.truetype(path, 22, index=index)
            if f.getbbox("中文")[2] > 0:
                _FONTS["bold" if bold else "reg"] = (path, index)
        except Exception:  # noqa: BLE001
            continue
    if "reg" not in _FONTS:
        raise RuntimeError("找不到可用的中文字体，请安装 fonts-noto-cjk 或设置 CJK_FONT_REG")
    _FONTS.setdefault("bold", _FONTS["reg"])


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    _resolve()
    path, index = _FONTS["bold" if bold else "reg"]
    return ImageFont.truetype(path, size, index=index)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, max_w: int) -> list[str]:
    out: list[str] = []
    for para in str(text).split("\n"):
        para = para.strip()
        if not para:
            continue
        tokens = re.findall(r"[A-Za-z0-9][A-Za-z0-9@:/._+'’\-]*|\s+|.", para)
        cur = ""
        for tok in tokens:
            if tok.isspace():
                if cur and not cur.endswith(" "):
                    cur += " "
                continue
            cand = cur + tok
            if draw.textlength(cand, font=fnt) <= max_w or not cur.strip():
                cur = cand
            else:
                out.append(cur.rstrip())
                cur = tok
        if cur.strip():
            out.append(cur.rstrip())
    return out or [""]


def box_size(draw, lines, fnt, padx, pady, lh=1.45):
    w = max((draw.textlength(t, font=fnt) for t in lines), default=0)
    line_h = int(fnt.size * lh)
    return int(w) + padx * 2, line_h * len(lines) + pady * 2, line_h, padx, pady


def draw_box(img, draw, box, lines, fnt, fill, stroke, text_color="#1F2430",
             radius=14, width=3, padx=18, pady=12):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill,
                           outline=stroke, width=width)
    _, _, line_h, _, _ = box_size(draw, lines, fnt, padx, pady)
    ty = y0 + pady
    for ln in lines:
        draw.text((x0 + padx, ty), ln, font=fnt, fill=text_color)
        ty += line_h


def curve(draw, p0, p1, color, width=3):
    x0, y0 = p0
    x1, y1 = p1
    mid = (x0 + x1) / 2
    pts = []
    for i in range(41):
        t = i / 40
        x = (1 - t) ** 3 * x0 + 3 * (1 - t) ** 2 * t * mid + 3 * (1 - t) * t ** 2 * mid + t ** 3 * x1
        y = (1 - t) ** 3 * y0 + 3 * (1 - t) ** 2 * t * y0 + 3 * (1 - t) * t ** 2 * y1 + t ** 3 * y1
        pts.append((x, y))
    draw.line(pts, fill=color, width=width, joint="curve")


def render_mindmap(tree: dict, out_path: str, footer: str = "", scale: int = 2):
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    f_root, f_branch, f_child = font(30, True), font(21, True), font(18)

    root_lines = wrap(probe, tree.get("title", ""), f_root, 320)
    rw, rh, _, _, _ = box_size(probe, root_lines, f_root, 22, 16)

    slots = []
    for br in tree.get("branches", []) or []:
        b_lines = wrap(probe, br.get("title", ""), f_branch, 250)
        bw, bh, _, _, _ = box_size(probe, b_lines, f_branch, 16, 11)
        kids = []
        for kid in br.get("children", []) or []:
            k_lines = wrap(probe, kid, f_child, 320)
            kw, kh, _, _, _ = box_size(probe, k_lines, f_child, 14, 10)
            kids.append((k_lines, kw, kh))
        kids_h = sum(k[2] for k in kids) + 12 * max(0, len(kids) - 1)
        slots.append({"lines": b_lines, "w": bw, "h": bh, "kids": kids,
                      "kids_h": kids_h, "slot_h": max(bh, kids_h)})

    pad = 54
    gap_y = 34
    total_h = sum(s["slot_h"] for s in slots) + gap_y * max(0, len(slots) - 1)
    total_h = max(total_h, rh) + pad * 2 + (26 if footer else 0)

    x_root = pad
    x_branch = x_root + rw + 64
    max_bw = max((s["w"] for s in slots), default=0)
    x_child = x_branch + max_bw + 42
    max_cw = max((k[1] for s in slots for k in s["kids"]), default=0)
    total_w = x_child + max_cw + pad

    img = Image.new("RGB", (int(total_w) * scale, int(total_h) * scale), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    draw.fontmode = "L"

    def S(v):
        return v * scale

    root_top = (total_h - rh - (26 if footer else 0)) / 2
    draw_box(img, draw, (S(x_root), S(root_top), S(x_root + rw), S(root_top + rh)),
             root_lines, font(30 * scale, True), "#22303F", "#22303F",
             text_color="#FFFFFF", radius=16 * scale, width=2 * scale,
             padx=22 * scale, pady=16 * scale)

    y = pad
    for idx, s in enumerate(slots):
        fill, stroke = PALETTE[idx % len(PALETTE)]
        slot_top = y
        b_top = slot_top + (s["slot_h"] - s["h"]) / 2
        k_top = slot_top + (s["slot_h"] - s["kids_h"]) / 2

        draw_box(img, draw, (S(x_branch), S(b_top), S(x_branch + s["w"]), S(b_top + s["h"])),
                 s["lines"], font(21 * scale, True), fill, stroke,
                 radius=13 * scale, width=2 * scale, padx=16 * scale, pady=11 * scale)
        curve(draw, (S(x_root + rw), S(root_top + rh / 2)),
              (S(x_branch), S(b_top + s["h"] / 2)), stroke, width=3 * scale)

        ky = k_top
        for k_lines, kw, kh in s["kids"]:
            draw_box(img, draw, (S(x_child), S(ky), S(x_child + kw), S(ky + kh)),
                     k_lines, font(18 * scale), "#FFFFFF", stroke,
                     radius=11 * scale, width=2 * scale, padx=14 * scale, pady=10 * scale)
            curve(draw, (S(x_branch + s["w"]), S(b_top + s["h"] / 2)),
                  (S(x_child), S(ky + kh / 2)), stroke, width=2 * scale)
            ky += kh + 12
        y += s["slot_h"] + gap_y

    if footer:
        f = font(13 * scale)
        tw = draw.textlength(footer, font=f)
        draw.text((S(total_w) - tw - 18 * scale, S(total_h) - 24 * scale),
                  footer, font=f, fill="#9AA3AF")

    img = img.resize((int(total_w), int(total_h)), Image.LANCZOS)
    # 调色板量化：文件更小，邮件附件更轻
    img.convert("P", palette=Image.ADAPTIVE, colors=256).save(out_path, "PNG", optimize=True)
    return int(total_w), int(total_h)


def build_markdown(blocks: dict, trans: dict, meta: dict) -> str:
    title, lede = blocks["title"], blocks.get("lede", "")
    body, tail = blocks["blocks"], blocks.get("tail", [])
    title_zh = meta.get("title_zh") or ""
    skip = {int(x) for x in meta.get("skip", [])}

    out: list[str] = []
    out.append(f"# {title}")
    if title_zh:
        out.append(f"\n## {title_zh}")
    out.append("")
    out.append(
        f"**来源**：Communications of the ACM（{meta.get('section','')}）　|　"
        f"**发布**：{meta.get('date_site','')}（美东）　|　"
        f"**北京时间**：{meta.get('date_cst','')}　|　"
        f"**作者**：{meta.get('authors','')}"
    )
    out.append(f"\n[原文链接]({meta.get('link','')})　·　生成于 {meta.get('generated_at','')}")
    out.append("\n![思维导图](mindmap.png)\n")
    out.append("---\n")

    out.append("## 一、摘要\n")
    lede_zh = (meta.get("lede_zh") or "").strip()
    if lede_zh:
        out.append(f"> {lede_zh}\n")
    elif lede:
        out.append(f"> {lede.strip()}\n")
    out.append(meta.get("summary", "").strip() + "\n")

    points = meta.get("points") or []
    if points:
        out.append("## 二、核心要点\n")
        for i, p in enumerate(points, 1):
            out.append(f"{i}. {p}")
        out.append("")

    terms = meta.get("terms") or []
    if terms:
        out.append("## 三、关键词对照\n")
        out.append("| English | 中文 |")
        out.append("| --- | --- |")
        for t in terms:
            out.append(f"| {t.get('en','')} | {t.get('zh','')} |")
        out.append("")

    out.append("## 四、中英对照全文\n")
    for i, blk in enumerate(body, 1):
        zh = "" if i in skip else (trans.get(str(i)) or "").strip()
        en = blk["en"].strip()
        if blk["type"] == "h":
            out.append(f"### {en}")
            if zh:
                out.append(f"*{zh}*\n")
            continue
        if blk["type"] == "li":
            out.append(f"- {en}")
            if zh:
                out.append(f"\n  > {zh}\n")
            continue
        out.append(en)
        if zh:
            out.append(f"\n> {zh}\n")
        else:
            out.append("")

    if tail:
        out.append("## 附录：参考与脚注（原文）\n")
        for t in tail:
            out.append(t)
            out.append("")

    out.append("---")
    out.append("*英文原文版权归 Communications of the ACM 及作者所有；中文译文由 AI 辅助生成，仅供学习参考。*")
    return "\n".join(out)


def render_article(adir: str, blocks: dict, trans: dict, meta: dict) -> dict:
    # 补齐元信息
    raw_path = os.path.join(adir, "raw.json")
    if os.path.exists(raw_path):
        with open(raw_path, encoding="utf-8") as fh:
            raw = json.load(fh)
        secs = raw.get("section") or []
        meta.setdefault("link", raw.get("link", ""))
        meta.setdefault("authors", raw.get("authors", ""))
        meta.setdefault("section", {72: "News", 164: "Blog@CACM"}.get(secs[0] if secs else 0, ""))
        dt = datetime.fromisoformat(raw["date"]).replace(tzinfo=SITE_TZ)
        meta.setdefault("date_site", raw["date"][:16].replace("T", " "))
        meta.setdefault("date_cst", dt.astimezone(CST).strftime("%Y-%m-%d %H:%M"))
    meta.setdefault("generated_at", datetime.now(CST).strftime("%Y-%m-%d %H:%M"))

    footer = f"CACM · {meta.get('date_cst', '')[:10]} · 自动生成"
    png = os.path.join(adir, "mindmap.png")
    w, h = render_mindmap(meta["mindmap"], png, footer=footer)

    md = build_markdown(blocks, trans, meta)
    md_path = os.path.join(adir, "article.md")
    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write(md)
    return {"mindmap": png, "markdown": md_path, "size": [w, h], "chars": len(md)}


if __name__ == "__main__":
    adir = sys.argv[1]
    with open(os.path.join(adir, "blocks.json"), encoding="utf-8") as fh:
        blocks = json.load(fh)
    with open(os.path.join(adir, "meta.json"), encoding="utf-8") as fh:
        meta = json.load(fh)
    with open(os.path.join(adir, "translations.json"), encoding="utf-8") as fh:
        trans = json.load(fh)
    print(json.dumps(render_article(adir, blocks, trans, meta), ensure_ascii=False, indent=2))
