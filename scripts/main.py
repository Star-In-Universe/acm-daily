#!/usr/bin/env python3
"""CACM 每日推送主流程：抓取 → 翻译 → 摘要/导图 → 渲染 → 邮件。"""
from __future__ import annotations

import argparse
import json
import os
import sys
import traceback

import ai
import fetch
import mailer
import render

ROOT = fetch.ROOT


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", type=int, default=None, help="强制处理指定文章 id")
    ap.add_argument("--reuse", action="store_true", help="复用已有的 translations/meta（调试用）")
    ap.add_argument("--dry-run", metavar="EML", help="只生成 .eml 不发信")
    ap.add_argument("--no-mail", action="store_true", help="不发邮件（仅生成文件）")
    args = ap.parse_args()

    force = args.force or int(os.environ.get("FORCE_ID") or 0) or None
    section = int(os.environ.get("CACM_SECTION", "72") or 0) or None
    result = fetch.check(force, section)
    print("FETCH:", json.dumps(result, ensure_ascii=False))

    if result["status"] == "no_new":
        print(f"NO_NEW ({result.get('reason')})：{result['newest']['title']}")
        return 0
    if result["status"] != "new":
        print("ERROR:", result.get("message"))
        return 1

    adir = os.path.join(ROOT, result["dir"])
    with open(os.path.join(adir, "blocks.json"), encoding="utf-8") as fh:
        blocks = json.load(fh)

    trans_path = os.path.join(adir, "translations.json")
    meta_path = os.path.join(adir, "meta.json")

    if args.reuse and os.path.exists(trans_path) and os.path.exists(meta_path):
        with open(trans_path, encoding="utf-8") as fh:
            translations = json.load(fh)
        with open(meta_path, encoding="utf-8") as fh:
            meta = json.load(fh)
        print("REUSE: 使用已有译文与摘要")
    else:
        print(f"TRANSLATE: {result['blocks']} 段 / {result['words']} 词 …")
        translations = ai.translate_blocks(blocks["blocks"], blocks["title"])
        print(f"TRANSLATE: 完成 {len(translations)} 段")
        print("META: 生成摘要与思维导图结构 …")
        meta = ai.build_meta(blocks["title"], blocks.get("lede", ""), blocks["blocks"])
        with open(trans_path, "w", encoding="utf-8") as fh:
            json.dump(translations, fh, ensure_ascii=False, indent=1)
        with open(meta_path, "w", encoding="utf-8") as fh:
            json.dump(meta, fh, ensure_ascii=False, indent=1)

    out = render.render_article(adir, blocks, translations, meta)
    print("RENDER:", json.dumps(out, ensure_ascii=False))

    if not args.no_mail:
        sent = mailer.send_digest(
            meta, blocks, len(translations), len(blocks["blocks"]),
            out["markdown"], out["mindmap"], dry_run=args.dry_run,
        )
        print("MAIL:", json.dumps(sent, ensure_ascii=False))

    if not args.dry_run:
        fetch.mark_done(result["id"], {
            "title": result["title"],
            "date": result["date"],
            "link": result["link"],
            "dir": result["dir"],
        })
        print(f"DONE: 已登记 {result['id']}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:  # noqa: BLE001
        traceback.print_exc()
        sys.exit(1)
