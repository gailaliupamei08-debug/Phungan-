[app]
title = Phungan
package.name = phungan
package.domain = org.phungan
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas
version = 1.0.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/phungan_icon-1.png

# Android settings
android.api = 35
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
