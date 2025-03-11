from manim import *

class BestFitMemoryAllocation(Scene):
    def construct(self):
        # Title
        title = Text("Best-Fit Memory Allocation Strategy", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))

        # Initialize memory blocks
        memory_width = 10
        memory_height = 1

        # Create memory representation
        memory = Rectangle(width=memory_width, height=memory_height, color=WHITE)
        memory.move_to(ORIGIN)
        self.play(Create(memory))

        # Initial memory partitions - using exact values to avoid floating point issues
        partitions = [
            {"size": 2.5, "status": "free", "process": None},
            {"size": 1.5, "status": "allocated", "process": "P1"},
            {"size": 3.0, "status": "free", "process": None},
            {"size": 2.0, "status": "allocated", "process": "P2"},
            {"size": 1.0, "status": "free", "process": None},
        ]

        # Create initial partition visualization with a fixed initial label
        # This fixes the issue with the unwanted text at the start
        self.create_memory_visualization(memory, partitions, "Initial Memory State")

        # Process to allocate with Best-Fit
        new_process = {"name": "P3", "size": 2.0}

        # Show allocation process
        self.show_best_fit_allocation(memory, partitions, new_process, animate_changes=True)

        # Another allocation
        new_process2 = {"name": "P4", "size": 0.8}
        self.show_best_fit_allocation(memory, partitions, new_process2, animate_changes=True)

        # External fragmentation demonstration
        new_process3 = {"name": "P5", "size": 3.5}
        self.show_best_fit_allocation(memory, partitions, new_process3, animate_changes=True)

        # Cleanup
        self.play(FadeOut(Group(*self.mobjects)))

        # Conclusion - fixed spacing and layout to prevent overlap
        conclusion_items = [
            Text("Best-Fit Strategy:", font_size=42),
            Text("• Finds the smallest free partition that fits", font_size=34),
            Text("• Minimizes wasted memory within allocations", font_size=34),
            Text("• Suffers from external fragmentation", font_size=34, color=RED),
            Text("• Can increase allocation time due to scanning", font_size=34)
        ]
        
        conclusion = VGroup(*conclusion_items)
        conclusion.arrange(DOWN, aligned_edge=LEFT, buff=0.4)  # Increased buff for more space
        conclusion.to_edge(LEFT, buff=1)  # Add left margin
        
        self.play(Write(conclusion))
        self.wait(3)

    def show_best_fit_allocation(self, memory, partitions, new_process, animate_changes=False):
        process_info = Text(f"Allocating {new_process['name']} ({new_process['size']} units)", font_size=32)
        process_info.to_edge(DOWN)
        self.play(Write(process_info))
        self.wait(1)

        pointer = Arrow(start=LEFT, end=RIGHT, color=YELLOW)
        pointer.scale(0.8)
        pointer.next_to(memory, UP, buff=0.3)
        self.play(Create(pointer))

        # Best-Fit Search: Find the smallest free block that fits
        best_index = None
        best_size = float('inf')  # This is okay since we're just comparing, not displaying
        current_x = memory.get_left()[0]

        for i, partition in enumerate(partitions):
            width = partition["size"]
            new_x = current_x + width / 2
            self.play(pointer.animate.next_to([new_x, memory.get_center()[1], 0], UP, buff=0.3))

            if partition["status"] == "free" and partition["size"] >= new_process["size"]:
                if partition["size"] < best_size:
                    best_size = partition["size"]
                    best_index = i

            current_x += width

        if best_index is not None:
            self.update_memory_visualization(memory, partitions,
                f"Best block found at position {best_index+1} for {new_process['name']}",
                highlight_index=best_index)
            self.wait(0.5)

            # Allocation with split if necessary
            if partitions[best_index]["size"] > new_process["size"]:
                # Fix: Use round to avoid floating point issues
                remaining_size = round(partitions[best_index]["size"] - new_process["size"], 1)

                if animate_changes:
                    partitions[best_index] = {"size": new_process["size"], "status": "allocated", "process": new_process["name"]}
                    partitions.insert(best_index + 1, {"size": remaining_size, "status": "free", "process": None})

                    self.update_memory_visualization(memory, partitions,
                        f"Allocated {new_process['name']} and split block (remaining {remaining_size} free units)")
            else:
                if animate_changes:
                    partitions[best_index] = {"size": partitions[best_index]["size"], "status": "allocated", "process": new_process["name"]}

                    self.update_memory_visualization(memory, partitions,
                        f"Allocated {new_process['name']} to exact-fit block")
        else:
            # IMPORTANT FIX: Fade out the process_info before showing the fragmentation issue
            # This prevents the "Allocating P5" text from overlapping with the "Allocation Failed" message
            self.play(FadeOut(process_info))
            self.show_fragmentation_issue(memory, partitions, new_process)
            # Only fade out the pointer since process_info is already gone
            self.play(FadeOut(pointer))
            return

        self.play(FadeOut(pointer), FadeOut(process_info))

    def show_fragmentation_issue(self, memory, partitions, new_process):
        # Fix: Round the sum to avoid floating point issues
        total_free = round(sum(p["size"] for p in partitions if p["status"] == "free"), 1)
        highlights = VGroup()
        current_x = memory.get_left()[0]

        for partition in partitions:
            if partition["status"] == "free":
                width = partition["size"]
                highlight = Rectangle(
                    width=width, height=memory.height, color=BLUE,
                    fill_opacity=0.3, stroke_width=3
                )
                highlight.move_to([current_x + width/2, memory.get_center()[1], 0])
                highlights.add(highlight)
            current_x += partition["size"]

        self.play(FadeIn(highlights))
        self.wait(1)
        self.play(FadeOut(highlights))

        # Split into two lines for better readability
        fail_msg = VGroup(
            Text(f"Allocation failed: External Fragmentation", color=RED, font_size=32),
            Text(f"Total free: {total_free} units, needed: {new_process['size']} units", color=RED, font_size=32)
        ).arrange(DOWN)
        fail_msg.to_edge(DOWN)
        self.play(Write(fail_msg))
        self.wait(2)
        self.play(FadeOut(fail_msg))

    def create_memory_visualization(self, memory, partitions, label_text):
        rectangles_group = VGroup()
        labels_group = VGroup()
        current_x = memory.get_left()[0]

        for partition in partitions:
            width = partition["size"]
            color = RED if partition["status"] == "allocated" else GREEN

            rect = Rectangle(
                width=width, height=memory.height, color=color,
                fill_opacity=0.5, stroke_width=2
            )
            rect.move_to([current_x + width/2, memory.get_center()[1], 0])
            rectangles_group.add(rect)

            # Keep the original format for the memory block labels
            size_text = f"{partition['size']:.1f}" if partition["status"] == "free" else ""
            block_label_text = partition["process"] if partition["status"] == "allocated" else f"Free\n{size_text}"
            
            label = Text(block_label_text, font_size=24, color=WHITE)
            label.move_to(rect.get_center())
            labels_group.add(label)

            current_x += width

        # Create a fixed label below the memory to avoid any unwanted text
        state_label = Text(label_text, font_size=32)
        state_label.next_to(memory, DOWN, buff=0.5)
        self.memory_rect_group = rectangles_group
        self.memory_label_group = labels_group
        self.state_label = state_label

        self.play(Create(rectangles_group), Write(labels_group), Write(state_label))
        self.wait(1)

    def update_memory_visualization(self, memory, partitions, label_text, highlight_index=None):
        new_rectangles = VGroup()
        new_labels = VGroup()
        current_x = memory.get_left()[0]

        for i, partition in enumerate(partitions):
            width = partition["size"]
            color = RED if partition["status"] == "allocated" else GREEN
            highlight = i == highlight_index

            rect = Rectangle(
                width=width, height=memory.height, color=YELLOW if highlight else color,
                fill_opacity=0.5, stroke_width=4 if highlight else 2
            )
            rect.move_to([current_x + width/2, memory.get_center()[1], 0])
            new_rectangles.add(rect)

            # Keep consistent formatting for memory block labels
            size_text = f"{partition['size']:.1f}" if partition["status"] == "free" else ""
            label_text_content = partition["process"] if partition["status"] == "allocated" else f"Free\n{size_text}"
            
            label = Text(label_text_content, font_size=24, color=WHITE)
            label.move_to(rect.get_center())
            new_labels.add(label)

            current_x += width

        new_state_label = Text(label_text, font_size=32)
        new_state_label.next_to(memory, DOWN, buff=0.5)

        self.play(Transform(self.memory_rect_group, new_rectangles),
                  Transform(self.memory_label_group, new_labels),
                  Transform(self.state_label, new_state_label))