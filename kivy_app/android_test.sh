#!/usr/bin/env bash
set -euo pipefail

# android_test.sh - automates build, deploy, run, log collection and uninstall for testing
# Usage: ./android_test.sh [clean]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

function err() { echo "ERROR: $*" >&2; exit 1; }

command -v buildozer >/dev/null 2>&1 || err "buildozer not found in PATH. Install buildozer in WSL/Linux first."
command -v adb >/dev/null 2>&1 || echo "Warning: adb not found in PATH. adb steps will be skipped if not available."

if [[ ${1-} == "clean" ]]; then
    echo "Cleaning buildozer environment..."
    buildozer android clean
fi

echo "Building debug APK (this may take a while)..."
buildozer -v android debug

APK_PATH="bin/$(grep "package.name" buildozer.spec | awk -F= '{gsub(/ /,"",$2); print $2}')-0.1-debug.apk"
if [[ ! -f "$APK_PATH" ]]; then
    echo "APK not found at $APK_PATH — attempting to find any APK in bin/"
    APK_PATH=$(ls -1 bin/*.apk 2>/dev/null | tail -n1 || true)
fi

if [[ -z "$APK_PATH" ]]; then
    echo "APK not found. Build may have failed. Look in bin/ for output." >&2
else
    echo "Found APK: $APK_PATH"
fi

if command -v adb >/dev/null 2>&1; then
    echo "Checking connected devices..."
    adb devices | sed -n '2,$p'
    echo "Deploying APK (adb install -r)..."
    if [[ -n "$APK_PATH" && -f "$APK_PATH" ]]; then
        adb install -r "$APK_PATH" || true
    fi

    # Attempt to start the app using package from buildozer.spec
    PKG=$(grep "package.name" buildozer.spec | awk -F= '{gsub(/ /,"",$2); print $2}')
    if [[ -n "$PKG" ]]; then
        echo "Starting app $PKG..."
        adb shell am start -n ${PKG}/org.kivy.android.PythonActivity || true
    fi

    echo "Clearing previous logcat and collecting logs (press Ctrl-C to stop)..."
    adb logcat -c || true
    adb logcat | sed -u -n 's/\r//g; /python/p' > android_test_log.txt &
    LOGPID=$!
    echo "Logging into android_test_log.txt (pid=$LOGPID). To stop, Ctrl-C."
    wait $LOGPID || true
else
    echo "adb not available — skipping deploy/run/log steps. You can install adb and re-run this script." >&2
fi

echo "Done. Collected logs (if any) are in android_test_log.txt"
