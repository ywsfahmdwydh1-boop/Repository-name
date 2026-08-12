[app]

# اسم التطبيق
title = Number Guessing Game

# اسم الحزمة
package.name = numberguessing

# الدومين
package.domain = org.example

# ملف التشغيل
source.include_exts = py,png,jpg,jpeg,kv,atlas

# مجلد المشروع
source.dir = .

# ملف البداية
entrypoint = main.py

# إصدار التطبيق
version = 1.0

# المكتبات المطلوبة
requirements = python3,kivy

# اتجاه الشاشة
orientation = portrait

# اسم الشاشة
fullscreen = 0


[buildozer]

# مستوى التحذيرات
log_level = 2

# تشغيل التحسين
warn_on_root = 1


[app:android]

# معمارية أندرويد
android.archs = arm64-v8a

# أقل إصدار أندرويد
android.minapi = 21

# إصدار SDK
android.api = 35

# إصدار NDK
android.ndk = 27c

# قبول تراخيص أندرويد
android.accept_sdk_license = True
