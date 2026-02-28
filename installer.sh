#!/data/data/com.termux/files/usr/bin/bash

echo -e "\033[31m"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║          QUADDOS - TERMUX INSTALLER                      ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "\033[0m"

echo -e "\033[33m[*] Updating packages...\033[0m"
pkg update -y && pkg upgrade -y

echo -e "\033[33m[*] Installing required packages...\033[0m"
pkg install -y python
pkg install -y python-pip
pkg install -y git
pkg install -y clang
pkg install -y libffi
pkg install -y openssl
pkg install -y rust
pkg install -y binutils

echo -e "\033[33m[*] Installing Python dependencies...\033[0m"
pip install --upgrade pip
pip install aiohttp
pip install requests
pip install asyncio
pip install colorama
