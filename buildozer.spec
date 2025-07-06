[app]
title = GroceryApp
package.name = groceryapp
package.domain = org.yourdomain
source.dir = .
source.include_exts = py,kv,png,jpg,db
source.include_patterns = **/*.kv, **/*.db, **/*.png
version = 1.0
requirements = python3==3.10.11,kivy,pillow,libffi,pyjnius,cython==0.29.36
icon.filename = kivy/icons/app_icon.png
fullscreen = 1
orientation = portrait
android.api = 30
android.ndk_api = 21
android.sdk_path = /opt/android-sdk
android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r25b
android.archs = armeabi-v7a
copy_libs = 1
strip = 1

[buildozer]
warn_on_root = 0
