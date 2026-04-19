---
name: reduce-aigc-traces
description: Rewrites user-supplied text to reduce AI-written patterns while preserving meaning and terminology. Covers general Chinese, academic Chinese (papers/reports), and English. Use when the user asks to 降AIGC、去AI味、人性化改写、学术降重风格、humanize text、remove AI patterns、rewrite to sound human-written, or references AIGC traces.
---

# Reduce AIGC Traces (Humanize Rewrite)

## When to Use Which Variant

| Variant | Use When |
|--------|-----------|
| **General (Chinese)** | Everyday/professional prose in Chinese; not formally a thesis section. |
| **Academic (Chinese)** | Papers, reports, literature reviews, methodology sections in Chinese. |
| **English** | Any English text where the user wants less “LLM-shaped” phrasing. |

If the user does not specify, infer from language and cues (e.g. “论文/报告/摘要/引言” → academic Chinese).

## Shared Rules (All Variants)

- Preserve **core information**, **logic**, **facts/data**, and **professional terms** exactly as given. Do not add claims or soften rigor in academic contexts.
- **Output only the rewritten text** — no preamble, bullets, meta-commentary, or “here is the rewrite.”
- Prefer **plain, restrained** tone; avoid hype adjectives and emotional padding.
- **Vary rhythm**: mix short and long sentences; avoid mechanically parallel paragraphs.
- **Cut template glue**: remove or replace stock transitions that read like outlines (see variant prompts).
- **Natural paragraphs**: looser structure is fine; do not force uniform “three-part” blocks.

## Execution: Apply the Matching System Prompt

Treat the following as **hard constraints** for the rewrite. The agent should follow the chosen block literally.

### 1. General Chinese — 降低AIGC痕迹

请严格保留原文核心信息、专业术语与逻辑不变，对文本进行人性化重写：1. 打破AI式完美对称句式，长短句交错；2. 删除模板化连接词（首先、其次、综上所述、总而言之等）；3. 减少过度排比与冗余修饰；4. 段落结构自然松散，不刻意规整；5. 语气平实克制，不使用夸张副词与情绪化表达；6. 避免机械分段，保持自然行文节奏；7. 只输出改写后的最终文本，不解释、不添加额外内容。

### 2. Academic Chinese — 学术降AI痕迹

在完全保留学术严谨性、核心论点、数据与专业术语不变的前提下重写：1. 拆解AI式长难句，改用更自然的学术表达；2. 去掉固定框架词与套路化总结；3. 调整句式节奏，避免结构高度统一；4. 精简冗余解释，保留关键论证；5. 行文符合人类写作习惯，逻辑连贯不生硬；6. 仅输出改写结果，无额外说明。

### 3. English — Reduce AIGC Traces

Rewrite the text to eliminate AI-generated patterns while preserving all core meaning, facts, and key terms. 1. Break up overly perfect symmetric sentences; mix short and long sentences. 2. Remove template phrases: first, second, in conclusion, overall, etc. 3. Avoid repetitive structures and redundant adjectives. 4. Use natural paragraph flow, not rigid formatting. 5. Keep tone neutral and concise. 6. Output only the revised text, no explanations.

## Quality Check (Silent, Before Answering)

- If the draft still reads like a checklist or every paragraph opens the same way, revise once more.
- Terminology and claims still match the source; no new citations or numbers invented.

## Examples

**User:** “把下面这段话去AI味（中文）… [paste]”  
**Agent:** Select **General Chinese** block, output **only** the rewritten paragraph(s).

**User:** “Discussion section sounds GPT-ish, keep it academic” + Chinese text  
**Agent:** Select **Academic Chinese** block.

**User:** “Reduce AIGC traces” + English abstract  
**Agent:** Select **English** block.
