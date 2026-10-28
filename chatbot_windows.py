"""Windows implementation of the chat-window automation example.

Install the Tesseract OCR executable separately and ensure it is available on PATH.
The chat and reply-box coordinates below are examples; adjust them for your display.
"""
import re
import time

import pyautogui
import pytesseract
from pytesseract import Output

# Coordinates are in screen pixels: (left, top, width, height).
CHAT_REGION = (552, 188, 889, 605)
REPLY_POINT = (665, 831)
POLL_INTERVAL_SECONDS = 5
OCR_LANGUAGE = "eng"

TIME_PATTERN = re.compile(r"^\d{1,2}:\d{2}\s?(am|pm)$", re.IGNORECASE)
last_processed_message = None


def take_screenshot():
    """Capture the configured chat area without writing the image to disk."""
    return pyautogui.screenshot(region=CHAT_REGION)


def imagetotext(image, lang=OCR_LANGUAGE):
    """Return one OCR record per text line with normalized horizontal position."""
    data = pytesseract.image_to_data(
        image,
        lang=lang,
        output_type=Output.DICT,
    )
    lines = {}

    for index, raw_text in enumerate(data["text"]):
        text = raw_text.strip()
        if not text:
            continue

        key = (
            data["block_num"][index],
            data["par_num"][index],
            data["line_num"][index],
        )
        confidence = float(data["conf"][index])
        left = int(data["left"][index])
        top = int(data["top"][index])
        width = int(data["width"][index])
        entry = lines.setdefault(
            key,
            {"words": [], "confidence": [], "left": left, "right": left + width, "top": top},
        )
        entry["words"].append(text)
        if confidence >= 0:
            entry["confidence"].append(confidence)
        entry["left"] = min(entry["left"], left)
        entry["right"] = max(entry["right"], left + width)
        entry["top"] = min(entry["top"], top)

    image_width = image.width or 1
    results = []
    for entry in lines.values():
        text = " ".join(entry["words"])
        center_x = (entry["left"] + entry["right"]) / 2 / image_width
        confidences = entry["confidence"]
        confidence = sum(confidences) / len(confidences) if confidences else 0
        results.append([text, confidence, center_x, entry["top"]])

    return results


def is_time(text):
    return TIME_PATTERN.fullmatch(text.strip()) is not None


def clean_text(text):
    text = TIME_PATTERN.sub("", text)
    text = re.sub(r"/+", "", text)
    return text.strip()


def get_reply(message):
    """Keep the sample project's existing reply rules."""
    lowered = message.lower()
    if "kaha" in lowered:
        return "Room me hu"
    if "aa" in lowered:
        return "Aa raha hu"
    return "Okay"


def process_results(results):
    """Find and reply once to the latest received line in the captured area."""
    global last_processed_message

    conversation = []
    for text, _confidence, center_x, _top in sorted(results, key=lambda item: item[3]):
        if is_time(text):
            continue
        text = clean_text(text)
        if not text:
            continue
        role = "received" if center_x < 0.5 else "sent"
        conversation.append({"role": role, "text": text})

    for message in conversation:
        print(message)

    latest_message = next(
        (message for message in reversed(conversation) if message["role"] == "received"),
        None,
    )
    if latest_message is None:
        print("No received message found")
        return

    latest_text = latest_message["text"]
    if latest_text == last_processed_message:
        print("Already processed")
        return

    print("Latest message:", latest_message)
    reply = get_reply(latest_text)
    print("Reply:", reply)

    pyautogui.click(*REPLY_POINT)
    time.sleep(0.5)
    pyautogui.write(reply, interval=0.05)
    pyautogui.press("enter")
    last_processed_message = latest_text


def main():
    print("Checking messages. Press Ctrl+C to stop.")
    time.sleep(5)
    while True:
        results = imagetotext(take_screenshot())
        process_results(results)
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
