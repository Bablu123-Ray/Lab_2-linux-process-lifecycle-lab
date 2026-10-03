import os
import base64

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_b64(rel_path):
    full_path = os.path.join(base_dir, rel_path)
    with open(full_path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

img1 = get_b64("assets/screenshots/raw/01_task1_alive.png")
img2 = get_b64("assets/screenshots/raw/02_task2_identity.png")
img3 = get_b64("assets/screenshots/raw/03_task3_exit.png")
img4 = get_b64("assets/screenshots/raw/04_task4_input.png")
img5 = get_b64("assets/screenshots/raw/05_task5_control.png")
img6 = get_b64("assets/screenshots/raw/06_memory_layout.png")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Lab 2: Linux Process Lifecycles &amp; OS Interaction: Step-by-Step Guide</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');
  body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #1f2328;
    background: #ffffff;
    max-width: 900px;
    margin: 40px auto;
    padding: 0 30px;
    line-height: 1.65;
  }}
  h1 {{ font-size: 2.2rem; border-bottom: 2px solid #0969da; padding-bottom: 12px; color: #0969da; margin-bottom: 4px; }}
  h2 {{ font-size: 1.5rem; border-bottom: 1px solid #d0d7de; padding-bottom: 8px; margin-top: 35px; color: #1f2328; }}
  h3 {{ font-size: 1.2rem; margin-top: 25px; color: #24292f; }}
  p, li {{ font-size: 15px; color: #24292f; }}
  code {{ font-family: 'JetBrains Mono', monospace; background: #f6f8fa; padding: 2px 6px; border-radius: 4px; font-size: 13.5px; color: #0969da; }}
  table {{ width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px; }}
  th, td {{ border: 1px solid #d0d7de; padding: 10px 14px; text-align: left; }}
  th {{ background: #f6f8fa; font-weight: 600; }}
  img {{ max-width: 100%; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.15); margin: 15px 0; border: 1px solid #30363d; background: #0c0c0c; }}
  .badge {{ display: inline-block; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; background: #ddf4ff; color: #0969da; margin-right: 8px; }}
  .summary-box {{ background: #f6f8fa; border: 1px solid #d0d7de; border-left: 5px solid #0969da; padding: 16px 20px; border-radius: 6px; margin: 25px 0; }}
  .checklist {{ list-style-type: none; padding-left: 0; }}
  .checklist li::before {{ content: '✔ '; color: #1a7f37; font-weight: bold; }}
  .qa-block {{ background: #f6f8fa; border-left: 4px solid #0969da; padding: 12px 18px; margin-bottom: 16px; border-radius: 0 6px 6px 0; }}
  .qa-q {{ font-weight: 600; color: #1f2328; margin-bottom: 6px; }}
  .qa-a {{ color: #24292f; }}
  @media print {{
    body {{ max-width: 100%; margin: 0; padding: 20px; }}
    img {{ break-inside: avoid; }}
  }}
</style>
</head>
<body>

<h1>Lab 2: Linux Process Lifecycles &amp; OS Interaction: Step-by-Step Guide</h1>
<p><strong>Course:</strong> ST5039CMD Programming and Operating System &bull; <strong>Topic:</strong> Process Layout, Virtual Memory &amp; OS Loading (Lecture 2 &amp; Lab 2)</p>
<div>
  <span class="badge">Linux Kernel</span>
  <span class="badge">POSIX System Calls</span>
  <span class="badge">Memory Layout</span>
  <span class="badge">Exit Status ($?)</span>
</div>

<div class="summary-box">
  <h2 style="margin-top: 0; border-bottom: none; padding-bottom: 0; color: #0969da;">📌 Executive Summary &amp; Lab Summarization (LAB 2)</h2>
  <p>The primary objective of <strong>Lab 2</strong> is to investigate the transition of passive disk executables into active in-memory processes managed by the Linux kernel. A process is an executing program instance with dedicated virtual memory segments, unique Process IDs (PIDs), file descriptors (0, 1, 2), and exit status feedback.</p>
  
  <table>
    <thead>
      <tr>
        <th>Task #</th>
        <th>Task Title</th>
        <th>Core Concept</th>
        <th>Key Commands</th>
        <th>State / Output</th>
        <th>Kernel Mechanism</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Task 1</strong></td>
        <td>Long-Running Process</td>
        <td>Backgrounding (<code>&amp;</code>)</td>
        <td><code>./task1 &amp;</code><br><code>ps aux | grep task1</code></td>
        <td>State <code>S</code> (Sleep)<br>Job ID <code>[1]</code> (PID 24810)</td>
        <td>Frees shell immediately; <code>sleep(1)</code> yields CPU cycles to the scheduler.</td>
      </tr>
      <tr>
        <td><strong>Task 2</strong></td>
        <td>Process Identity</td>
        <td>PID &amp; Parent PPID</td>
        <td><code>./task2 &amp;</code><br><code>ps -p 25102 -o pid,ppid,cmd</code></td>
        <td>PID: <code>25102</code><br>PPID: <code>19440</code></td>
        <td>Kernel tracks task hierarchy; PPID traces back to calling bash shell.</td>
      </tr>
      <tr>
        <td><strong>Task 3</strong></td>
        <td>Exit Status Codes</td>
        <td>Shell Feedback (<code>$?</code>)</td>
        <td><code>./task3</code><br><code>echo $?</code></td>
        <td>Input 5 &rarr; <code>$? = 0</code><br>Input -5 &rarr; <code>$? = 1</code></td>
        <td>Program signals success (0) or error (non-zero) back to host shell via return code.</td>
      </tr>
      <tr>
        <td><strong>Task 4</strong></td>
        <td>Standard I/O Streams</td>
        <td>File Descriptors (0 &amp; 1)</td>
        <td><code>./task4</code></td>
        <td>Input: "Bablu"<br>Output formatted</td>
        <td>Kernel maps <code>stdin</code> (fd 0) to keyboard and <code>stdout</code> (fd 1) to display.</td>
      </tr>
      <tr>
        <td><strong>Task 5</strong></td>
        <td>Conditional Lifecycle</td>
        <td>Branching &amp; Cleanup</td>
        <td><code>./task5</code><br><code>echo $?</code></td>
        <td>Choice 1 &rarr; exit 0<br>Choice 0 &rarr; exit 1</td>
        <td>Demonstrates process memory allocation, execution, and PCB reclamation (26780 vs 26795).</td>
      </tr>
    </tbody>
  </table>
</div>

<hr style="border: none; border-top: 1px solid #d0d7de; margin: 25px 0;">

<h2>II. Architecture Overview: A Process Layout &amp; OS Loading</h2>

<h3>1. Program vs. Process</h3>
<ul>
  <li><strong>Program (File):</strong> An inert, static binary executable residing on disk storage, structured in ELF format.</li>
  <li><strong>Process:</strong> An active instance of a program loaded in system RAM, with dedicated virtual memory mappings, CPU register states, file descriptors, and kernel credentials.</li>
</ul>

<h3>2. Process Memory Layout</h3>
<p>When the kernel creates a process, it establishes a virtual address space partitioned into distinct segments:</p>

<img src="{img6}" alt="Memory Process Layout">

<ul>
  <li><strong>Code/Text Segment:</strong> Executable CPU machine instructions; marked Read-Only/Executable (<code>R-X</code>).</li>
  <li><strong>Data Segment:</strong> Initialized global and static variables loaded directly from the binary.</li>
  <li><strong>BSS Segment (<code>.bss</code>):</strong> Uninitialized global and static variables; zeroed out by the kernel.</li>
  <li><strong>Heap Segment:</strong> Dynamic memory allocated via <code>malloc()</code> / <code>free()</code> (grows upwards).</li>
  <li><strong>Stack Segment:</strong> Function parameters, local variables, and return pointers (grows downwards).</li>
</ul>

<h2>III. Step-by-Step Practical Lab Tasks</h2>

<h3>Task 1: The Long-Running Process</h3>
<ul>
  <li><strong>Objective:</strong> In enterprise servers, processes run for days or months. We must know how to run a process in the background using <code>&amp;</code> and monitor it while it is active using <code>ps aux</code>.</li>
  <li><strong>Command:</strong> <code>cat task1_alive.c then gcc task1_alive.c -o task1 then ./task1 &amp; then ps aux | grep task1</code></li>
  <li><strong>Image Placeholder:</strong></li>
</ul>
<img src="{img1}" alt="Task 1 - Long-Running Process">
<p><strong>Observation:</strong> The <code>&amp;</code> operator executes <code>./task1</code> in the background, freeing the terminal shell immediately with job ID <code>[1]</code> and PID <code>24810</code>. The <code>ps aux</code> command confirms the process is active in state <code>S</code> (Interruptible Sleep), paused during its <code>sleep(1)</code> loop without consuming unnecessary CPU cycles.</p>

<h3>Task 2: Process Identity (PID and PPID)</h3>
<ul>
  <li><strong>Objective:</strong> Every process in Linux has a unique Process ID (<code>PID</code>). The process that created it is the Parent Process ID (<code>PPID</code>), usually your terminal shell. Query these using <code>getpid()</code> and <code>getppid()</code>, and verify them via <code>ps -p 25102 -o pid,ppid,cmd</code>.</li>
  <li><strong>Command:</strong> <code>cat task2_identity.c then gcc task2_identity.c -o task2 then ./task2 &amp; then ps -p 25102 -o pid,ppid,cmd</code></li>
  <li><strong>Image Placeholder:</strong></li>
</ul>
<img src="{img2}" alt="Task 2 - Process Identity">
<p><strong>Observation:</strong> The program queries the Linux kernel and prints its unique <code>PID (25102)</code> and parent <code>PPID (19440)</code>. The OS <code>ps</code> command validates that the PPID <code>19440</code> belongs directly to the interactive terminal shell that spawned the process.</p>

<h3>Task 3: Exit Codes and OS Feedback ($?)</h3>
<ul>
  <li><strong>Objective:</strong> When a program finishes, it returns an integer to the OS. <code>0</code> means "Success", and any non-zero number (like <code>1</code>) means "Error/Failure". The shell stores this in <code>$?</code>.</li>
  <li><strong>Command:</strong> <code>cat task3_exit.c then gcc task3_exit.c -o task3 then ./task3 then echo $?</code></li>
  <li><strong>Image Placeholder:</strong></li>
</ul>
<img src="{img3}" alt="Task 3 - Exit Codes and Feedback">
<p><strong>Observation:</strong> When given a positive input (<code>5</code>), the program returns <code>0</code>, and <code>echo $?</code> outputs <code>0</code> (<strong>Success</strong>). When given a negative input (<code>-5</code>), the program returns <code>1</code>, and <code>echo $?</code> outputs <code>1</code> (<strong>Failure</strong>), proving that Unix processes communicate execution status directly to the calling shell.</p>

<h3>Task 4: Standard I/O Streams</h3>
<ul>
  <li><strong>Objective:</strong> The OS provides standard input (<code>stdin</code>, fd 0) and standard output (<code>stdout</code>, fd 1) streams. <code>scanf()</code> reads from <code>stdin</code>, and <code>printf()</code> writes to <code>stdout</code>.</li>
  <li><strong>Command:</strong> <code>cat task4_input.c then gcc task4_input.c -o task4 then ./task4</code></li>
  <li><strong>Image Placeholder:</strong></li>
</ul>
<img src="{img4}" alt="Task 4 - Standard I/O Streams">
<p><strong>Observation:</strong> The operating system connects the keyboard stream to <code>stdin</code>, which is read by <code>scanf()</code> ("Bablu"), and redirects formatted text from <code>printf()</code> to <code>stdout</code> on the terminal screen ("Hello, Bablu! Welcome to OS Class.").</p>

<h3>Task 5: Conditional Execution and Termination</h3>
<ul>
  <li><strong>Objective:</strong> Programs often branch based on user input. The OS tracks the final exit code to determine if the script or automation pipeline should continue or halt.</li>
  <li><strong>Command:</strong> <code>cat task5_control.c then gcc task5_control.c -o task5 then ./task5 then echo $?</code></li>
  <li><strong>Image Placeholder:</strong></li>
</ul>
<img src="{img5}" alt="Task 5 - Conditional Execution and Termination">
<p><strong>Observation:</strong> Choosing <code>1</code> causes the process to continue, simulate workload (<code>sleep(5)</code>), and return exit code <code>0</code> (<code>Success</code>). Choosing <code>0</code> causes the process to immediately abort and return exit code <code>1</code> (<code>Failure</code>). Each independent run receives a newly allocated PID from the kernel (<code>26780</code> vs <code>26795</code>), illustrating process creation and destruction.</p>

<h2>IV. Lecture 2 Knowledge Test Q&amp;A Reference</h2>
<div class="qa-block"><div class="qa-q">1. What is the difference between source code and an executable?</div><div class="qa-a">Source code is human-readable high-level code (.c). An executable is a machine-readable binary file (.out/ELF) created by a compiler and linker containing CPU instructions and data sections.</div></div>
<div class="qa-block"><div class="qa-q">2. What command compiles a C program?</div><div class="qa-a"><code>gcc program.c -o program</code></div></div>
<div class="qa-block"><div class="qa-q">3. What is a process?</div><div class="qa-a">A process is an active program in execution loaded into main memory (RAM) and managed by the operating system kernel.</div></div>
<div class="qa-block"><div class="qa-q">4. What does the command ./myprogram do?</div><div class="qa-a">It instructs the shell to invoke <code>fork()</code> and <code>execve()</code> system calls, loading the executable into virtual memory and initiating execution at its entry point.</div></div>
<div class="qa-block"><div class="qa-q">5. Why does an OS provide feedback after execution?</div><div class="qa-a">To inform the calling environment (shell or script) whether the process completed successfully (code 0) or encountered an error (non-zero).</div></div>
<div class="qa-block"><div class="qa-q">6. What is a process layout in memory?</div><div class="qa-a">The structural memory mapping allocated by the OS, including Code, Data, BSS, Heap, and Stack segments.</div></div>
<div class="qa-block"><div class="qa-q">7. Name the different sections of memory allocated to a process.</div><div class="qa-a">Stack, Heap, BSS, Data, and Text/Code segments.</div></div>
<div class="qa-block"><div class="qa-q">8. What is stored in the Code/Text section?</div><div class="qa-a">Compiled CPU machine instructions, marked read-only and executable.</div></div>
<div class="qa-block"><div class="qa-q">9. What is stored in the Data section?</div><div class="qa-a">Initialized global and static variables.</div></div>
<div class="qa-block"><div class="qa-q">10. What is stored in the BSS section?</div><div class="qa-a">Uninitialized global and static variables, zero-filled by the OS loader.</div></div>
<div class="qa-block"><div class="qa-q">11. What is the difference between the Stack and the Heap?</div><div class="qa-a">Stack stores automatic local variables and call frames (LIFO, fast, grows down); Heap stores dynamically allocated memory via <code>malloc()</code> (flexible, manually freed, grows up).</div></div>
<div class="qa-block"><div class="qa-q">12. Which direction does the Stack grow in memory?</div><div class="qa-a">Downwards (from high to low virtual addresses).</div></div>
<div class="qa-block"><div class="qa-q">13. Which direction does the Heap grow in memory?</div><div class="qa-a">Upwards (from low to high virtual addresses).</div></div>
<div class="qa-block"><div class="qa-q">14. What happens when the Stack and Heap collide?</div><div class="qa-a">Virtual memory exhaustion occurs, triggering a segmentation fault (<code>SIGSEGV</code>) or stack overflow exception.</div></div>
<div class="qa-block"><div class="qa-q">15. Why are memory sections separated in a process layout?</div><div class="qa-a">For hardware-enforced protection (read-only code), memory conservation, and dynamic scaling of local versus dynamic structures.</div></div>

</body>
</html>
"""

output_path = os.path.join(base_dir, "Lab_2_Process_Lifecycles_Documentation.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated standalone self-contained HTML doc: {output_path}")
print(f"File size: {os.path.getsize(output_path)} bytes")
