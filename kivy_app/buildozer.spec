[app]
# (str) Title of your application
title = SimpleKivyApp

# (str) Package name
package.name = simplekivyapp

# (str) Package domain (reverse domain notation)
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .
source.include_exts = py,kv,png,jpg,atlas

# (str) Application versioning
version = 0.1

# (list) Application requirements
# Use exact kivy version installed on your machine to avoid mismatches when packaging
requirements = python3,kivy==2.3.1

# (str) Supported orientation (portrait, landscape or all)
orientation = portrait

# (list) Permissions
android.permissions = INTERNET

# (str) Icon (place a 512x512 png at the path below or adjust path)
icon.filename = %(source.dir)s/icon.png

# Android specific
android.api = 33
android.ndk = 25b

# (int) Android version code (Google Play uses this to distinguish updates)
android.version_code = 1

# (list) Supported architectures
android.archs = armeabi-v7a, arm64-v8a

# (int) Minimum Android API your app uses
android.minapi = 21

# (bool) Indicate whether to copy the .pyd/.so from the host
android.copy_libs = 1

# (list) Additional common permissions you may need. Enable the ones your app requires.
# Examples:
#  - Location: ACCESS_FINE_LOCATION
#  - Camera: CAMERA
#  - Microphone: RECORD_AUDIO
#  - Storage (legacy): READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
# Note: Android 11+ has scoped storage; WRITE_EXTERNAL_STORAGE may not behave as on older APIs.
android.permissions = INTERNET,CAMERA,RECORD_AUDIO,ACCESS_FINE_LOCATION,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# (bool) Allow backup on Android (set to 0/False for sensitive apps)
android.allow_backup = False

# (bool) Use AndroidX libraries
android.use_androidx = True

# Signing / release configuration (fill these for release builds)
# android.keystore = /path/to/your.keystore
# android.keystore_password = your_keystore_password
# android.keyalias = your_key_alias
# android.keyalias_password = your_key_alias_password
# android.release = 1
