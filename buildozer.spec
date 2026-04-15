[app]
title = CocoonGlass
package.name = cocoonglass
package.domain = org.cocoonweavers
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,glsl,bin,db
version = 0.1

requirements = python3,kivy==2.3.0,kivymd==1.2.0,pyyaml,plyer,requests,urllib3,charset-normalizer,idna,certifi

orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0
android.permissions = RECORD_AUDIO, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, FOREGROUND_SERVICE, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, POST_NOTIFICATIONS

android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a

# (str) Icon of the application
#android.icon.filename = %(source.dir)s/data/icon.png

# (str) Presplash of the application
#android.presplash.filename = %(source.dir)s/data/presplash.png

android.allow_backup = True

# (list) List of service to declare
#services = transcription:service.py

android.meta_data = android.max_aspect=2.1

# (list) Permissions for MIUI and other manufacturers if needed via manifest
android.manifest.intent_filters =

# (bool) Indicate if the application should be monitor for orientation, or not
android.skip_update_buildozer = False

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpython.so
android.copy_libs = 1

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
