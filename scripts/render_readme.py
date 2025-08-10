from pathlib import Path
import json, re, datetime as dt

root = Path(__file__).resolve().parent.parent

# 读入配置
data = json.loads((root / 'links.json').read_text(encoding='utf-8'))

# 读模板 & 正文
tpl = (root / 'README.tpl.md').read_text(encoding='utf-8')
content_path = root / 'CONTENT.md'
custom_content = content_path.read_text(encoding='utf-8') if content_path.exists() else ""

# 计算字段
def osf_slug(url: str) -> str:
    try:
        return url.rstrip('/').split('/')[-1]
    except Exception:
        return ""

kv = {
    "title": data.get("title", ""),
    "subtitle": data.get("subtitle", ""),
    "repo_url": data.get("repo_url", ""),
    "osf_url": data.get("osf_url", ""),
    "osf_slug": osf_slug(data.get("osf_url", "")),
    "zenodo_concept_doi": data.get("zenodo_concept_doi", ""),
    "last_updated": dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
    "custom_content": custom_content.strip(),
}

# 渲染 {{key}} 占位符
def render(t: str, kv: dict) -> str:
    for k, v in kv.items():
        t = re.sub(r'{{\s*' + re.escape(k) + r'\s*}}', v, t)
    return t

out = render(tpl, kv)
(root / 'README.md').write_text(out, encoding='utf-8')
print("README.md updated.")
