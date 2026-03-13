[app]
title = Showoff Fork
package.name = showoff
package.domain = ru.garagesession
source.dir = .
source.include_exts = py,json,csv,md,txt
version = 1.1.1

requirements = python3,kivy

orientation = portrait
fullscreen = 0

# Permissions (no special ones needed)
android.permissions =

android.add_src = showoff

# Entry point
entrypoint = showoff/kivy_main.py

[buildozer]
log_level = 2
warn_on_root = 1
