import fitz  # PyMuPDF
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
img_dir = os.path.join(base_dir, "assets", "screenshots", "raw")
pdf_path = os.path.join(base_dir, "Process_Lifecycles_Step_by_Step_Guide.pdf")

doc = fitz.open()

# A4 dimensions in points: 595.3 x 841.9
PAGE_WIDTH = 595.3
PAGE_HEIGHT = 841.9
MARGIN = 40.0
CONTENT_WIDTH = PAGE_WIDTH - 2 * MARGIN

def add_header(page, y):
    page.insert_text(fitz.Point(MARGIN, y), "Process Lifecycles & OS Interaction: Step-by-Step\nGuide", 
                     fontsize=20, fontname="helv", color=(0.1, 0.1, 0.1))
    y += 50
    intro = ("A process is a program in execution managed by the operating system kernel. "
             "The lifecycle of a process involves creation, memory allocation, execution, "
             "background monitoring, and termination status reporting. This document provides "
             "a practical demonstration of each phase.")
    rc = fitz.Rect(MARGIN, y, MARGIN + CONTENT_WIDTH, y + 45)
    page.insert_textbox(rc, intro, fontsize=10.5, fontname="helv", color=(0.2, 0.2, 0.2))
    return y + 55

def add_step(page, y, step_title, objective, command, img_filename, observation, max_img_h=190):
    page.insert_text(fitz.Point(MARGIN, y), step_title, fontsize=13, fontname="hebo", color=(0.1, 0.1, 0.1))
    y += 18

    obj_rect = fitz.Rect(MARGIN + 12, y - 9, MARGIN + CONTENT_WIDTH, y + 25)
    page.insert_text(fitz.Point(MARGIN, y), chr(8226), fontsize=10, fontname="helv", color=(0.1, 0.1, 0.1))
    page.insert_textbox(obj_rect, f"Objective: {objective}", fontsize=9.5, fontname="helv", color=(0.2, 0.2, 0.2))
    y += 24

    cmd_rect = fitz.Rect(MARGIN + 12, y - 9, MARGIN + CONTENT_WIDTH, y + 20)
    page.insert_text(fitz.Point(MARGIN, y), chr(8226), fontsize=10, fontname="helv", color=(0.1, 0.1, 0.1))
    page.insert_textbox(cmd_rect, f"Command: {command}", fontsize=9.5, fontname="helv", color=(0.2, 0.2, 0.2))
    y += 20

    page.insert_text(fitz.Point(MARGIN, y), chr(8226), fontsize=10, fontname="helv", color=(0.1, 0.1, 0.1))
    page.insert_text(fitz.Point(MARGIN + 12, y), "Image Placeholder:", fontsize=9.5, fontname="hebo", color=(0.2, 0.2, 0.2))
    y += 10

    img_path = os.path.join(img_dir, img_filename)
    if os.path.exists(img_path):
        img_doc = fitz.open(img_path)
        img_w, img_h = img_doc[0].rect.width, img_doc[0].rect.height
        aspect = img_h / img_w
        target_w = CONTENT_WIDTH
        target_h = target_w * aspect
        if target_h > max_img_h:
            target_h = max_img_h
            target_w = target_h / aspect
        
        img_rect = fitz.Rect(MARGIN, y, MARGIN + target_w, y + target_h)
        page.insert_image(img_rect, filename=img_path)
        y += target_h + 12

    obs_rect = fitz.Rect(MARGIN + 12, y - 9, MARGIN + CONTENT_WIDTH, y + 40)
    page.insert_text(fitz.Point(MARGIN, y), chr(8226), fontsize=10, fontname="helv", color=(0.1, 0.1, 0.1))
    page.insert_textbox(obs_rect, f"Observation: {observation}", fontsize=9.5, fontname="helv", color=(0.2, 0.2, 0.2))
    y += 42
    return y

# Page 1
page1 = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
y1 = 50
y1 = add_header(page1, y1)
y1 = add_step(page1, y1, 
              step_title="Step 1: The Long-Running Background Process",
              objective="View the source code, run the process in the background using '&', and monitor its active state using 'ps aux'.",
              command="cat task1_alive.c then gcc task1_alive.c -o task1 then ./task1 & then ps aux | grep task1",
              img_filename="01_task1_alive.png",
              observation="The '&' operator launches './task1' in the background with job ID [1] and PID 24810. The 'ps aux' command shows the process running in status 'S' (Interruptible Sleep), waiting on the 1-second sleep() timer.",
              max_img_h=190)

# Page 2
page2 = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
y2 = 50
y2 = add_step(page2, y2,
              step_title="Step 2: Process Identity (PID and PPID)",
              objective="Every process in Linux has a unique Process ID (PID). The process that created it is the Parent Process ID (PPID), usually your terminal shell.",
              command="cat task2_identity.c then gcc task2_identity.c -o task2 then ./task2 & then ps -p 25102 -o pid,ppid,cmd",
              img_filename="02_task2_identity.png",
              observation="The program queries the Linux kernel and prints its unique PID (25102) and parent PPID (19440). The OS ps command confirms that PPID 19440 corresponds directly to the interactive terminal shell session.",
              max_img_h=230)

# Page 3
page3 = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
y3 = 50
y3 = add_step(page3, y3,
              step_title="Step 3: Exit Codes and OS Feedback ($?)",
              objective="When a program finishes, it returns an integer to the OS. 0 means 'Success', and any non-zero number (like 1) means 'Error/Failure'. The shell stores this in $?.",
              command="cat task3_exit.c then gcc task3_exit.c -o task3 then ./task3 then echo $?",
              img_filename="03_task3_exit.png",
              observation="Positive input (5) returns exit code 0 ('Success'). Negative input (-5) returns exit code 1 ('Failure'). The shell captures the return code in the special parameter $?, allowing scripts to determine success or failure.",
              max_img_h=230)

# Page 4
page4 = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
y4 = 50
y4 = add_step(page4, y4,
              step_title="Step 4: Standard I/O Streams (stdin & stdout)",
              objective="The OS provides standard input (stdin, fd 0) and standard output (stdout, fd 1) streams. scanf() reads from stdin, and printf() writes to stdout.",
              command="cat task4_input.c then gcc task4_input.c -o task4 then ./task4",
              img_filename="04_task4_input.png",
              observation="The operating system automatically connects the keyboard to stdin (fd 0), which is parsed by scanf() (\"Bablu\"), and delivers formatted text from printf() to stdout (fd 1) on the terminal display.",
              max_img_h=190)

# Page 5
page5 = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
y5 = 50
y5 = add_step(page5, y5,
              step_title="Step 5: Conditional Execution and Termination",
              objective="Programs often branch based on user input. The OS tracks the final exit code to determine if the script or automation pipeline should continue or halt.",
              command="cat task5_control.c then gcc task5_control.c -o task5 then ./task5 then echo $?",
              img_filename="05_task5_control.png",
              observation="Choosing 1 continues execution, sleeps for 5 seconds, and returns exit code 0 (Success). Choosing 0 aborts execution and returns exit code 1 (Failure). Each run receives a distinct PID allocated by the OS kernel (26780 vs 26795).",
              max_img_h=250)

# Page 6
page6 = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
y6 = 50
y6 = add_step(page6, y6,
              step_title="Step 6: Memory Process Layout (Lecture 2 Integration)",
              objective="Understand how the operating system organizes process virtual memory into Code/Text, Data, BSS, Heap, and Stack segments when loaded via fork() and execve().",
              command="readelf -l binary then cat /proc/self/maps",
              img_filename="06_memory_layout.png",
              observation="The kernel allocates isolated virtual memory pages for the process. Instructions reside in the read-only Code segment (.text), global variables in Data/BSS, dynamic allocations on the Heap, and call frames on the Stack.",
              max_img_h=220)

doc.save(pdf_path)
print(f"Successfully generated exact PDF guide: {pdf_path}")
print(f"Total pages: {len(doc)}")
