---
title: "Virtual Memory Internals: How It Works and Why It Matters"
description: "How memory is used by processors"
publishDate: "16 March 2025"
coverImage:
  src: "./cover.jpg"
  alt: "Image of a Hard Drive"
tags: ["memory", "paging", "riscv","sv32"]
draft: true
---
## Introduction
Hey there! I’m Suraj! Lately, I’ve been working on my own operating system for the RISC-V architecture (more on that in future posts). While implementing virtual memory, I found the **SV32 paging scheme** pretty fascinating. That got me exploring virtual memory a bit more and I wanted to share some of the interesting things I learned along the way!

In this post, we'll break down:
- What **memory** is and how processes use it
- Problems like **fragmentation** and how virtual memory solves them
- How **paging** works and why it’s crucial
- A deep dive into **SV32** paging in RISC-V

---

## What is Memory?
Before diving into virtual memory, let’s understand **what memory is** and **how memory works** in a computer.<br><br>

At the fundamental level, memory serves as an essential hardware component designed to store and retrieve data efficiently. It operates as a structured array of addressable storage units, each capable of holding binary information. This architecture creates a system where the processor can interact with specific locations through unique addresses, much like how we use street addresses to locate specific buildings in a city. <br> <br>
When we consider memory at its most basic function, it acts as a temporary workspace for the computer's operations. The processor constantly reads instructions and data from memory, performs calculations, and writes results back to memory. There are different types of memory which are described below


### **Types of Memory**
- **Registers** – CPU-internal storage locations (32-64 bits) with near-zero latency access, used for immediate operations, addresses and instruction pointers
- **Cache** – Hierarchical SRAM (L1/L2/L3) serving as high-speed buffer between CPU and main memory, operating on temporal/spatial locality principles with access times of 1-60 CPU cycles
- **RAM (Main Memory)** – DRAM-based volatile storage that holds currently executing processes and their working sets, directly addressable through the MMU and organized in pages for virtual memory management(this is what we are concerned with)
- **Disk Storage** – Non-volatile persistence layer with highest capacity and latency
:::note
Disk storage also plays a crucial role in virtual memory systems, particularly in paging, where memory pages are temporarily moved between RAM and disk to optimize usage. While we won't delve deeply into swap space and its management here, we'll explore how paging works and how disk storage comes into play in subsequent articles.
:::

### **How Processes Use Memory**

For a process to run, its data must be loaded into the Main Memory (RAM). This is fundamental to how computers work - the CPU constantly fetches data from memory into its registers to perform calculations and execute instructions. When you're multitasking with applications like Spotify streaming music, Microsoft Word processing your document and Firefox displaying web pages simultaneously, all these programs need some portion of your RAM. We'll take a quick look at logical and virtual addresses too, since they are fundamental to how processes work in the modern age.<br>

When a process runs on your computer, it operates with its **own view of memory** – a simplified, continuous space where it can read and write data. This is what we call the **logical address space**. From the process's perspective, memory appears as a contiguous block beginning at address zero and extending upward.<br><br>
However, these logical addresses don't directly correspond to actual physical locations in your RAM. The **physical address space** represents the actual hardware memory locations in your system. This separation between logical and physical addresses is crucial to modern computing.

The translation from logical to physical addresses is handled by a dedicated hardware component known as the **Memory Management Unit**(MMU). Acting as a bridge between the CPU and memory, the MMU dynamically resolves address mappings using structured translation mechanisms. These mechanisms, which can range from simple direct mappings to more sophisticated paging techniques, determine how logical addresses correspond to physical memory locations. The visualization below provides a high-level view of how logical addresses interact with the MMU to establish mappings within the physical address space.

The visualization below provides a high-level view of how logical addresses interact with the MMU to establish mappings within the physical address space.
![illustration_of_mmu](/mmu.png)

But here's where things get interesting: modern computers often run dozens or even hundreds of processes simultaneously, many of which require substantial memory. We should not forget that RAM is limited (around 16 GB in most systems), so how do we allocate memory to these processes? Let's have a look in the subsequent sections.

---

## Memory Allocation Stratigies
Let us assume that any given moment, we have a list of available block sizes and processes that need to be allocated in the memory.
In general, the memory blocks compromise a set of holes(memory blocks that are avilable for processes) of various sizes that are scattered throughout the memory. When a process arrives and needs memory, the system wlll search the set of holes for one that is large enough for this process. This procedure is an instace of the **general dynamic storage allocation problem**. Let's discuss some of the common solutions to this problem
#### 1. First Fit
This strategy tells to allocate the first hole that is large enough to accomdate the process. Searching will usually start at the beginning of the set of holes. We stop searching once we find the first free hole that is large enough. The below animation demonstrates the First Fit strategy

![gif](/first_fit.gif)

#### 2. Best Fit
Here, we allocate the smallest hole that is big enough for the process. Obviosuly, we need to search the entire list of memory blocks to find the smallest hole, unless the list is ordered by size. This will make sure to produce the smallest leftover hole. The animation below demonstrates the Best Fit strategy

![gif](/best_fit.gif)

#### 3. Worst Fit
Finally, in this strategy we allocate the largest hole that is available in the list. Here too, we should search the entire list. This strategy produces the largest leftover hole. The animation below demonstrates the Worst Fit strategy

![gif](/worst_fit.gif)

As we can see from the above animations these strategies suffers from **external fragmentation**. External fragmentation occurs when processes are loaded and removed from the memory and leave the memory in little broken pieces. External fragmentation exists when there is enough total memory to satisfy the request but the available spaces are not contiguous.

:::note
If it wasn't obvious from the name, there is also a phenomenon called **internal fragmentation**. To keep things simple for now, we'll revisit this topic in a later section.
:::

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