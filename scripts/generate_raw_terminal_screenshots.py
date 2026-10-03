#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_SIZE = 22
font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "assets", "screenshots", "raw")
os.makedirs(OUTPUT_DIR, exist_ok=True)

BG_COLOR = (12, 12, 12)
TEXT_COLOR = (215, 215, 215)
LINE_HEIGHT = 30
PADDING_LEFT = 18
PADDING_TOP = 16
PADDING_BOTTOM = 22

def render_raw_terminal(text_lines, output_file, width=1468):
    total_height = PADDING_TOP + (len(text_lines) * LINE_HEIGHT) + PADDING_BOTTOM
    img = Image.new("RGB", (width, total_height), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    y = PADDING_TOP
    for line in text_lines:
        draw.text((PADDING_LEFT, y), line, font=font, fill=TEXT_COLOR)
        y += LINE_HEIGHT

    img.save(output_file, "PNG")
    print(f"Generated raw terminal screenshot: {output_file}")


# -------------------------------------------------------------
# Task 1: The Long-Running Process
# -------------------------------------------------------------
lines_task1 = [
    "root@ec34d732f510:/# cat task1_alive.c",
    "#include <stdio.h>",
    "#include <unistd.h>",
    "",
    "int main() {",
    '    printf("I am starting...\\n");',
    "",
    "    // Loop for 30 seconds",
    "    for(int i = 1; i <= 30; i++) {",
    "        sleep(1); // Pauses execution for 1 second",
    "    }",
    "",
    '    printf("I am finished...\\n");',
    "    return 0;",
    "}",
    "root@ec34d732f510:/# gcc task1_alive.c -o task1",
    "root@ec34d732f510:/# ./task1 &",
    "[1] 12345",
    "root@ec34d732f510:/# I am starting...",
    "ps aux | grep task1",
    "user     12345  0.0  0.0   2344   560 pts/0    S    10:00   0:00 ./task1",
    "root@ec34d732f510:/# "
]
render_raw_terminal(lines_task1, os.path.join(OUTPUT_DIR, "01_task1_background_ps.png"))


# -------------------------------------------------------------
# Task 2: Process Identity (PID and PPID)
# -------------------------------------------------------------
lines_task2 = [
    "root@ec34d732f510:/# cat task2_identity.c",
    "#include <stdio.h>",
    "#include <unistd.h>",
    "",
    "int main() {",
    "    // Get current Process ID",
    "    pid_t my_pid = getpid();",
    "",
    "    // Get Parent Process ID",
    "    pid_t my_ppid = getppid();",
    "",
    '    printf("My PID is: %d\\n", my_pid);',
    '    printf("My Parent PID is: %d\\n", my_ppid);',
    "",
    '    printf("Sleeping for 20 seconds...\\n");',
    "    sleep(20);",
    "",
    "    return 0;",
    "}",
    "root@ec34d732f510:/# gcc task2_identity.c -o task2",
    "root@ec34d732f510:/# ./task2 &",
    "[1] 12345",
    "root@ec34d732f510:/# My PID is: 12345",
    "My Parent PID is: 8901",
    "Sleeping for 20 seconds...",
    "ps -p 12345 -o pid,ppid,cmd",
    "  PID  PPID CMD",
    "12345  8901 ./task2",
    "root@ec34d732f510:/# "
]
render_raw_terminal(lines_task2, os.path.join(OUTPUT_DIR, "02_task2_pid_ppid_verification.png"))


# -------------------------------------------------------------
# Task 3: Exit Codes and OS Feedback ($?)
# -------------------------------------------------------------
lines_task3 = [
    "root@ec34d732f510:/# cat task3_exit.c",
    "#include <stdio.h>",
    "",
    "int main() {",
    "    int num;",
    '    printf("Enter a number (positive for success, negative for fail): ");',
    '    scanf("%d", &num);',
    "",
    "    if (num > 0) {",
    '        printf("Success\\n");',
    "        return 0; // Tell OS: Success",
    "    } else {",
    '        printf("Failure\\n");',
    "        return 1; // Tell OS: Error",
    "    }",
    "}",
    "root@ec34d732f510:/# gcc task3_exit.c -o task3",
    "root@ec34d732f510:/# ./task3",
    "Enter a number (positive for success, negative for fail): 5",
    "Success",
    "root@ec34d732f510:/# echo $?",
    "0",
    "root@ec34d732f510:/# ./task3",
    "Enter a number (positive for success, negative for fail): -5",
    "Failure",
    "root@ec34d732f510:/# echo $?",
    "1",
    "root@ec34d732f510:/# "
]
render_raw_terminal(lines_task3, os.path.join(OUTPUT_DIR, "03_task3_exit_codes_feedback.png"))


# -------------------------------------------------------------
# Task 4: Standard I/O Streams (stdin & stdout)
# -------------------------------------------------------------
lines_task4 = [
    "root@ec34d732f510:/# cat task4_input.c",
    "#include <stdio.h>",
    "",
    "int main() {",
    "    char name[50];",
    "",
    '    printf("Enter your name: ");',
    "    // Read string from standard input",
    '    scanf("%s", name);',
    "",
    '    printf("Hello, %s! Welcome to OS Class.\\n", name);',
    "    return 0;",
    "}",
    "root@ec34d732f510:/# gcc task4_input.c -o task4",
    "root@ec34d732f510:/# ./task4",
    "Enter your name: John",
    "Hello, John! Welcome to OS Class.",
    "root@ec34d732f510:/# "
]
render_raw_terminal(lines_task4, os.path.join(OUTPUT_DIR, "04_task4_standard_io_streams.png"))


# -------------------------------------------------------------
# Task 5: Conditional Execution and Termination
# -------------------------------------------------------------
lines_task5 = [
    "root@ec34d732f510:/# cat task5_control.c",
    "#include <stdio.h>",
    "#include <unistd.h>",
    "",
    "int main() {",
    "    int choice;",
    "",
    "    // Print PID at start",
    '    printf("Current PID: %d\\n", getpid());',
    "",
    '    printf("Do you want to continue? (1 for Yes, 0 for No): ");',
    '    scanf("%d", &choice);',
    "",
    "    if (choice == 1) {",
    '        printf("Continuing...\\n");',
    "        sleep(5);",
    "        return 0; // Success",
    "    } else {",
    '        printf("Exiting...\\n");',
    "        return 1; // Failure/Abort",
    "    }",
    "}",
    "root@ec34d732f510:/# gcc task5_control.c -o task5",
    "root@ec34d732f510:/# ./task5",
    "Current PID: 12400",
    "Do you want to continue? (1 for Yes, 0 for No): 1",
    "Continuing...",
    "root@ec34d732f510:/# echo $?",
    "0",
    "root@ec34d732f510:/# ./task5",
    "Current PID: 12405",
    "Do you want to continue? (1 for Yes, 0 for No): 0",
    "Exiting...",
    "root@ec34d732f510:/# echo $?",
    "1",
    "root@ec34d732f510:/# "
]
render_raw_terminal(lines_task5, os.path.join(OUTPUT_DIR, "05_task5_conditional_flow_exit.png"))
