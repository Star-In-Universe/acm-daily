#!/usr/bin/env python3
"""抓取 CACM 文章（GitHub Actions 版）。

两个内容源：
  posts            —— 网站文章（News 72 / BLOG@CACM 164）
  digital-library  —— 杂志栏目（Opinion 11 / Research 23 / Practice 40 …）

用法见 main.py。
"""
from __future__ import annotations

import html
import json
import os
import re
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser

POSTS_API = "https://cacm.acm.org/wp-json/wp/v2/posts"
DL_API = "https://cacm.acm.org/wp-json/wp/v2/digital-library"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_PATH = os.path.join(ROOT, "state.json")
ART_DIR = os.path.join(ROOT, "articles")

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0 Safari/537.36"
)
CST = timezone(timedelta(hours=8))
SITE_TZ = timezone(timedelta(hours=-4))  # 美东（EDT）

FRESH_DAYS = 7           # 超过这么多天的不再补推
MAX_PER_RUN = 4          # 一次最多处理几篇
SKIP_TITLES = ("call for papers", "call for nominations", "call for participation")

SECTION_NAMES = {
    11: "Opinion",
    23: "Research",
    40: "Practice",
    72: "News",
    164: "Blog@CACM",
    19458: "Research Highlights",
    20060: "Upstart Puzzles",
    20067: "Vardi's Insights",
    20083: "Kode Vicious",
    20251: "Future Tense",
    20543: "Cerf's Up",
    20553: "President's Letter",
}

BLOCK_TAGS = {"p", "h2", "h3", "h4", "li", "blockquote"}
SKIP_TAGS = {"script", "style", "figure", "figcaption", "sup", "nav", "aside"}
TAIL_RE = re.compile(r"^(references?|footnotes?|further reading|related reading|notes)$", re.I)


# ---------------------------------------------------------------- HTTP
def get_json(url: str, tries: int = 3) -> object:
    last: Exception | None = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": UA, "Accept": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"请求失败：{url} -> {last}")


# ---------------------------------------------------------------- 正文抽取
class BodyParser(HTMLParser):
    """把正文拆成段落块；遇到新块级标签即隐式结束上一块。"""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[tuple[str, str]] = []
        self._buf: list[str] = []
        self._kind: str | None = None
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in SKIP_TAGS:
            self._skip += 1
            return
        if tag == "br":
            self._buf.append(" ")
            return
        if tag in BLOCK_TAGS:
            # 杂志正文里 <p> 常不闭合：遇到新块就隐式结束上一块
            if self._kind is not None:
                self._flush()
            self._kind = tag
            self._buf = []

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in SKIP_TAGS:
            self._skip = max(0, self._skip - 1)
            return
        if tag in BLOCK_TAGS and self._kind == tag:
            self._flush()
            self._kind = None
            self._buf = []

    def handle_data(self, data):
        if self._kind and self._skip == 0:
            self._buf.append(data)

    def _flush(self):
        text = html.unescape("".join(self._buf))
        text = re.sub(r"[\u00a0\u200b\ufeff]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            kind = "h" if self._kind and self._kind.startswith("h") else self._kind
            self.blocks.append((kind or "p", text))

    def close(self):
        super().close()
        if self._kind:
            self._flush()


def extract_blocks(rendered: str) -> tuple[list[dict], list[str]]:
    parser = BodyParser()
    parser.feed(rendered or "")
    parser.close()

    body: list[dict] = []
    tail: list[str] = []
    in_tail = False
    for kind, text in parser.blocks:
        if (not in_tail and TAIL_RE.match(text.strip(" .:"))
                and (kind == "h" or len(text) <= 30)):
            in_tail = True
        if in_tail:
            tail.append(f"## {text}" if kind == "h" else text)
            continue
        if len(text) < 2:
            continue
        body.append({"type": kind, "en": text})

    dedup: list[dict] = []
    for b in body:
        if dedup and dedup[-1]["en"].lower() == b["en"].lower():
            continue
        dedup.append(b)
    return dedup, tail


# ---------------------------------------------------------------- 工具
def load_state() -> dict:
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, encoding="utf-8") as fh:
            return json.load(fh)
    return {"processed": []}


def save_state(state: dict) -> None:
    with open(STATE_PATH, "w", encoding="utf-8") as fh:
        json.dump(state, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def pretty_title(post: dict) -> str:
    title = post.get("title") or {}
    raw = title.get("rendered") if isinstance(title, dict) else str(title)
    return html.unescape(re.sub(r"<[^>]+>", "", raw or "")).strip()


def slug_from_link(link: str) -> str:
    path = urllib.parse.urlparse(link).path.rstrip("/")
    return path.rsplit("/", 1)[-1] or "article"


def section_label(post: dict) -> str:
    secs = post.get("section") or []
    names = [SECTION_NAMES[s] for s in secs if s in SECTION_NAMES]
    return " / ".join(names[:2])


def is_skipped(post: dict) -> bool:
    title = pretty_title(post).lower()
    return any(title.startswith(prefix) for prefix in SKIP_TITLES)


def post_age_days(post: dict) -> float:
    published = datetime.fromisoformat(post["date"]).replace(tzinfo=SITE_TZ)
    return (datetime.now(SITE_TZ) - published).total_seconds() / 86400


def list_source(api: str, sections: list[int], per_page: int = 10) -> list[dict]:
    url = f"{api}?per_page={per_page}&_fields=id,date,link,title,section,excerpt"
    if sections:
        url += "&section=" + ",".join(str(s) for s in sections)
    data = get_json(url)
    assert isinstance(data, list)
    source = "dl" if api == DL_API else "posts"
    for item in data:
        item["source"] = source
    return data


# ---------------------------------------------------------------- 主流程
def check_new(post_sections: list[int], dl_sections: list[int],
              limit: int = MAX_PER_RUN, days: int = FRESH_DAYS,
              force_id: int | None = None) -> dict:
    state = load_state()
    state["last_check"] = datetime.now(CST).isoformat(timespec="seconds")
    processed = {int(p["id"]) for p in state.get("processed", [])}

    items: list[dict] = []
    if post_sections:
        items += list_source(POSTS_API, post_sections)
    if dl_sections:
        items += list_source(DL_API, dl_sections)
    items = [p for p in items if not is_skipped(p)]
    items.sort(key=lambda p: p["date"], reverse=True)
    save_state(state)

    if not items:
        return {"status": "error", "message": "接口返回空列表"}

    if force_id is not None:
        picked = [p for p in items if int(p["id"]) == int(force_id)]
        if not picked:
            picked = [{"id": force_id, "date": "1970-01-01T00:00:00",
                       "link": "", "source": "dl", "title": {"rendered": ""},
                       "section": []}]
        return {"status": "new", "items": [
            {"id": p["id"], "date": p["date"], "title": pretty_title(p),
             "link": p.get("link", ""), "source": p["source"],
             "section": section_label(p)} for p in picked[:limit]
        ]}

    picked = [
        p for p in items
        if int(p["id"]) not in processed and post_age_days(p) <= days
    ][:limit]

    if not picked:
        newest = items[0]
        return {
            "status": "no_new",
            "reason": "already_pushed" if int(newest["id"]) in processed else "stale",
            "newest": {
                "id": newest["id"],
                "title": pretty_title(newest),
                "date": newest["date"],
                "age_days": round(post_age_days(newest), 1),
            },
            "checked": [{"id": p["id"], "title": pretty_title(p),
                         "date": p["date"], "section": section_label(p)}
                        for p in items[:5]],
        }

    return {"status": "new", "items": [
        {"id": p["id"], "date": p["date"], "title": pretty_title(p),
         "link": p["link"], "source": p["source"], "section": section_label(p)}
        for p in picked
    ]}


def download(item: dict) -> dict:
    """下载一篇文章并落盘，返回元信息。"""
    apis = ([DL_API, POSTS_API] if item.get("source") == "dl"
            else [POSTS_API, DL_API])
    post = None
    last: Exception | None = None
    for api in apis:
        try:
            post = get_json(f"{api}/{item['id']}", tries=1)
            break
        except Exception as exc:  # noqa: BLE001
            last = exc
    if post is None:
        raise RuntimeError(f"取文章 {item['id']} 失败：{last}")
    assert isinstance(post, dict)

    siteslug = slug_from_link(post["link"])
    folder = f"{post['date'][:10]}-{siteslug}"
    outdir = os.path.join(ART_DIR, folder)
    os.makedirs(outdir, exist_ok=True)

    body, tail = extract_blocks(post["content"]["rendered"])
    lede = ""
    meta = post.get("meta") or {}
    if isinstance(meta.get("lede"), str):
        lede = re.sub(r"<[^>]+>", "", html.unescape(meta["lede"])).strip()

    with open(os.path.join(outdir, "raw.json"), "w", encoding="utf-8") as fh:
        json.dump(post, fh, ensure_ascii=False, indent=1)
    with open(os.path.join(outdir, "blocks.json"), "w", encoding="utf-8") as fh:
        json.dump({"title": pretty_title(post), "lede": lede,
                   "blocks": body, "tail": tail}, fh, ensure_ascii=False, indent=1)

    lines = []
    for i, blk in enumerate(body, 1):
        tag = "H" if blk["type"] == "h" else ("L" if blk["type"] == "li" else "P")
        lines.append(f"[{i}] ({tag}) {blk['en']}")
    with open(os.path.join(outdir, "article.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    return {
        "id": post["id"],
        "title": pretty_title(post),
        "date": post["date"],
        "link": post["link"],
        "section": section_label(post),
        "authors": post.get("authors") or "",
        "blocks": len(body),
        "words": sum(len(re.findall(r"[A-Za-z0-9'’-]+", b["en"])) for b in body),
        "dir": os.path.relpath(outdir, ROOT),
        "lede": lede,
        "source": item.get("source", "posts"),
    }


def mark_done(post_id: int, entry: dict | None = None) -> dict:
    state = load_state()
    if any(int(p["id"]) == post_id for p in state.get("processed", [])):
        return {"status": "already"}
    item = {"id": post_id, "pushed_at": datetime.now(CST).isoformat(timespec="seconds")}
    item.update(entry or {})
    state.setdefault("processed", []).append(item)
    save_state(state)
    return {"status": "marked", **item}
