from manim import *

class FirstFitMemoryAllocation(Scene):
    def construct(self):
        # Title
        title = Text("First-Fit Memory Allocation Strategy", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))

        # Initialize memory blocks
        memory_width = 10
        memory_height = 1

        # Create memory representation
        memory = Rectangle(width=memory_width, height=memory_height, color=WHITE)
        memory.move_to(ORIGIN)
        self.play(Create(memory))

        # Initial memory partitions
        partitions = [
            {"size": 2.5, "status": "free", "process": None},
            {"size": 1.5, "status": "allocated", "process": "P1"},
            {"size": 3.0, "status": "free", "process": None},
            {"size": 2.0, "status": "allocated", "process": "P2"},
            {"size": 1.0, "status": "free", "process": None},
        ]

        # Create initial partition visualization
        self.create_memory_visualization(memory, partitions, "Initial Memory State")

        # Process to allocate with First-Fit
        new_process = {"name": "P3", "size": 2.0}

        # Show allocation process
        self.show_first_fit_allocation(memory, partitions, new_process, animate_changes=True)

        # Another allocation
        new_process2 = {"name": "P4", "size": 0.8}
        self.show_first_fit_allocation(memory, partitions, new_process2, animate_changes=True)

        # Create a situation where fragmentation prevents allocation
        # P5 needs 1.5 units of memory - more than any single free block
        # But less than the total free memory (which should be 2.7 units after P3 and P4)
        new_process3 = {"name": "P5", "size": 3.5}
        self.show_first_fit_allocation(memory, partitions, new_process3, animate_changes=True)

        # Calculate total free memory for use in explanation
        total_free = sum(p["size"] for p in partitions if p["status"] == "free")

        # Show fragmentation problem
        fragmentation_title = Text("Memory Fragmentation Problem", font_size=42, color=YELLOW)
        fragmentation_title.to_edge(UP)

        fragmentation_explanation = Text(
            f"Total free memory ({total_free} units) > P5 size (3.5 units)\nBut no single contiguous block is large enough",
            font_size=32,
            color=YELLOW
        )
        fragmentation_explanation.next_to(memory, DOWN, buff=1.5)

        self.play(
            Transform(title, fragmentation_title),
            Write(fragmentation_explanation)
        )
        self.wait(2)

        # Cleanup
        self.play(FadeOut(Group(*self.mobjects)))

        # Conclusion
        conclusion = VGroup(
            Text("First-Fit Strategy:", font_size=42),
            Text("• Allocates to the first free partition that fits", font_size=36),
            Text("• Simple to implement and efficient to execute", font_size=36),
            Text("• Suffers from external fragmentation", font_size=36, color=RED),
            Text("• May waste memory when small processes occupy large chunks", font_size=36)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        self.play(Write(conclusion))
        self.wait(3)

    def create_memory_visualization(self, memory, partitions, label_text):
        # Initial creation of memory visualization
        rectangles_group = VGroup()
        labels_group = VGroup()

        current_x = memory.get_left()[0]
        for partition in partitions:
            width = partition["size"]
            color = RED if partition["status"] == "allocated" else GREEN

            rect = Rectangle(
                width=width,
                height=memory.height,
                color=color,
                fill_opacity=0.5,
                stroke_width=2
            )
            rect.move_to([current_x + width/2, memory.get_center()[1], 0])
            rectangles_group.add(rect)

            # Create label for the partition
            if partition["status"] == "allocated":
                label = Text(partition["process"], font_size=28, color=WHITE)
            else:
                label = Text(f"Free\n{partition['size']}", font_size=24, color=WHITE)

            label.move_to(rect.get_center())
            labels_group.add(label)

            current_x += width

        # Add a label for current state
        state_label = Text(label_text, font_size=32)
        state_label.next_to(memory, DOWN, buff=0.5)

        # Store the visualization objects
        self.memory_rect_group = rectangles_group
        self.memory_label_group = labels_group
        self.state_label = state_label

        # Play animation
        self.play(
            Create(rectangles_group),
            Write(labels_group),
            Write(state_label)
        )
        self.wait(1)

    def update_memory_visualization(self, memory, partitions, label_text, highlight_index=None):
        # Create new visualization
        new_rectangles = VGroup()
        new_labels = VGroup()

        current_x = memory.get_left()[0]
        for i, partition in enumerate(partitions):
            width = partition["size"]
            color = RED if partition["status"] == "allocated" else GREEN
            highlight = i == highlight_index

            rect = Rectangle(
                width=width,
                height=memory.height,
                color=YELLOW if highlight else color,
                fill_opacity=0.5,
                stroke_width=4 if highlight else 2
            )
            rect.move_to([current_x + width/2, memory.get_center()[1], 0])
            new_rectangles.add(rect)

            # Create label for the partition
            if partition["status"] == "allocated":
                label = Text(partition["process"], font_size=28, color=WHITE)
            else:
                label = Text(f"Free\n{partition['size']}", font_size=24, color=WHITE)

            label.move_to(rect.get_center())
            new_labels.add(label)

            current_x += width

        # Update state label
        new_state_label = Text(label_text, font_size=32)
        new_state_label.next_to(memory, DOWN, buff=0.5)

        # Play transform animation
        self.play(
            Transform(self.memory_rect_group, new_rectangles),
            Transform(self.memory_label_group, new_labels),
            Transform(self.state_label, new_state_label)
        )

    def show_first_fit_allocation(self, memory, partitions, new_process, animate_changes=False):
        # Show process information
        process_info = Text(f"Allocating {new_process['name']} ({new_process['size']} units)", font_size=32)
        process_info.to_edge(DOWN)
        self.play(Write(process_info))
        self.wait(1)

        # Create an arrow to point at current partition being checked
        pointer = Arrow(start=LEFT, end=RIGHT, color=YELLOW)
        pointer.scale(0.8)
        pointer.next_to(memory, UP, buff=0.3)
        self.play(Create(pointer))

        # Search for first fit
        current_x = memory.get_left()[0]
        allocated = False

        for i, partition in enumerate(partitions):
            # Move the pointer to this partition
            width = partition["size"]
            new_x = current_x + width/2
            self.play(pointer.animate.next_to(
                [new_x, memory.get_center()[1], 0],
                UP,
                buff=0.3
            ))

            # Check if this partition fits
            if partition["status"] == "free" and partition["size"] >= new_process["size"]:
                # Highlight this partition
                self.update_memory_visualization(memory, partitions,
                    f"Found suitable block at position {i+1} for {new_process['name']}",
                    highlight_index=i)
                self.wait(0.5)

                # Create new partitions - real time allocation
                if partition["size"] > new_process["size"]:
                    # Prepare for split animation
                    remaining_size = partition["size"] - new_process["size"]

                    # Real-time animation of the split
                    if animate_changes:
                        # Update partitions list
                        partitions[i] = {"size": new_process["size"], "status": "allocated", "process": new_process["name"]}
                        partitions.insert(i+1, {"size": remaining_size, "status": "free", "process": None})

                        # Real-time update showing allocation
                        self.update_memory_visualization(memory, partitions,
                            f"Allocated {new_process['name']} and split block (creating {remaining_size} free units)")
                else:
                    # Just allocate the entire partition
                    if animate_changes:
                        partitions[i] = {"size": partition["size"], "status": "allocated", "process": new_process["name"]}

                        # Real-time update showing allocation
                        self.update_memory_visualization(memory, partitions,
                            f"Allocated {new_process['name']} to exact-fit block")

                allocated = True
                break

            current_x += width

        # Clean up
        self.play(FadeOut(pointer), FadeOut(process_info))

        if not allocated:
            # Show message if allocation failed
            total_free = sum(p["size"] for p in partitions if p["status"] == "free")

            # Highlight all free blocks to show fragmentation
            current_x = memory.get_left()[0]
            highlights = VGroup()

            for i, partition in enumerate(partitions):
                if partition["status"] == "free":
                    width = partition["size"]
                    highlight = Rectangle(
                        width=width,
                        height=memory.height,
                        color=BLUE,
                        fill_opacity=0.3,
                        stroke_width=3
                    )
                    highlight.move_to([current_x + width/2, memory.get_center()[1], 0])
                    highlights.add(highlight)
                current_x += width

            self.play(FadeIn(highlights))
            self.wait(1)
            self.play(FadeOut(highlights))

            fail_msg = Text(
                f"Allocation failed: External Fragmentation\nTotal free: {total_free} units, needed: {new_process['size']} units",
                color=RED,
                font_size=32
            )
            fail_msg.to_edge(DOWN)
            self.play(Write(fail_msg))
            self.wait(2)
            self.play(FadeOut(fail_msg))