---
title: "Getting Placed and My University Expereience"
description: "My journey through campus placements"
publishDate: "19 September 2025" 
tags: ["placements", "personal"]
---


## Starting my blog
I’ve been meaning to start a blog for a while now. There’s always been this itch to put my thoughts down - about systems, my projects, and the rollercoaster of being a final-year student chasing after placements and a role I truly enjoy. I couldn’t think of a better way to begin than by sharing one of the biggest moments of my college life so far: getting placed.

In this post, I’ll talk about my journey through college - the grind, the constant shifts in interest, the rejections along the way, and finally, the plot twist at the end (you’ll want to stay for that!).

## New Beginnings
After finishing high school, I joined my undergrad majoring in Computer Science. Funny thing is, I initially wanted to go for Electronics and Communications, but the job market for those roles wasn’t looking too bright in my country. Since I already had a decent interest in Arduinos and writing code for them, I figured CS was the safer bet - or so I thought.

The first two semesters were a completely new experience. I suddenly had the freedom to explore what I wanted, but the curriculum still forced me into physics and chemistry (I’m still not sure how exactly they’re supposed to help me… maybe the connection will click one day). Around this time, I picked up C, got into low-level engineering, and started exploring reverse-engineering challenges (shout out to picoCTF). That’s when I discovered how much I enjoyed taking things apart just to see how they worked under the hood.

This was also when I entered my first hackathon. We got a crash course on Flutter and Figma, and then had 36 hours to build an app from scratch. I had zero experience with Flutter or Dart (and this was back in 2022, before ChatGPT blew up). My team and I scraped tutorials off YouTube and managed to make a simple app that took ingredients from your kitchen and suggested recipes. Honestly, it was more pretty UI than solid engineering, but for first-semester students without AI copilots, it was something. To our surprise, we ended up winning Best Implementation.

That day I learnt something important about myself: I work best under pressure. When there’s a hard deadline and something real at stake, I give it everything. It’s not a trait I’m especially proud of, but it’s shaped a lot of my college journey - sometimes successfully, sometimes not - as I kept trying to build discipline without external pressure.


## Finding My Groove in CS

By the time I entered my 3rd semester, things started to feel serious. Seniors used to say, “this is where the real CS begins” - and they were right. I still remember the first time I implemented a linked list in pure C. It was like pulling back a curtain and realizing how much magic was hiding under the hood. For the first time, I wasn’t just using data structures - I was building them. That single experience lit a spark: I wanted to go deeper into low-level programming and see how everything actually worked.

Most of my 3rd and 4th semester was spent buried in textbooks on Operating Systems and Database Management Systems, and binge-watching lectures from other universities on YouTube. I wasn’t just studying for grades anymore - I was genuinely curious, and I wanted to absorb as much as possible.

In my 5th semester, I picked an elective called Big Data, and it completely changed the way I looked at storage. Until then, I hadn’t really thought about where large volumes of data lived or how they were managed. Learning about the Hadoop Distributed File System (HDFS) sent me down a rabbit hole into filesystems and the unique challenges of distributed environments.

But it was 6th semester that truly cemented my path. Two courses shaped everything:

1. Heterogeneous Parallelism - where I learned about CPU pipelines, cache coherence, and how different processing units could work together on the same program. It was my first real taste of computer architecture and performance engineering, and I couldn’t get enough.

2. Cloud Computing - where we explored virtualization, scalability, and the gnarly problems that arise in modern cloud systems. What fascinated me wasn’t just the problems, but how elegant some of the solutions were.

By the end of that year, I knew what I wanted to chase: distributed systems and performance engineering. And just as I was starting to feel like I’d found my groove, the biggest challenge of my undergrad life appeared on the horizon: placements.

## Placements

For those outside India: placements (or on-campus recruiting) are when companies visit universities, conduct tests (usually LeetCode-style coding questions plus some OS/DBMS MCQs), and then interview shortlisted students. If you survive the whole gauntlet, you get the offer.

One company I had my eye on from the very beginning was Couchbase. They build distributed systems and their own database engine, basically the stuff I love. Unlike many companies, their hiring process is more personal: they don’t rely only on test scores. Instead, they manually go through resumes and call students who show strong fundamentals, demonstrated by projects, GPA, or past internships.

Here’s the catch: I had zero internships. My strength was projects, textbooks, and a decent handle on LeetCode. To my relief, I still got the interview call.

### Preparing for Couchbase

I spent the days before revising core CS, walking through my projects’ source code, and brushing up concurrency concepts - mutexes, atomics, multithreading. This was my first serious interview, so the nerves were very real.

#### Round 1

The interviewer welcomed me warmly, which calmed me a little. He was an alum of my university, so we started chatting about campus life. Then the real test began:

1. Why is count++ not thread-safe?

I explained the read-modify-write breakdown and talked about mutexes and atomics. When I mentioned compare-and-swap, he seemed impressed and asked me to dive deeper.

2. Given an array of billions of integers, how do you sum them on a multicore system?

I suggested splitting work equally, but he pushed me to think about load balancing. I eventually landed on batching, which was the optimal approach. I got nervous while coding the indices, but he guided me, and we got there.

It was a great discussion, but I knew my nerves showed.

#### Round 2

This round focused heavily on my projects. He grilled me on my shared-memory key-value store, how I prevented race conditions, how I designed concurrency. I explained with diagrams, and he seemed satisfied.

Then came an interesting one:

1. If you have a cache between a user and an e-commerce site like Amazon, what’s the best cache eviction policy?

I started with LRU, but he challenged me with a “fire sale” scenario where every item is popular. That forced me to think deeper. I proposed a windowed approach that blends frequency with recency, and he liked it.

2. Design a multi-threaded search in a binary tree.

I misunderstood “binary tree” as “BST” at first, but quickly corrected. I proposed spawning threads for subtrees carefully, checking a global flag for early exits, and coded it up.

This time I came out feeling okay, but not 100% sure.

#### Round 3

By now I was running on nothing but coffee and nerves, it had been almost 6 to 7 hours since I had anything to eat. The interviewer asked me to briefly explain my projects and my teaching assistant role for Big Data. Then he asked:

1. Simulate a deadlock in C++.

My mind blanked. Completely. For a few seconds, I thought it was over. Then he nudged me: “Don’t you think we need to acquire something first?” That brought me back. I wrote code with two threads and two mutexes acquiring in opposite order, then explained solutions like ordering locks. He seemed satisfied.

I waited anxiously for results. Then it came: **Rejected**.

### Rejection

The walk back home was brutal. My mind kept replaying the interviews, the hesitation in R1, the overthinking in R2, the freeze in R3. Maybe it was speed? Maybe my lack of internships? Maybe just nerves? Too many variables, no clear answers.

I gave myself two days off, then got back to tests, LeetCode, and brushing my fundamentals. I told myself the Couchbase chapter was over.

### The Twist

A month later, my placement coordinator called me out of the blue:

:::note[Placement Officer]
“Couchbase has come back to campus. They want to hire you. Do you want to take it?”
:::

I thought I misheard. I asked him to repeat it. When it sunk in, I said yes immediately  and probably scared the neighbors with how much I jumped around.

That evening, HR called to confirm the details, and soon after, the official internship offer letter landed in my inbox. The cherry on top: Couchbase told me they have a historical 100% conversion rate for interns to full-time.

After weeks of rejection, doubt, and what-ifs… the company I wanted most came back for me.