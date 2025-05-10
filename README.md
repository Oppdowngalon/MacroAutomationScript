# Macro Automation Script

This script allows you to automate mouse and keyboard actions using a sleek and modern GUI.

## How to Use

1. Run the `macro_app.py` script.
2. The GUI will open, allowing you to add, remove, and configure macro actions.

### Macro Actions

- **Type:** Types the specified text. Enter the text you want to type in the "Value" field.
- **Press:** Presses a specific key. Enter the key name you want to press in the "Value" field. For example, `enter`, `space`, `tab`, `esc`, `up`, `down`, `left`, `right`, `a`, `b`, `c`, etc., or arrow keys like `left`, `right`, `up`, `down`. You can find a list of valid key names in the PyAutoGUI documentation.
- **HotKey:** Presses a combination of keys. Enter the keys separated by `+`, for example `ctrl+s`, `ctrl+shift+esc`.
- **Click:** Clicks at a specific location. When you select "Click" as the action type, click on the screen to set the coordinates.
- **Move:** Moves the mouse cursor to a specific location. Enter the x and y coordinates separated by a comma, for example `100,200`.

### Settings

- **Interval (sec):** Sets the wait time between each action in seconds.
- **Loops:** Sets the number of times the macro will repeat.
- **Wait Time Between Loops (sec):** Sets the wait time between each loop in seconds. This delay occurs after a full cycle of actions is completed and before the next loop begins.
tempHeader: Settings (Thai)

### Controls

- **Start Macro:** Starts the macro execution.
- **Stop Macro:** Stops the macro execution.
- The loop progress is displayed in the GUI window.

## Notes

- Make sure you have the `pyautogui` library installed. You can install it using `pip install pyautogui`.
- The script uses `tkinter` for the GUI and has a modern look and feel.

## Thai Version

# สคริปต์การทำงานอัตโนมัติของ Macro

สคริปต์นี้ช่วยให้คุณสามารถทำงานอัตโนมัติของการกระทำของเมาส์และคีย์บอร์ดโดยใช้ GUI ที่ทันสมัยและสวยงาม

## วิธีการใช้งาน

1. เรียกใช้สคริปต์ `macro_app.py`
2. GUI จะเปิดขึ้น ช่วยให้คุณสามารถเพิ่ม ลบ และกำหนดค่าการกระทำของ Macro ได้

### การกระทำของ Macro

- **Type:** พิมพ์ข้อความที่ระบุ ป้อนข้อความที่คุณต้องการพิมพ์ในช่อง "Value"
- **Press:** กดปุ่มเฉพาะ ป้อนชื่อปุ่มที่คุณต้องการกดในช่อง "Value" ตัวอย่างเช่น `enter`, `space`, `tab`, `esc`, `up`, `down`, `left`, `right`, `a`, `b`, `c` หรือปุ่มลูกศรเช่น `left`, `right`, `up`, `down` คุณสามารถค้นหารายชื่อชื่อปุ่มที่ถูกต้องได้ในเอกสาร PyAutoGUI
- **HotKey:** กดปุ่มผสม ป้อนปุ่มที่คั่นด้วย `+` ตัวอย่างเช่น `ctrl+s`, `ctrl+shift+esc`
- **Click:** คลิกที่ตำแหน่งที่ระบุ เมื่อคุณเลือก "Click" เป็นประเภทการกระทำ ให้คลิกบนหน้าจอเพื่อตั้งค่าพิกัด
- **Move:** เลื่อนเคอร์เซอร์เมาส์ไปยังตำแหน่งที่ระบุ ป้อนพิกัด x และ y ที่คั่นด้วยเครื่องหมายจุลภาค ตัวอย่างเช่น `100,200`

### การตั้งค่า

- **Interval (วินาที):** กำหนดเวลารอระหว่างการกระทำแต่ละรายการเป็นวินาที
- **Loops:** กำหนดจำนวนครั้งที่ Macro จะทำซ้ำ
- **Wait Time Between Loops (วินาที):** กำหนดเวลารอระหว่างแต่ละลูปเป็นวินาที การหน่วงเวลานี้จะเกิดขึ้นหลังจากรอบการทำงานเสร็จสมบูรณ์และก่อนที่ลูปถัดไปจะเริ่มขึ้น

### การควบคุม

- **Start Macro:** เริ่มการทำงานของ Macro
- **Stop Macro:** หยุดการทำงานของ Macro
- ความคืบหน้าของลูปจะแสดงในหน้าต่าง GUI

## หมายเหตุ

- โปรดตรวจสอบให้แน่ใจว่าคุณได้ติดตั้งไลบรารี `pyautogui` แล้ว คุณสามารถติดตั้งได้โดยใช้ `pip install pyautogui`
- สคริปต์นี้ใช้ `tkinter` สำหรับ GUI และมีรูปลักษณ์ที่ทันสมัยและน่าใช้
