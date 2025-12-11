#!/bin/bash
# Automatyczny setup i budowa aplikacji Kivy TTS na iOS
# Uruchom na Macu w folderze projektu
set -e

# Instalacja zależności
brew install python@3.8 || true
pip3 install kivy edge-tts Cython kivy-ios
sudo gem install fastlane || true

# Tworzenie projektu iOS
python3 -m kivy_ios.toolchain create bookreader ios
python3 -m kivy_ios.toolchain build kivy
python3 -m kivy_ios.toolchain build python3
python3 -m kivy_ios.toolchain build edge-tts
python3 -m kivy_ios.toolchain build bookreader

# Fastlane setup
if [ ! -d ".fastlane" ]; then
  fastlane init --non-interactive || true
fi

# Budowanie i eksport przez Fastlane
fastlane build

# Uruchomienie aplikacji na symulatorze/urządzeniu
python3 -m kivy_ios.toolchain launch bookreader

echo "Gotowe! Aplikacja zbudowana i uruchomiona na iOS."
