[app]
title = GroceryApp
package.name = groceryapp
package.domain = org.yourdomain
source.dir = .
source.include_exts = py,kv,png,jpg
version = 1.0
requirements = python3,kivy,pillow
exclude_modules = email,html,xml,unittest,pydoc,doctest,distutils
android.archs = armeabi-v7a
strip = 1
debug = 0
copy_libs = 1
icon.filename = kivy/icons/app_icon.png
orientation = portrait
fullscreen = 1

# Important paths for GitHub Actions
android.sdk_path = /home/runner/android-sdk
android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r25b
android.ndk_api = 21
android.api = 30
