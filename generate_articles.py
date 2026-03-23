import os
import time
import requests
from pathlib import Path

def load_env():
    """Load variables from .env file securely"""
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        # Try finding it in tokens directory as fallback
        env_path = Path(__file__).parent / "tokens" / ".env"
        
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()

# Load securely
load_env()
API_KEY = os.environ.get("GOOGLE_AI_KEY", "")

if not API_KEY:
    print("❌ ERROR: API key not found. Please create a .env file with GOOGLE_AI_KEY=your_key")
    exit(1)

MODEL = "gemini-2.5-flash"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
CONTENT_DIR = "adwaaksa-site/content"
PHONE = "0558697397"
SITE_NAME = "صحراء الشرق"
DOMAIN = "adwaaksa.com"

os.makedirs(CONTENT_DIR, exist_ok=True)

SYSTEM_PROMPT = f"""أنت خبير SEO محترف، ومتخصص في كتابة المحتوى لسوق المقاولات والخدمات في السعودية.
مهمتك الأساسية هي كتابة مقالات لموقع شركة "{SITE_NAME}".

الشروط الإلزامية:
1. المدن المستهدفة: الرياض فقط.
2. نطاق العمل: كشف التماس الكهرباء، فحص الكابلات بدون تكسير، وأعطال الكابلات الأرضية.
3. دمج رقم الهاتف {PHONE} بأسلوب طبيعي ومقنع (CTA) داخل المقال وفي نهايته.
4. استخدم تنسيق Markdown وتأكد من تضمين العناوين H2 و H3.
5. يجب أن يحتوي المقال على 1000 كلمة على الأقل مع الحفاظ على القيمة العالية للمحتوى.
"""

NEW_ARTICLES = [
    {
        "keyword": "شركة صيانة كهرباء منازل بالرياض",
        "slug": "home-electrical-maintenance-company-riyadh",
        "instruction": "مقال شامل عن أهمية صيانة الكهرباء الدورية في المنازل لتفادي التماسات، وكيف تقدم شركة صحراء الشرق هذه الخدمة باحترافية وسرعة استجابة في الرياض."
    },
    {
        "keyword": "أسباب احتراق أسلاك الكهرباء في الجدار",
        "slug": "causes-of-wire-burning-inside-walls",
        "instruction": "مقال توعوي يشرح للمستخدم أسباب احتراق الأسلاك وتلفها داخل الجدران (مثل زيادة الأحمال وسوء التأسيس)، وكيف يمكن لأجهزة الكشف الحديثة تحديد المشكلة دون تكسير."
    },
    {
        "keyword": "اصلاح اعطال الكابلات الارضية بدون حفر",
        "slug": "repair-underground-cable-faults-no-digging",
        "instruction": "مقال تقني يبسط للمستخدم العادي تقنية تحديد موقع عطل الكيبل تحت الأرض بدقة، بحيث يتم الحفر فقط في نقطة العطل بدلاً من تشويه الحوش أو المنزل بالكامل."
    },
    {
        "keyword": "علامات تسريب الكهرباء في المنزل",
        "slug": "signs-of-electrical-leakage-in-home",
        "instruction": "مقال عن تسريب الكهرباء الذي يؤدي إلى ارتفاع فاتورة الكهرباء ورعشة الإضاءة، وكيف تقوم شركة صحراء الشرق بفحص شامل لعزل الكابلات لحل هذه المشكلة."
    },
    {
        "keyword": "خطورة التماس الكهرباء عند نزول المطر",
        "slug": "danger-of-short-circuit-during-rain",
        "instruction": "مقال موسمي مهم جداً عن دخول مياه الأمطار إلى الكابلات والتمديدات الخارجية مما يسبب فصل القاطع، وكيفية العزل الصحيح ومعالجة هذه التماسات."
    },
    {
        "keyword": "جهاز فحص التماس الكهرباء وتحديد الاعطال",
        "slug": "short-circuit-detection-device-technology",
        "instruction": "مقال تعريفي بالأجهزة الحديثة التي تستخدمها شركة صحراء الشرق لتحديد أعطال الكهرباء والتماسات بدقة عالية، لبناء الثقة مع العميل وإبراز الاحترافية."
    },
    {
        "keyword": "رقم فني كهرباء طوارئ بالرياض 24 ساعة",
        "slug": "emergency-electrician-number-riyadh-24-hours",
        "instruction": "مقال يركز جداً على جانب الطوارئ، حيث توفر الشركة استجابة سريعة لأي حالة التماس أو انقطاع مفاجئ للتيار في الرياض. المقال يجب أن يكون محفزاً للاتصال الفوري."
    }
]

def generate_article(keyword, slug, instruction):
    user_prompt = f"""{instruction}

الكلمة المفتاحية الأساسية: {keyword}

المطلوب: مقال SEO كامل بصيغة Markdown يبدأ بـ frontmatter كالتالي:
---
title: "عنوان المقال (يحتوي على الكلمة المفتاحية بشكل تسويقي جذاب)"
slug: "{slug}"
category: "صيانة كهرباء"
date: "2026-03-23"
description: "وصف ميتا 150-160 حرف يحتوي على الكلمة المفتاحية واسم الشركة"
image: "/images/articles/{slug}.png"
keywords: ["{keyword}", "الرياض", "صحراء الشرق"]
---

ثم المحتوى المنسق بشكل جميل باستخدام Markdown (H2, H3، وتعداد نقطي إذا لزم الأمر، وقسم للأسئلة الشائعة في النهاية)."""

    body = {
        "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
        "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 8192}
    }
    
    try:
        r = requests.post(API_URL, json=body, timeout=120)
        if r.status_code == 200:
            data = r.json()
            for c in data.get("candidates", []):
                for p in c.get("content", {}).get("parts", []):
                    return p.get("text")
        else:
            print(f"    ❌ API Error {r.status_code}: {r.text[:200]}")
    except Exception as e:
        print(f"    ❌ Exception: {e}")
    return None

def main():
    print("🚀 بدء تشغيل سكريبت التوليد الآمن...")
    
    # Check existing files to determine starting number
    existing_files = [f for f in os.listdir(CONTENT_DIR) if f.endswith('.md')]
    next_num = len(existing_files) + 1
    
    for art in NEW_ARTICLES:
        fn = f"{next_num:02d}-{art['slug']}.md"
        fp = os.path.join(CONTENT_DIR, fn)
        
        # Skip if slug already broadly exists
        if any(art['slug'] in f for f in existing_files):
            print(f"⏭️ تخطي '{art['keyword']}' — المقال موجود مسبقاً.")
            continue
            
        print(f"⏳ جاري كتابة مقال: {art['keyword']}...")
        text = generate_article(art["keyword"], art["slug"], art["instruction"])
        
        if text:
            text = text.strip()
            if text.startswith('```markdown'):
                text = text[len('```markdown'):]
            if text.startswith('```'):
                text = text[3:]
            if text.endswith('```'):
                text = text[:-3]
                
            text = text.strip()
            
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"✅ تم الحفظ بنجاح: {fn}")
            next_num += 1
        else:
            print(f"❌ فشل توليد المقال: {art['keyword']}")
            
        time.sleep(3) # Delay to respect API limits

if __name__ == "__main__":
    main()
