[app]
title = Service Test
package.name = servicetest
package.domain = com.snuq
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
version = 1.0
requirements = python3,kivy,plyer,oscpy
orientation = portrait
services = servicetestbg:service.py:foreground
#maybe add - :sticky
android.permissions = android.permission.INTERNET, android.permission.FOREGROUND_SERVICE
android.archs = arm64-v8a, armeabi-v7a


[buildozer]
log_level = 2
warn_on_root = 1
