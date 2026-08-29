[app]

# (str) Title of your application
title = Snake Game

# (str) Package name
package.name = snakegame

# (str) Package domain (needed for android packaging)
package.domain = org.example

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 0.1

# (list) Application requirements
requirements = python3,kivy

# (str) Supported orientation
orientation = portrait

# (bool) Fullscreen application
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API supported
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (bool) Auto accept SDK license
android.accept_sdk_license = True

# (str) Android NDK architecture to build for
android.archs = arm64-v8a, armeabi-v7a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
