#!/usr/bin/env python3
"""把当天 1~N 篇文章组装成一封 HTML 邮件并通过 SMTP 发出。"""
from __future__ import annotations

import html as html_mod
import os
import smtplib
import ssl
from datetime import datetime
from email.message import EmailMessage
from email.utils import formataddr, formatdate


def _esc(text: str) -> str:
    return html_mod.escape(str(text), quote=False)


def _article_block(index: int, art: dict) -> str:
    meta, blocks = art["meta"], art["blocks"]
    title_zh = _esc(meta.get("title_zh", ""))
    title_en = _esc(blocks.get("title", ""))
    lede = _esc(meta.get("lede_zh", "") or "")
    summary = _esc(meta.get("summary", "")).replace("\n", "<br>")
    points = "".join(
        f'<li style="margin:5px 0;line-height:1.65">{_esc(p)}</li>'
        for p in meta.get("points", [])[:4]
    )
    section = _esc(meta.get("section", ""))
    link = _esc(meta.get("link", ""))
    border = "none" if index == 0 else "2px solid #EDF1F7"

    return f"""
  <div style="margin:0 0 28px;padding-top:{'0' if index == 0 else '22px'};border-top:{border}">
    <div style="font-size:12px;color:#8A93A0;margin-bottom:6px">{section}</div>
    <h2 style="font-size:19px;line-height:1.5;margin:0 0 4px;color:#1F2937">{title_zh}</h2>
    <div style="font-size:12.5px;color:#7A8494;margin-bottom:10px">{title_en}</div>
    {f'<div style="font-size:14px;color:#4B5563;line-height:1.7;margin-bottom:12px">{lede}</div>' if lede else ''}

    <div style="background:#fff;border-radius:10px;padding:14px 16px;margin-bottom:12px;
                box-shadow:0 1px 3px rgba(16,24,40,.06)">
      <div style="font-size:12px;color:#2F6FD0;font-weight:600;margin-bottom:6px">摘要</div>
      <div style="font-size:14px;line-height:1.8;color:#374151">{summary}</div>
    </div>

    <div style="background:#fff;border-radius:10px;padding:14px 16px;margin-bottom:12px;
                box-shadow:0 1px 3px rgba(16,24,40,.06)">
      <div style="font-size:12px;color:#2F6FD0;font-weight:600;margin-bottom:6px">核心要点</div>
      <ul style="margin:0;padding-left:18px;font-size:13.5px;color:#374151">{points}</ul>
    </div>

    <img src="cid:mindmap{index}@cacm" alt="思维导图"
         style="width:100%;height:auto;display:block;border-radius:8px;border:1px solid #EDF1F7">
    <div style="font-size:12px;color:#98A2B3;margin-top:8px">
      中英对照全文见附件 <b>{_esc(art['filename'])}</b> ·
      <a href="{link}" style="color:#2F6FD0">原文</a>
    </div>
  </div>"""


def build_html(articles: list[dict], date_label: str) -> str:
    body = "".join(_article_block(i, a) for i, a in enumerate(articles))
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>CACM 每日推送</title></head>
<body style="margin:0;padding:0;background:#F4F6FA;font-family:-apple-system,'PingFang SC','Microsoft YaHei',Arial,sans-serif">
<div style="max-width:680px;margin:0 auto;padding:20px 16px 32px">

  <div style="font-size:12px;color:#8A93A0;letter-spacing:1px;margin-bottom:14px">
    CACM 每日推送 · {_esc(date_label)} · 共 {len(articles)} 篇
  </div>

  {body}

  <div style="font-size:11.5px;color:#A7B0BD;line-height:1.7;border-top:1px solid #E5E9F0;padding-top:12px">
    英文原文版权归 Communications of the ACM 及作者所有；中文译文由 AI 辅助生成，仅供学习参考。<br>
    本邮件由 GitHub Actions 定时生成 · {datetime.now().strftime('%Y-%m-%d %H:%M')}
  </div>
</div>
</body></html>"""


def build_text(articles: list[dict], date_label: str) -> str:
    parts = [f"CACM 每日推送 · {date_label} · 共 {len(articles)} 篇", ""]
    for i, a in enumerate(articles, 1):
        meta = a["meta"]
        parts += [f"[{i}] {meta.get('title_zh','')}", a["blocks"].get("title", ""), "",
                  meta.get("summary", ""), "", "要点："]
        parts += [f"- {p}" for p in meta.get("points", [])]
        parts += ["", f"原文：{meta.get('link','')}",
                  f"全文：附件 {a['filename']}", "", "-" * 40, ""]
    return "\n".join(parts)


def build_message(articles: list[dict], mail_to: list[str], mail_from: str,
                  date_label: str) -> EmailMessage:
    if len(articles) == 1:
        subject = f"[CACM] {date_label} · {articles[0]['meta'].get('title_zh','')}"
    else:
        first = articles[0]["meta"].get("title_zh", "")
        subject = f"[CACM] {date_label} · {len(articles)} 篇｜{first} 等"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr(("CACM 每日推送", mail_from))
    msg["To"] = ", ".join(mail_to)
    msg["Date"] = formatdate(localtime=True)

    msg.set_content(build_text(articles, date_label))
    msg.add_alternative(build_html(articles, date_label), subtype="html")

    html_part = msg.get_payload()[1]
    for i, art in enumerate(articles):
        with open(art["png"], "rb") as fh:
            html_part.add_related(fh.read(), maintype="image", subtype="png",
                                  cid=f"mindmap{i}@cacm")

    for art in articles:
        with open(art["md"], "rb") as fh:
            msg.add_attachment(fh.read(), maintype="text", subtype="markdown",
                               filename=art["filename"])
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
        with smtplib.SMTP_SSL(host, port, context=context, timeout=90) as smtp:
            smtp.login(user, password)
            smtp.send_message(msg)
    else:
        with smtplib.SMTP(host, port, timeout=90) as smtp:
            smtp.ehlo()
            smtp.starttls(context=context)
            smtp.login(user, password)
            smtp.send_message(msg)


def send_digest(articles: list[dict], date_label: str,
                dry_run: str | None = None) -> dict:
    mail_to = [x.strip() for x in os.environ.get("MAIL_TO", "").split(",") if x.strip()]
    mail_from = (os.environ.get("MAIL_FROM") or os.environ.get("SMTP_USER")
                 or "noreply@localhost")
    if dry_run:
        mail_to = mail_to or ["test@example.com"]
    if not mail_to:
        raise RuntimeError("缺少 MAIL_TO")

    msg = build_message(articles, mail_to, mail_from, date_label)
    if dry_run:
        with open(dry_run, "wb") as fh:
            fh.write(msg.as_bytes())
        return {"status": "dry_run", "path": dry_run,
                "bytes": os.path.getsize(dry_run), "subject": str(msg["Subject"])}

    send(msg)
    return {"status": "sent", "to": mail_to, "subject": str(msg["Subject"])}
