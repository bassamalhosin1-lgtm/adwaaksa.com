#!/usr/bin/env python3
"""
GSC Manager — List sites, submit sitemap, check sitemaps status
"""
import sys
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

CREDS_PATH = r"c:\Users\Abdalgani\Desktop\myapp\adwaaksa.com\tokens\gold-yen-491119-m9-2a5fdc05a2b8.json"
SCOPES = ['https://www.googleapis.com/auth/webmasters']

SITE_URL = 'sc-domain:adwaaksa.com'
SITEMAP_URL = 'https://new.adwaaksa.com/sitemap.xml'

def get_service():
    credentials = Credentials.from_service_account_file(CREDS_PATH, scopes=SCOPES)
    return build('searchconsole', 'v1', credentials=credentials)

def main():
    service = get_service()
    
    # 1. List sites
    print("=" * 50)
    print("1. قائمة المواقع المربوطة بحساب الخدمة:")
    print("=" * 50)
    try:
        sites = service.sites().list().execute()
        entries = sites.get('siteEntry', [])
        if entries:
            for s in entries:
                print(f"   ✅ {s['siteUrl']} — صلاحية: {s['permissionLevel']}")
        else:
            print("   ⚠️ لا توجد مواقع مربوطة! تأكد من إضافة إيميل الحساب كمالك في GSC")
    except Exception as e:
        print(f"   ❌ خطأ: {e}")
    
    # 2. Submit sitemap
    print("\n" + "=" * 50)
    print(f"2. إرسال خريطة الموقع: {SITEMAP_URL}")
    print("=" * 50)
    try:
        service.sitemaps().submit(siteUrl=SITE_URL, feedpath=SITEMAP_URL).execute()
        print("   ✅ تم إرسال خريطة الموقع بنجاح!")
    except Exception as e:
        print(f"   ❌ خطأ: {e}")

    # 3. List sitemaps
    print("\n" + "=" * 50)
    print("3. حالة خرائط الموقع المسجلة:")
    print("=" * 50)
    try:
        sitemaps = service.sitemaps().list(siteUrl=SITE_URL).execute()
        entries = sitemaps.get('sitemap', [])
        if entries:
            for sm in entries:
                print(f"   📄 {sm['path']}")
                print(f"      آخر تحميل: {sm.get('lastDownloaded', 'لم يتم بعد')}")
                print(f"      تحذيرات: {sm.get('warnings', 0)} | أخطاء: {sm.get('errors', 0)}")
                contents = sm.get('contents', [])
                for c in contents:
                    print(f"      نوع: {c.get('type', '?')} — مرسل: {c.get('submitted', '?')} — مفهرس: {c.get('indexed','?')}")
        else:
            print("   لا توجد خرائط موقع مسجلة بعد")
    except Exception as e:
        print(f"   ❌ خطأ: {e}")

    # 4. Search analytics (last 7 days)
    print("\n" + "=" * 50)
    print("4. تحليلات البحث (آخر 7 أيام):")
    print("=" * 50)
    from datetime import datetime, timedelta
    end = datetime.now().strftime('%Y-%m-%d')
    start = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    try:
        result = service.searchanalytics().query(
            siteUrl=SITE_URL,
            body={
                'startDate': start,
                'endDate': end,
                'dimensions': ['query'],
                'rowLimit': 10
            }
        ).execute()
        rows = result.get('rows', [])
        if rows:
            print(f"   {'الكلمة المفتاحية':<40} نقرات   ظهور")
            print("   " + "-" * 60)
            for r in rows:
                kw = r['keys'][0]
                print(f"   {kw:<40} {r['clicks']:<8} {r['impressions']}")
        else:
            print("   📭 لا توجد بيانات بحث بعد (الموقع جديد، جوجل يحتاج عدة أيام)")
    except Exception as e:
        print(f"   ❌ خطأ: {e}")

    print("\n" + "=" * 50)
    print("✅ انتهى الفحص!")
    print("=" * 50)

if __name__ == '__main__':
    main()
