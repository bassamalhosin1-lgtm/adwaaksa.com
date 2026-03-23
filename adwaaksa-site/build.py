"""
🔧 Adwaaksa Static Site Generator (v2 — Professional Architecture)
==================================================================
بنية احترافية قابلة للتوسيع — مشروع adwaaksa.com (صحراء الشرق)

templates/
├── layouts/       → Base layout (base.html)
├── pages/         → Page-specific content (article.html, blog_index.html)
└── partials/      → Reusable components (head, navbar, footer, cta, sidebar, scripts)

content/           → Markdown articles with YAML frontmatter
static/            → CSS, JS, images (copied as-is to dist/)
dist/              → Generated output (HTML, sitemap, robots.txt)

Workflow:
  1. Layout wraps page content
  2. Both layout and pages can {% include "partials/name" %}
  3. All {{variables}} are replaced from context
  4. Markdown is converted to semantic HTML
"""
import os, re, json, shutil
from datetime import datetime
from pathlib import Path

# ────── Config ──────
PROJECT_DIR   = Path(__file__).parent
TEMPLATES_DIR = PROJECT_DIR / 'templates'
CONTENT_DIR   = PROJECT_DIR / 'content'
STATIC_DIR    = PROJECT_DIR / 'static'
OUTPUT_DIR    = PROJECT_DIR / 'dist'

SITE_CONFIG = {
    'site_url':   'https://new.adwaaksa.com',
    'site_name':  'صحراء الشرق — كشف أعطال الكابلات',
    'phone':      '0558697397',
    'whatsapp':   '966558697397',
    'author':     'شركة صحراء الشرق',
    'og_type':    'website',
    'hero_image': '/images/default-hero.webp',
    'extra_css':  '',
    'extra_js':   '',
}


# ═══════════════════════════════════════════
#  TEMPLATE ENGINE
# ═══════════════════════════════════════════

class TemplateEngine:
    """محرّك قوالب بسيط وقوي — يدعم {% include %} و {{variables}}"""

    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir
        self._cache = {}

    def _load(self, name: str) -> str:
        """تحميل ملف قالب (مع cache)"""
        if name in self._cache:
            return self._cache[name]
        path = self.templates_dir / f'{name}.html'
        if not path.exists():
            raise FileNotFoundError(f'Template not found: {path}')
        content = path.read_text(encoding='utf-8')
        self._cache[name] = content
        return content

    def _resolve_includes(self, html: str, depth=0) -> str:
        """استبدال {% include "path/name" %} بمحتوى الملف (recursive, max 5 levels)"""
        if depth > 5:
            return html
        def replace(m):
            name = m.group(1).strip().strip('"').strip("'")
            try:
                included = self._load(name)
                return self._resolve_includes(included, depth + 1)
            except FileNotFoundError:
                return f'<!-- INCLUDE NOT FOUND: {name} -->'
        return re.sub(r'\{%\s*include\s+"?([^"%}]+)"?\s*%\}', replace, html)

    def _replace_vars(self, html: str, context: dict) -> str:
        """استبدال {{variable}} بقيم من context"""
        for key, val in context.items():
            if isinstance(val, list):
                val = ', '.join(str(v) for v in val)
            html = html.replace('{{' + key + '}}', str(val))
        return html

    def render(self, template_name: str, context: dict) -> str:
        """تحميل قالب → حل includes → استبدال متغيرات"""
        html = self._load(template_name)
        html = self._resolve_includes(html)
        html = self._replace_vars(html, context)
        return html

    def render_with_layout(self, layout_name: str, page_name: str, context: dict) -> str:
        """تجميع Page داخل Layout — الطريقة الاحترافية"""
        # 1. تحميل Page وحل includes الداخلية
        page_html = self._load(page_name)
        page_html = self._resolve_includes(page_html)

        # 2. تحميل Layout وحل includes الداخلية
        layout_html = self._load(layout_name)
        layout_html = self._resolve_includes(layout_html)

        # 3. حقن Page داخل Layout
        combined = layout_html.replace('{{page_content}}', page_html)

        # 4. استبدال جميع المتغيرات على النص النهائي المُجمّع
        final = self._replace_vars(combined, context)
        return final


# ═══════════════════════════════════════════
#  MARKDOWN CONVERTER
# ═══════════════════════════════════════════

def md_to_html(md_text: str) -> str:
    """تحويل Markdown إلى HTML دلالي (H1-H6, lists, tables, images, bold, links)"""
    lines = md_text.strip().split('\n')
    html_parts = []
    in_ul, in_ol, in_table = False, False, False

    for line in lines:
        s = line.strip()

        # إغلاق عناصر مفتوحة عند سطر فارغ
        if not s:
            if in_ul:   html_parts.append('</ul>'); in_ul = False
            if in_ol:   html_parts.append('</ol>'); in_ol = False
            if in_table: html_parts.append('</tbody></table></div>'); in_table = False
            continue

        # عناوين
        hm = re.match(r'^(#{1,6})\s+(.+)', s)
        if hm:
            level = len(hm.group(1))
            html_parts.append(f'<h{level}>{_inline(hm.group(2))}</h{level}>')
            continue

        # صور
        im = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)', s)
        if im:
            alt, src = im.groups()
            html_parts.append(f'<figure><img src="{src}" alt="{alt}" loading="lazy"><figcaption>{alt}</figcaption></figure>')
            continue

        # فاصل أفقي
        if re.match(r'^---+$', s):
            html_parts.append('<hr>')
            continue

        # قوائم نقطية
        if s.startswith('- ') or s.startswith('* '):
            if not in_ul: html_parts.append('<ul>'); in_ul = True
            html_parts.append(f'<li>{_inline(s[2:])}</li>')
            continue

        # قوائم مرقمة
        om = re.match(r'^(\d+)\.\s+(.+)', s)
        if om:
            if not in_ol: html_parts.append('<ol>'); in_ol = True
            html_parts.append(f'<li>{_inline(om.group(2))}</li>')
            continue

        # جداول
        if s.startswith('|'):
            cells = [c.strip() for c in s.split('|')[1:-1]]
            if all(set(c) <= set('-: ') for c in cells):
                continue  # separator row
            if not in_table:
                html_parts.append('<div class="table-wrap"><table><tbody>')
                in_table = True
            row = ''.join(f'<td>{_inline(c)}</td>' for c in cells)
            html_parts.append(f'<tr>{row}</tr>')
            continue

        # فقرة عادية
        html_parts.append(f'<p>{_inline(s)}</p>')

    # إغلاق أي عناصر مفتوحة
    if in_ul:    html_parts.append('</ul>')
    if in_ol:    html_parts.append('</ol>')
    if in_table: html_parts.append('</tbody></table></div>')

    return '\n'.join(html_parts)


def _inline(text: str) -> str:
    """تحويل bold, italic, links, code (inline)"""
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    return text


# ═══════════════════════════════════════════
#  FRONTMATTER PARSER
# ═══════════════════════════════════════════

def parse_frontmatter(text: str) -> tuple:
    """يستخرج YAML frontmatter + المحتوى"""
    meta = {}
    content = text
    fm = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', text, re.DOTALL)
    if fm:
        fm_text, content = fm.groups()
        for line in fm_text.split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                if val.startswith('[') and val.endswith(']'):
                    val = [v.strip().strip('"').strip("'") for v in val[1:-1].split(',')]
                meta[key] = val
    return meta, content


# ═══════════════════════════════════════════
#  SITE BUILDER
# ═══════════════════════════════════════════

def build_site():
    print('🔨 Adwaaksa SSG v2 — بدء البناء...\n')
    engine = TemplateEngine(TEMPLATES_DIR)

    # ── Prep output ──
    # if OUTPUT_DIR.exists():
    #     shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for sub in ['blog', 'home', 'css', 'js', 'images']:
        (OUTPUT_DIR / sub).mkdir(exist_ok=True)

    # ── Copy static files ──
    print('📋 نسخ الملفات الثابتة...')
    if STATIC_DIR.exists():
        for f in STATIC_DIR.rglob('*'):
            if f.is_file():
                rel = f.relative_to(STATIC_DIR)
                dest = OUTPUT_DIR / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dest)
                print(f'   {rel}')

    # ── Build articles ──
    print('\n📝 بناء المقالات...')
    articles = []
    CONTENT_DIR.mkdir(exist_ok=True)

    for md_file in sorted(CONTENT_DIR.glob('*.md')):
        meta, content_md = parse_frontmatter(md_file.read_text(encoding='utf-8'))
        slug = meta.get('slug', md_file.stem)

        ctx = {
            **SITE_CONFIG,
            'page_title': meta.get('title', slug),
            'title':       meta.get('title', slug),
            'description': meta.get('description', ''),
            'date':        meta.get('date', ''),
            'category':    meta.get('category', ''),
            'keywords':    meta.get('keywords', ''),
            'slug':        slug,
            'content':     md_to_html(content_md),
            'hero_image':  meta.get('image', meta.get('hero_image', SITE_CONFIG['hero_image'])),
            'canonical_url': f"{SITE_CONFIG['site_url']}/blog/{slug}.html",
            'og_type':     'article',
            'extra_css':   '<link rel="stylesheet" href="/css/article.css">',
            'extra_js':    '',
        }

        html = engine.render_with_layout('layouts/base', 'pages/article', ctx)
        out_path = OUTPUT_DIR / 'blog' / f'{slug}.html'
        out_path.write_text(html, encoding='utf-8')
        print(f'   ✅ blog/{slug}.html')
        articles.append(ctx)

    # ── Build blog index ──
    print('\n📚 بناء صفحة المدونة...')
    cards_html = ''
    for a in articles:
        cards_html += f'''
        <a href="/blog/{a['slug']}.html" class="blog-card" data-cat="{a['category']}">
            <div class="blog-card-img"><img src="{a['hero_image']}" alt="{a['title']}" loading="lazy"></div>
            <div class="blog-card-body">
                <span class="blog-tag">{a['category']}</span>
                <h3>{a['title']}</h3>
                <p>{a['description'][:120]}...</p>
                <span class="blog-date">{a['date']}</span>
            </div>
        </a>'''

    blog_ctx = {
        **SITE_CONFIG,
        'page_title':      'صحراء الشرق — كشف أعطال الكابلات والمدونة',
        'description':     f"مقالات متخصصة في كشف أعطال الكابلات والتمديدات. {len(articles)} مقال من خبراء الكابلات.",
        'canonical_url':   f"{SITE_CONFIG['site_url']}/",
        'articles_list':   cards_html,
        'articles_count':  str(len(articles)),
        'extra_css':       '<link rel="stylesheet" href="/css/article.css">',
        'extra_js':        '',
        'keywords':        'كشف أعطال كابلات, التماس الكهرباء, فحص كابلات, كهربائي',
    }
    blog_html = engine.render_with_layout('layouts/base', 'pages/blog_index', blog_ctx)
    (OUTPUT_DIR / 'index.html').write_text(blog_html, encoding='utf-8')
    print(f'   ✅ index.html (المدونة الرئيسية - {len(articles)} مقال)')

    # ── Build Homepage ──
    print('\n🏠 بناء الصفحة الرئيسية...')
    # Latest 6 articles for homepage
    latest_html = ''
    if articles:
        latest_html = '<div class="blog-grid">'
        for a in articles[:6]:
            latest_html += f'''
            <a href="/blog/{a['slug']}.html" class="blog-card">
                <div class="blog-card-img"><img src="{a['hero_image']}" alt="{a['title']}" loading="lazy"></div>
                <div class="blog-card-body">
                    <span class="blog-tag">{a['category']}</span>
                    <h3>{a['title']}</h3>
                    <p>{a['description'][:100]}...</p>
                    <span class="blog-date">{a['date']}</span>
                </div>
            </a>'''
        latest_html += '</div>'

    home_ctx = {
        **SITE_CONFIG,
        'page_title':      'شركة صحراء الشرق — كشف أعطال الكابلات وإصلاحها',
        'description':     'شركة صحراء الشرق متخصصة في فحص وكشف أعطال الكابلات الكهربائية وإصلاحها بأحدث الأجهزة في الرياض وجدة. اتصل الآن 0558697397',
        'keywords':        'كشف أعطال كابلات, التماس الكهرباء, فحص كابلات, إصلاح كابلات, كهربائي, الرياض, جدة',
        'canonical_url':   SITE_CONFIG['site_url'] + '/home/',
        'latest_articles': latest_html,
        'extra_css':       '',
        'extra_js':        '',
    }
    home_html = engine.render_with_layout('layouts/base', 'pages/homepage', home_ctx)
    (OUTPUT_DIR / 'home' / 'index.html').write_text(home_html, encoding='utf-8')
    print('   ✅ home/index.html (الصفحة الرئيسية القديمة)')

    # ── Sitemap & robots ──
    print('\n🗺️  بناء sitemap.xml و robots.txt...')
    today = datetime.now().strftime('%Y-%m-%d')
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += f'  <url><loc>{SITE_CONFIG["site_url"]}/</loc><lastmod>{today}</lastmod><priority>1.0</priority></url>\n'
    sitemap += f'  <url><loc>{SITE_CONFIG["site_url"]}/home/</loc><lastmod>{today}</lastmod><priority>0.9</priority></url>\n'
    for a in articles:
        sitemap += f'  <url><loc>{SITE_CONFIG["site_url"]}/blog/{a["slug"]}.html</loc><lastmod>{a["date"] or today}</lastmod><priority>0.7</priority></url>\n'
    sitemap += '</urlset>'
    (OUTPUT_DIR / 'sitemap.xml').write_text(sitemap, encoding='utf-8')
    (OUTPUT_DIR / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {SITE_CONFIG["site_url"]}/sitemap.xml\n', encoding='utf-8')
    print('   ✅ sitemap.xml + robots.txt')

    print(f'\n{"═"*50}')
    print(f'🎉 تم بناء الموقع بنجاح!')
    print(f'   📁 Output: {OUTPUT_DIR}')
    print(f'   📝 Articles: {len(articles)}')
    print(f'   🗺  Sitemap: {len(articles) + 2} URLs')
    print(f'{"═"*50}')


if __name__ == '__main__':
    build_site()
