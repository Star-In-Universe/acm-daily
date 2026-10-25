#!/usr/bin/env python3
"""把每日内容组装成 HTML 邮件并通过 SMTP 发出（支持 --dry-run 保存 .eml）。"""
from __future__ import annotations

import html as html_mod
import json
import os
import smtplib
import ssl
from datetime import datetime
from email.message import EmailMessage
from email.utils import formataddr, formatdate


def _esc(text: str) -> str:
    return html_mod.escape(str(text), quote=False)


def build_html(meta: dict, blocks: dict, translated: int, total: int) -> str:
    title_zh = _esc(meta.get("title_zh", ""))
    title_en = _esc(blocks.get("title", ""))
    lede = _esc(meta.get("lede_zh", "") or "")
    summary = _esc(meta.get("summary", "")).replace("\n", "<br>")
    points = "".join(
        f'<li style="margin:6px 0;line-height:1.7">{_esc(p)}</li>' for p in meta.get("points", [])
    )
    terms = "".join(
        f'<span style="display:inline-block;background:#EEF2F8;border-radius:6px;'
        f'padding:3px 8px;margin:3px 4px 3px 0;font-size:13px;color:#34495E">'
        f'{_esc(t.get("en",""))} · {_esc(t.get("zh",""))}</span>'
        for t in meta.get("terms", [])
    )

    return f"""<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title_zh}</title></head>
<body style="margin:0;padding:0;background:#F4F6FA;font-family:-apple-system,'PingFang SC','Microsoft YaHei',Arial,sans-serif">
<div style="max-width:680px;margin:0 auto;padding:20px 16px 32px">

  <div style="font-size:12px;color:#8A93A0;letter-spacing:1px;margin-bottom:10px">
    CACM 每日推送 · {_esc(meta.get("date_cst",""))} · {_esc(meta.get("section","News"))}
  </div>

  <h1 style="font-size:22px;line-height:1.45;margin:0 0 6px;color:#1F2937">{title_zh}</h1>
  <div style="font-size:13px;color:#7A8494;margin-bottom:16px">{title_en}</div>

  {f'<div style="font-size:15px;color:#4B5563;line-height:1.7;margin-bottom:18px">{lede}</div>' if lede else ''}

  <div style="background:#fff;border-radius:12px;padding:18px 18px 14px;margin-bottom:16px;
              box-shadow:0 1px 3px rgba(16,24,40,.06)">
    <div style="font-size:13px;color:#2F6FD0;font-weight:600;margin-bottom:8px">摘要</div>
    <div style="font-size:15px;line-height:1.85;color:#374151">{summary}</div>
  </div>

  <div style="background:#fff;border-radius:12px;padding:18px 18px 14px;margin-bottom:16px;
              box-shadow:0 1px 3px rgba(16,24,40,.06)">
    <div style="font-size:13px;color:#2F6FD0;font-weight:600;margin-bottom:8px">核心要点</div>
    <ol style="margin:0;padding-left:20px;font-size:14.5px;color:#374151">{points}</ol>
  </div>

  {f'<div style="margin-bottom:18px">{terms}</div>' if terms else ''}

  <div style="background:#fff;border-radius:12px;padding:10px;margin-bottom:16px;
              box-shadow:0 1px 3px rgba(16,24,40,.06)">
    <img src="cid:mindmap@cacm" alt="思维导图" style="width:100%;height:auto;display:block;border-radius:8px">
    <div style="font-size:12px;color:#98A2B3;text-align:center;padding:8px 0 2px">中文思维导图</div>
  </div>

  <div style="font-size:14px;line-height:1.8;color:#374151;margin-bottom:18px">
    中英对照全文（共 {translated}/{total} 段）见附件 <b>article.md</b>；
    上方思维导图可长按保存原图。<br>
    原文：<a href="{_esc(meta.get('link',''))}" style="color:#2F6FD0">{_esc(meta.get('link',''))}</a>
  </div>

  <div style="font-size:12px;color:#98A2B3;line-height:1.7;border-top:1px solid #E5E9F0;padding-top:12px">
    英文原文版权归 Communications of the ACM 及作者所有；中文译文由 AI 辅助生成，仅供学习参考。<br>
    本邮件由 GitHub Actions 定时生成 · {datetime.now().strftime('%Y-%m-%d %H:%M')}
  </div>
</div>
</body></html>"""


def build_message(meta: dict, blocks: dict, translated: int, total: int,
                  md_path: str, png_path: str, mail_to: list[str], mail_from: str) -> EmailMessage:
    subject = f"[CACM] {meta.get('date_cst','')[:10]} · {meta.get('title_zh','')}"
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr(("CACM 每日推送", mail_from))
    msg["To"] = ", ".join(mail_to)
    msg["Date"] = formatdate(localtime=True)

    text = [
        meta.get("title_zh", ""),
        blocks.get("title", ""),
        "",
        meta.get("summary", ""),
        "",
        "核心要点：",
    ]
    text += [f"{i}. {p}" for i, p in enumerate(meta.get("points", []), 1)]
    text += ["", f"原文：{meta.get('link','')}", "全文见附件 article.md / mindmap.png"]
    msg.set_content("\n".join(text))

    msg.add_alternative(build_html(meta, blocks, translated, total), subtype="html")
    html_part = msg.get_payload()[1]
    with open(png_path, "rb") as fh:
        html_part.add_related(fh.read(), maintype="image", subtype="png", cid="mindmap@cacm")

    with open(md_path, "rb") as fh:
        msg.add_attachment(fh.read(), maintype="text", subtype="markdown",
                           filename="article.md")
    return msg


def send(msg: EmailMessage) -> None:
    host = os.environ.get("SMTP_HOST", "")
    port = int(os.environ.get("SMTP_PORT", "465") or 465)
    user = os.environ.get("SMTP_USER", "")
    password = os.environ.get("SMTP_PASS", "")
    if not (host and user and password):
        raise RuntimeError("缺少 SMTP_HOST / SMTP_USER / SMTP_PASS")

    context = ssl.create_default_context()
    if port == 465:
        with smtplib.SMTP_SSL(host, port, context=context, timeout=60) as smtp:
            smtp.login(user, password)
            smtp.send_message(msg)
    else:
        with smtplib.SMTP(host, port, timeout=60) as smtp:
            smtp.ehlo()
            smtp.starttls(context=context)
            smtp.login(user, password)
            smtp.send_message(msg)


def send_digest(meta: dict, blocks: dict, translated: int, total: int,
                md_path: str, png_path: str, dry_run: str | None = None) -> dict:
    mail_to = [x.strip() for x in os.environ.get("MAIL_TO", "").split(",") if x.strip()]
    mail_from = (os.environ.get("MAIL_FROM") or os.environ.get("SMTP_USER")
                 or "noreply@localhost")
    if dry_run:
        mail_to = mail_to or ["test@example.com"]
    if not mail_to:
        raise RuntimeError("缺少 MAIL_TO")

    msg = build_message(meta, blocks, translated, total, md_path, png_path, mail_to, mail_from)
    if dry_run:
        with open(dry_run, "wb") as fh:
            fh.write(msg.as_bytes())
        return {"status": "dry_run", "path": dry_run, "bytes": os.path.getsize(dry_run),
                "subject": msg["Subject"]}

    send(msg)
    return {"status": "sent", "to": mail_to, "subject": msg["Subject"]}
