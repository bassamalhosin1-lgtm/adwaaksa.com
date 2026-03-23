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

# تشغيل خادم التطوير للاختبار
python server.py
```

## 🤖 التوليد الآمن للمقالات بالذكاء الاصطناعي

لضمان عدم تسريب أي مفاتيح API إلى GitHub، نستخدم الآن بيئة آمنة:

1. قم بإنشاء ملف `.env` في المجلد الرئيسي للمشروع (الملف محمي بـ `.gitignore` ولن يُرفع أبداً).
2. أضف مفتاح Google API الخاص بك داخل الملف هكذا:
   `GOOGLE_AI_KEY=AIzaSy...your_key_here`
3. شغّل سكريبت التوليد الآمن لتوليد المقالات:
   ```bash
   python generate_articles.py
   ```
4. لسحب التعديلات والصور والمقالات الجديدة إلى الموقع وبناءه، قم برفعها كالمعتاد:
   ```bash
   git add -A && git commit -m "add new articles" && git push
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
