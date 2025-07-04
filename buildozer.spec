[app]
title = GroceryApp
package.name = groceryapp
package.domain = org.yourdomain
source.dir = .
source.include_exts = py,kv,png,jpg
version = 1.0
requirements = python3,kivy
exclude_modules = email,html,xml,unittest,pydoc,doctest,distutils
android.archs = armeabi-v7a
strip = 1
debug = 0
copy_libs = 1
icon.filename = kivy/icons/app_icon.png
orientation = portrait
fullscreen = 1

#android.sdk_path = $HOME/.buildozer/android/platform/android-sdk
#android.ndk_path = $HOME/.buildozer/android/platform/android-ndk-r25b
android.build_tools_version = 30.0.3
android.api = 30

android.sdk_path = $ANDROIDSDK
android.ndk_path = $ANDROIDNDK
