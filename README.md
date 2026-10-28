# Chatbot Automation Project

A Python-based chatbot automation project that reads messages from a chat window using OCR, identifies the latest received message, generates a reply, and automatically sends it.

## Platform

This project is currently developed and tested on **macOS**.

The current OCR implementation uses Apple's **Vision framework** along with macOS-specific frameworks such as Quartz, Cocoa, and Foundation.

Therefore, the current implementation is specifically designed for macOS.

## Windows Support

The main chatbot logic can be reused on Windows.

However, the current OCR implementation uses Apple's Vision framework, which is not available on Windows.

For Windows support, the macOS-specific OCR components will be replaced with a Windows-compatible OCR solution.

The goal is to keep the main chatbot logic common across both platforms while changing only the platform-specific components.

## Current Workflow

```text
Chat Window
     ↓
Screenshot
     ↓
OCR
     ↓
Extract Messages
     ↓
Identify Latest Received Message
     ↓
Generate Reply
     ↓
PyAutoGUI
     ↓
Send Reply

## Windows Setup and Usage

The macOS implementation remains in `chatbot.py`. On Windows, use the separate
`chatbot_windows.py` entry point.

1. Install Python 3 and Tesseract OCR for Windows. During Tesseract setup, enable
   adding Tesseract to `PATH` (or add its installation folder to `PATH` manually).
2. In PowerShell, install the Python dependencies:

   ```powershell
   py -m pip install -r requirements.txt
   ```

3. Edit `CHAT_REGION` and `REPLY_POINT` near the top of `chatbot_windows.py`
   to match the chat window and its message box on your display.
4. Open the chat window and run:

   ```powershell
   py chatbot_windows.py
   ```

The script captures the configured chat area, reads message lines with Tesseract,
and uses the same sample reply rules as the macOS script. It sends a reply only
when it detects a new received message. Press `Ctrl+C` in the terminal to stop it.

