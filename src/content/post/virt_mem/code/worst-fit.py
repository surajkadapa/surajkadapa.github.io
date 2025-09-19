from manim import *

class WorstFitMemoryAllocation(Scene):
    def construct(self):
        # Title
        title = Text("Worst-Fit Memory Allocation Strategy", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))

        # Memory representation
        memory_width = 10
        memory_height = 1
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

        self.create_memory_visualization(memory, partitions, "Initial Memory State")

        # Processes to allocate using Worst-Fit
        processes = [
            {"name": "P3", "size": 2.0},
            {"name": "P4", "size": 0.8},
            {"name": "P5", "size": 3.5},
        ]

        for process in processes:
            self.show_worst_fit_allocation(memory, partitions, process, animate_changes=True)

        # Cleanup
        self.play(FadeOut(Group(*self.mobjects)))

        # Conclusion
        conclusion_items = [
            Text("Worst-Fit Strategy:", font_size=42),
            Text("• Finds the largest free partition available", font_size=34),
            Text("• Leaves bigger gaps for smaller processes", font_size=34),
            Text("• Can reduce fragmentation in some cases", font_size=34),
            Text("• May lead to inefficient use of large spaces", font_size=34, color=RED),
        ]
        
        conclusion = VGroup(*conclusion_items).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        conclusion.to_edge(LEFT, buff=1)

        self.play(Write(conclusion))
        self.wait(3)

    def show_worst_fit_allocation(self, memory, partitions, new_process, animate_changes=False):
        process_info = Text(f"Allocating {new_process['name']} ({new_process['size']} units)", font_size=32)
        process_info.to_edge(DOWN)
        self.play(Write(process_info))
        self.wait(1)

        pointer = Arrow(start=LEFT, end=RIGHT, color=YELLOW)
        pointer.scale(0.8)
        pointer.next_to(memory, UP, buff=0.3)
        self.play(Create(pointer))

        # Worst-Fit Search: Find the largest free block
        worst_index = None
        worst_size = 0
        current_x = memory.get_left()[0]

        for i, partition in enumerate(partitions):
            width = partition["size"]
            new_x = current_x + width / 2
            self.play(pointer.animate.next_to([new_x, memory.get_center()[1], 0], UP, buff=0.3))

            if partition["status"] == "free" and partition["size"] >= new_process["size"]:
                if partition["size"] > worst_size:
                    worst_size = partition["size"]
                    worst_index = i

            current_x += width

        if worst_index is not None:
            self.update_memory_visualization(memory, partitions,
                f"Largest block found at position {worst_index+1} for {new_process['name']}",
                highlight_index=worst_index)
            self.wait(0.5)

            # Allocation with split if necessary
            if partitions[worst_index]["size"] > new_process["size"]:
                remaining_size = round(partitions[worst_index]["size"] - new_process["size"], 1)

                if animate_changes:
                    partitions[worst_index] = {"size": new_process["size"], "status": "allocated", "process": new_process["name"]}
                    partitions.insert(worst_index + 1, {"size": remaining_size, "status": "free", "process": None})

                    self.update_memory_visualization(memory, partitions,
                        f"Allocated {new_process['name']} and split block (remaining {remaining_size} free units)")
            else:
                if animate_changes:
                    partitions[worst_index] = {"size": partitions[worst_index]["size"], "status": "allocated", "process": new_process["name"]}

                    self.update_memory_visualization(memory, partitions,
                        f"Allocated {new_process['name']} to exact-fit block")
        else:
            self.play(FadeOut(process_info))
            self.show_fragmentation_issue(memory, partitions, new_process)
            self.play(FadeOut(pointer))
            return

        self.play(FadeOut(pointer), FadeOut(process_info))

    def show_fragmentation_issue(self, memory, partitions, new_process):
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

            rect = Rectangle(width=width, height=memory.height, color=color, fill_opacity=0.5, stroke_width=2)
            rect.move_to([current_x + width/2, memory.get_center()[1], 0])
            rectangles_group.add(rect)

            size_text = f"{partition['size']:.1f}" if partition["status"] == "free" else ""
            block_label_text = partition["process"] if partition["status"] == "allocated" else f"Free\n{size_text}"
            
            label = Text(block_label_text, font_size=24, color=WHITE)
            label.move_to(rect.get_center())
            labels_group.add(label)

            current_x += width

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

            rect = Rectangle(width=width, height=memory.height, color=YELLOW if highlight else color, fill_opacity=0.5, stroke_width=4 if highlight else 2)
            rect.move_to([current_x + width/2, memory.get_center()[1], 0])
            new_rectangles.add(rect)

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
