#!/usr/bin/env python3
"""CACM 每日推送主流程：抓取 → 翻译 → 摘要/导图 → 渲染 → 汇总成一封邮件。"""
from __future__ import annotations

import argparse
import json
import os
import sys
import traceback
from datetime import datetime, timedelta, timezone

import ai
import fetch
import mailer
import render

ROOT = fetch.ROOT
CST = timezone(timedelta(hours=8))


def parse_sections(env_name: str, default: str) -> list[int]:
    raw = os.environ.get(env_name, default) or ""
    return [int(x.strip()) for x in raw.split(",") if x.strip()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", type=int, default=None, help="强制处理指定文章 id")
    ap.add_argument("--reuse", action="store_true", help="复用已有翻译/摘要（调试用）")
    ap.add_argument("--dry-run", metavar="EML", help="只生成 .eml 不发信")
    ap.add_argument("--no-mail", action="store_true", help="不生成邮件")
    args = ap.parse_args()

    force = args.force or int(os.environ.get("FORCE_ID") or 0) or None
    post_sections = parse_sections("CACM_POSTS_SECTIONS", "72")
    dl_sections = parse_sections("CACM_DL_SECTIONS", "11")

    result = fetch.check_new(post_sections, dl_sections, force_id=force)
    print("FETCH:", json.dumps(result, ensure_ascii=False))

    if result["status"] == "no_new":
        print(f"NO_NEW ({result.get('reason')})：{result['newest']['title']}")
        return 0
    if result["status"] != "new":
        print("ERROR:", result.get("message"))
        return 1

    articles: list[dict] = []
    for item in result["items"]:
        info = fetch.download(item)
        adir = os.path.join(ROOT, info["dir"])
        with open(os.path.join(adir, "blocks.json"), encoding="utf-8") as fh:
            blocks = json.load(fh)

        trans_path = os.path.join(adir, "translations.json")
        meta_path = os.path.join(adir, "meta.json")

        if args.reuse and os.path.exists(trans_path) and os.path.exists(meta_path):
            with open(trans_path, encoding="utf-8") as fh:
                translations = json.load(fh)
            with open(meta_path, encoding="utf-8") as fh:
                meta = json.load(fh)
            print(f"REUSE: {info['title'][:50]}")
        else:
            print(f"TRANSLATE: {info['title'][:50]} / {info['blocks']} 段 {info['words']} 词 …")
            translations = ai.translate_blocks(blocks["blocks"], blocks["title"])
            meta = ai.build_meta(blocks["title"], blocks.get("lede", ""), blocks["blocks"])
            with open(trans_path, "w", encoding="utf-8") as fh:
                json.dump(translations, fh, ensure_ascii=False, indent=1)
            with open(meta_path, "w", encoding="utf-8") as fh:
                json.dump(meta, fh, ensure_ascii=False, indent=1)

        out = render.render_article(adir, blocks, translations, meta)
        print("RENDER:", json.dumps(out, ensure_ascii=False))

        articles.append({
            "id": info["id"],
            "meta": meta,
            "blocks": blocks,
            "md": out["markdown"],
            "png": out["mindmap"],
            "filename": os.path.basename(info["dir"]) + ".md",
            "translated": len(translations),
            "total": len(blocks["blocks"]),
            "info": info,
        })

    date_label = datetime.now(CST).strftime("%Y-%m-%d")
    if not args.no_mail:
        sent = mailer.send_digest(articles, date_label, dry_run=args.dry_run)
        print("MAIL:", json.dumps(sent, ensure_ascii=False))

    if not args.dry_run:
        for item in result["items"]:
            fetch.mark_done(item["id"], {
                "title": item["title"], "date": item["date"],
                "link": item["link"], "section": item["section"],
            })
        print(f"DONE: 已登记 {len(result['items'])} 篇")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:  # noqa: BLE001
        traceback.print_exc()
        sys.exit(1)
