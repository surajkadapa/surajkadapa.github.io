---
title: "Virtual Memory Internals: How It Works and Why It Matters"
description: "This post is an example of how to add a cover/2hero image"
publishDate: "16 March 2025"
coverImage:
  src: "./cover2.png"
  alt: "Astro build wallpaper"
tags: ["memory", "paging", "riscv","sv32"]
draft: True
---
## Introduction
Hey there! I'm Suraj, and I've been working on my own operating system for the RISC-V architecture (more on that in future posts). While I was implementing **virtual memory**, I found the **SV32 paging scheme** particularly interesting. This lead me to explore virtual memory on a deeper level and understand it's internals. This post is an attempt to summarize the information I have learned.
In this post, I'll break down:
- What **memory** is and how processes use it
- Problems like **fragmentation** and how virtual memory solves them
- How **paging** works and why it’s crucial
- A deep dive into **SV32** paging in **RISC-V**

---

## What is Memory?
Before diving into virtual memory, let’s understand **what memory is** and **how memory works** in a computer.



### **Types of Memory:**
- **Registers** – Small, super-fast, used for CPU operations
- **Cache** – L1/L2/L3 caches to reduce memory access latency
- **RAM (Main Memory)** – Where processes run, faster than disk(this is what we are concerned with)
- **Disk Storage** – Used for swap space when RAM is full

### **How Processes Use Memory**
A process typically has:
- **Code Segment** – Stores executable code
- **Heap** – Dynamic memory (malloc/new)
- **Stack** – Stores function calls, local variables

**Problem:** **Physical memory is limited**, and processes need **isolation**.

---

## 2️⃣ The Problem: Fragmentation & Memory Management
When processes allocate and free memory, **fragmentation** happens:

### **Types of Fragmentation**
- **External Fragmentation** – Free memory exists, but is **scattered**
- **Internal Fragmentation** – Memory is allocated in fixed blocks, leading to waste

### **Solution: Virtual Memory**
Instead of giving processes **direct physical memory**, the OS provides a **virtual address space**, mapped to physical memory dynamically.

---

## 3️⃣ Virtual Memory & Paging
### **What is Virtual Memory?**
A technique that gives each process an **isolated memory space** while allowing more processes to run than available RAM.

### **Paging: How It Works**
Instead of allocating **one large contiguous memory block**, the OS divides memory into:
- **Pages** – Fixed-size chunks in virtual memory (e.g., 4KB)
- **Page Frames** – Corresponding chunks in physical memory

#### **Page Table & Address Translation**
The OS maintains **page tables** to map **virtual pages → physical frames**.
✅ **Benefit:** No fragmentation, easier memory allocation

📌 **Concepts:**
- **TLB (Translation Lookaside Buffer):** Cache for fast page table lookups
- **Page Faults:** Happens when a required page is **not in RAM**

---

## 4️⃣ RISC-V SV32: Paging in Action
### **What is SV32?**
**SV32 (Supervisor Virtual Memory, 32-bit)** is the paging scheme used in **RISC-V** for **32-bit systems**.

### **SV32 Page Table Structure**
SV32 uses **two-level paging**, meaning:
- A **virtual address (VA)** is divided into:
  - **VPN1** (First-level page table index)
  - **VPN0** (Second-level page table index)
  - **Offset** (Offset inside the page)

#### **How SV32 Translates Addresses:**
1. **VPN1** indexes the **root page table** → points to a **second-level table**
2. **VPN0** indexes the **second-level page table** → points to a **physical frame**
3. **Offset** is added to the **physical frame address** to get the final **physical address**

✍ **Example Diagram:**
*(Insert a visual representation of SV32 address translation here)*

### **Advantages of SV32**
- Efficient for **32-bit** systems
- Two-level hierarchy keeps page tables small
- Supports **permissions (RWX)** and memory protection

---

## 5️⃣ Wrapping Up (And What’s Next)
So far, we've explored:
✅ **Why virtual memory is needed**
✅ **How paging solves fragmentation issues**
✅ **How SV32 works in RISC-V**

I implemented SV32 while building my **own RISC-V OS**, and I’ll be sharing more details in upcoming blog posts! Stay tuned for deeper dives into **kernel memory management, process isolation, and implementing paging in an OS**.

Got questions or feedback? Let’s discuss in the comments! 🚀