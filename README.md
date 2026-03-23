# 🌐 adwaaksa.com — موقع صحراء الشرق

موقع **شركة صحراء الشرق** (adwaaksa.com) — موقع SEO ثابت (Static Site Generator) مبني بـ Python، متخصص في كشف وإصلاح أعطال الكابلات الكهربائية الأرضية في الرياض وجدة.

## 🛠️ التقنيات

- **محرك البناء:** Custom SSG بـ Python
- **اللغات:** HTML5, CSS3, JavaScript (Vanilla)
- **النشر:** GitHub Actions → Cloudflare Pages (تلقائي)
- **الأتمتة:** سكريبتات Python لتوليد المقالات والصور بالذكاء الاصطناعي

## 🚀 البدء السريع

```bash
# بناء الموقع
cd adwaaksa-site && python build.py

# تشغيل خادم التطوير
python server.py

# توليد مقال جديد
automation\generate.bat "كشف أعطال الكابلات تحت الأرض"

# نشر التغييرات
git add -A && git commit -m "تحديث" && git push
```

## 📂 الهيكل

```
adwaaksa.com/
├── adwaaksa-site/     → مجلد الموقع (SSG)
├── automation/        → أدوات الأتمتة
├── .github/workflows/ → CI/CD
├── Agent.md           → ذاكرة المشروع
└── implementation-plan.md → خطة العمل
```

## 📞 بيانات التواصل

- **الهاتف:** 0558697397
- **الموقع:** [adwaaksa.com](https://adwaaksa.com)

---

> ⚠️ هذا مستودع خاص (Private). لا ترفع ملفات `.sql` أو `tokens/` أو `.env`.
