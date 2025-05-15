import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re
from PyPDF2 import PdfReader

# ---------------- OS Concepts Simulation -------------------

# 1. CPU Scheduling: FCFS and SJF (based on file size)
class Scheduler:
    def __init__(self):
        self.queue = []

    def add_resume(self, filepath):
        size = os.path.getsize(filepath)
        self.queue.append((filepath, size))

    def schedule_fcfs(self):
        return self.queue

    def schedule_sjf(self):
        return sorted(self.queue, key=lambda x: x[1])

# 2. Memory Allocation - Fixed Partition Simulation
PARTITION_SIZE = 5000  # characters

def allocate_memory_for_resume(text):
    if len(text) > PARTITION_SIZE:
        return "Memory Overflow: Resume too large"
    return "Resume fits in memory"

# 3. File Allocation - Indexed Allocation Simulation
def simulate_indexed_allocation(text):
    lines = text.split('\n')
    index_block = {i: line.strip() for i, line in enumerate(lines) if line.strip()}
    return index_block

# 4. Page Replacement Algorithm - LRU Simulation
class PageTable:
    def __init__(self, capacity):
        self.capacity = capacity
        self.pages = {}

    def access_page(self, resume_id):
        if resume_id in self.pages:
            # Move accessed page to the end to show recent use (simulate LRU)
            self.pages.pop(resume_id)
            self.pages[resume_id] = True
        else:
            if len(self.pages) >= self.capacity:
                # Remove least recently used page (first inserted)
                self.pages.pop(next(iter(self.pages)))
            self.pages[resume_id] = True
        return list(self.pages.keys())

# 5. Frame Allocation - Proportional Allocation
def allocate_frames(resume_sizes, total_frames):
    total_size = sum(resume_sizes)
    frame_allocation = [int((size / total_size) * total_frames) if total_size > 0 else 0 for size in resume_sizes]
    return frame_allocation

# ---------------- Resume Evaluation & Scoring -------------------
def evaluate_resume(text):
    score = 0
    criteria = {
        "education": r"(bachelor|master|phd|b\.tech|bsc|msc|mca|mba)",
        "experience": r"(\d+\s+years?\s+experience|internship)",
        "skills": r"(python|java|sql|c\+\+|machine learning|data analysis)",
        "projects": r"projects?",
        "certifications": r"certifications?"
    }

    matched = {}
    for key, pattern in criteria.items():
        if re.search(pattern, text, re.IGNORECASE):
            matched[key] = True
            score += 20
        else:
            matched[key] = False

    rating = "Poor"
    if score >= 80:
        rating = "Excellent"
    elif score >= 60:
        rating = "Good"
    elif score >= 40:
        rating = "Average"

    return score, rating, matched

# Utility function to read text from resume file (PDF or TXT)
def read_resume_text(filepath):
    if filepath.lower().endswith('.txt'):
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    elif filepath.lower().endswith('.pdf'):
        try:
            reader = PdfReader(filepath)
            return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
    else:
        return "Unsupported file format. Use .txt or .pdf"

# ---------------- GUI -------------------
class ResumeAnalyzerApp:
    def __init__(self, master):
        self.master = master
        master.title("Resume Analyzer with OS Concepts")
        master.geometry("800x700")
        master.configure(bg="#f4f4f4")

        self.scheduler = Scheduler()
        self.resumes = []
        self.page_table = PageTable(capacity=3)

        self.label = tk.Label(master, text="Upload Resumes", font=("Arial", 16, "bold"), bg="#f4f4f4")
        self.label.pack(pady=10)

        self.upload_button = tk.Button(master, text="Upload Resume", font=("Arial", 12), bg="#4caf50", fg="white", command=self.upload_resume)
        self.upload_button.pack(pady=5)

        self.analyze_button = tk.Button(master, text="Analyze Resumes (SJF)", font=("Arial", 12), bg="#2196f3", fg="white", command=self.analyze_resumes)
        self.analyze_button.pack(pady=5)

        self.compare_button = tk.Button(master, text="Compare Resumes", font=("Arial", 12), bg="#f44336", fg="white", command=self.compare_resumes)
        self.compare_button.pack(pady=5)

        self.output = tk.Text(master, height=30, width=95, font=("Consolas", 10))
        self.output.pack(pady=10)

    def upload_resume(self):
        filepath = filedialog.askopenfilename(filetypes=[("PDF files", ".pdf"), ("Text files", ".txt")])
        if filepath:
            self.scheduler.add_resume(filepath)
            self.resumes.append(filepath)
            self.output.insert(tk.END, f"Uploaded: {os.path.basename(filepath)}\n")

    def analyze_resumes(self):
        if not self.resumes:
            messagebox.showerror("Error", "Please upload at least one resume first.")
            return

        scheduled = self.scheduler.schedule_sjf()
        resume_sizes = [size for (_, size) in scheduled]
        frames = allocate_frames(resume_sizes, total_frames=100)

        self.output.insert(tk.END, "\n--- Analyzing Resumes ---\n")

        for idx, (filepath, size) in enumerate(scheduled):
            text = read_resume_text(filepath)

            # Memory Allocation Check
            memory_msg = allocate_memory_for_resume(text)

            # File Allocation Simulation
            index_block = simulate_indexed_allocation(text)

            # Page Replacement Simulation
            resume_id = os.path.basename(filepath)
            current_pages = self.page_table.access_page(resume_id)

            # Resume Scoring
            score, rating, matched = evaluate_resume(text)

            self.output.insert(tk.END, f"\n>> {resume_id} ({size} bytes)\n")
            self.output.insert(tk.END, f"Frames Allocated: {frames[idx]}\n")
            self.output.insert(tk.END, f"Memory Status: {memory_msg}\n")
            self.output.insert(tk.END, f"Indexed Blocks: {list(index_block.keys())[:5]}...\n")
            self.output.insert(tk.END, f"Active Pages (LRU): {current_pages}\n")
            self.output.insert(tk.END, f"Resume Score: {score}/100\n")
            self.output.insert(tk.END, f"Rating: {rating}\n")
            self.output.insert(tk.END, f"Matched Sections: {', '.join([k for k,v in matched.items() if v])}\n")

    def compare_resumes(self):
        if len(self.resumes) < 2:
            messagebox.showerror("Error", "Please upload at least two resumes to compare.")
            return
        
        text1 = read_resume_text(self.resumes[0])
        text2 = read_resume_text(self.resumes[1])
        
        comparison = self.compare_resumes_effectiveness(text1, text2)
        
        self.output.insert(tk.END, "\n--- Effectiveness Comparison ---\n")
        self.output.insert(tk.END, f"Resume 1 Effectiveness Score: {comparison['Resume 1 Score']}\n")
        self.output.insert(tk.END, f"Resume 2 Effectiveness Score: {comparison['Resume 2 Score']}\n")
        self.output.insert(tk.END, f"Similarity Score: {comparison['Effectiveness Similarity']:.2f}%\n")

    def compare_resumes_effectiveness(self, text1, text2):
        score1, _, _ = evaluate_resume(text1)
        score2, _, _ = evaluate_resume(text2)

        if score1 == 0 or score2 == 0:
            similarity = 0  # If any resume has 0 score, set similarity to 0%
        else:
            similarity = (min(score1, score2) / max(score1, score2)) * 100
        
        comparison = {
            "Resume 1 Score": score1,
            "Resume 2 Score": score2,
            "Effectiveness Similarity": similarity
        }
        return comparison


# ---------------- Main -------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ResumeAnalyzerApp(root)
    root.mainloop()
