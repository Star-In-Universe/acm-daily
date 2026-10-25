#!/usr/bin/env python3
"""调用 DeepSeek API：逐段翻译 + 生成摘要/要点/思维导图结构。"""
from __future__ import annotations

import json
import os
import re
import time
import urllib.request

API_URL = os.environ.get("DEEPSEEK_API_URL", "https://api.deepseek.com/chat/completions")
MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
KEY = os.environ.get("DEEPSEEK_API_KEY", "")

CHUNK = 40  # 每次请求最多翻译的段落数


def _chat(messages: list[dict], max_tokens: int = 8000, temperature: float = 0.3) -> str:
    if not KEY:
        raise RuntimeError("缺少 DEEPSEEK_API_KEY")
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "response_format": {"type": "json_object"},
        "stream": False,
    }
    body = json.dumps(payload).encode("utf-8")
    last: Exception | None = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                API_URL,
                data=body,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {KEY}",
                },
            )
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"DeepSeek 请求失败：{last}")


def _json(text: str) -> dict:
    text = text.strip()
    text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.M).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start >= 0 and end > start:
            return json.loads(text[start:end + 1])
        raise


TRANSLATE_SYS = (
    "你是资深技术媒体译者，为中文读者翻译《Communications of the ACM》的文章。"
    "翻译要忠实、通顺，符合中文技术媒体表达习惯。只输出 JSON，不要任何解释。"
)

TRANSLATE_TMPL = """请把下面带编号的英文段落逐段翻译成简体中文。

要求：
1. 每个编号都要有对应译文，不能漏段、不能合并段落、不能改变编号。
2. 专有名词、产品名、机构缩写保留英文（如 Databricks、AWS、API、FinOps、SAR）。
3. 数字、人名、地名、URL 原样保留。
4. (H) 是标题，(L) 是列表项，(P) 是正文段落；列表项译文要简洁。
5. 术语第一次出现可在中文后用括号附英文，之后不再重复。
6. 只输出 JSON：{{"blocks": {{"1": "译文", "2": "译文"}}}}，键为编号字符串。

待翻译段落：
{body}
"""

META_SYS = (
    "你是《Communications of the ACM》中文版的主编助理，擅长提炼技术文章的结构与要点。"
    "只输出 JSON，不要任何解释。"
)

META_TMPL = """下面是一篇 CACM 文章的英文原文。请生成中文精读材料。

输出 JSON，结构如下：
{{
  "title_zh": "中文标题（不超过 20 字，准确、不猎奇）",
  "lede_zh": "一句话导语（30 字以内）",
  "summary": "摘要，250~400 字：交代背景与问题 → 文章讲了什么、关键证据或案例 → 结论与影响。不要用'本文''值得关注'等套话开头。",
  "points": ["核心要点，4~6 条，每条一句话，包含具体信息（数字、机构、结论）"],
  "terms": [{{"en": "英文术语", "zh": "中文译名"}}],
  "mindmap": {{
    "title": "根节点，6~12 字，可用 \\n 换行",
    "branches": [
      {{"title": "一级分支，6~14 字", "children": ["二级要点，≤22 字", "二级要点"]}}
    ]
  }}
}}

思维导图要求：3~5 个一级分支，每个 2~4 个二级要点；按"背景 / 机制或方法 / 证据或案例 / 影响或争议 / 结论"的逻辑组织，用中文概括，不要照抄英文小标题。

标题：{title}
导语：{lede}

正文：
{body}
"""


def translate_blocks(blocks: list[dict], title: str = "") -> dict[str, str]:
    """返回 {"1": "译文", ...}，键为 1-based 段号。"""
    out: dict[str, str] = {}
    for start in range(0, len(blocks), CHUNK):
        chunk = blocks[start:start + CHUNK]
        lines = []
        for offset, blk in enumerate(chunk):
            idx = start + offset + 1
            tag = "H" if blk["type"] == "h" else ("L" if blk["type"] == "li" else "P")
            lines.append(f"[{idx}] ({tag}) {blk['en']}")
        body = "\n".join(lines)
        result = _json(_chat([
            {"role": "system", "content": TRANSLATE_SYS},
            {"role": "user", "content": TRANSLATE_TMPL.format(body=body)},
        ], max_tokens=8000))
        got = result.get("blocks") or result
        for idx in range(start + 1, start + len(chunk) + 1):
            value = got.get(str(idx)) or got.get(idx)
            if isinstance(value, str) and value.strip():
                out[str(idx)] = value.strip()

    missing = [i for i in range(1, len(blocks) + 1) if str(i) not in out]
    if missing:
        # 补一次，只翻缺失段
        retry_blocks = [blocks[i - 1] for i in missing]
        lines = []
        for blk, idx in zip(retry_blocks, missing):
            tag = "H" if blk["type"] == "h" else ("L" if blk["type"] == "li" else "P")
            lines.append(f"[{idx}] ({tag}) {blk['en']}")
        result = _json(_chat([
            {"role": "system", "content": TRANSLATE_SYS},
            {"role": "user", "content": TRANSLATE_TMPL.format(body="\n".join(lines))},
        ], max_tokens=4000))
        got = result.get("blocks") or result
        for idx in missing:
            value = got.get(str(idx)) or got.get(idx)
            if isinstance(value, str) and value.strip():
                out[str(idx)] = value.strip()

    still = [i for i in range(1, len(blocks) + 1) if str(i) not in out]
    if still:
        raise RuntimeError(f"仍有 {len(still)} 段未翻译：{still[:10]}")
    return out


def build_meta(title: str, lede: str, blocks: list[dict]) -> dict:
    body = "\n".join(blk["en"] for blk in blocks)
    if len(body) > 24000:  # 控制上下文
        body = body[:24000] + " …"
    meta = _json(_chat([
        {"role": "system", "content": META_SYS},
        {"role": "user", "content": META_TMPL.format(title=title, lede=lede or "无", body=body)},
    ], max_tokens=2500, temperature=0.4))

    for key in ("title_zh", "summary"):
        if not meta.get(key):
            raise RuntimeError(f"模型未返回 {key}")
    meta.setdefault("lede_zh", "")
    meta.setdefault("points", [])
    meta.setdefault("terms", [])
    mm = meta.get("mindmap") or {}
    if not mm.get("branches"):
        raise RuntimeError("模型未返回 mindmap.branches")
    mm.setdefault("title", meta["title_zh"])
    meta["mindmap"] = mm
    meta.setdefault("skip", [])
    return meta
