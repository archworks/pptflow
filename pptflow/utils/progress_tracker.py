# Author: Valley-e
# Date: 2024/12/26  
# Description:
from dataclasses import dataclass
from typing import Callable


@dataclass
class ProgressStep:
    name: str
    weight: float  # Percentage weight of total progress (0-1)
    progress: float = 0  # Current progress of this step (0-1)


class ProgressTracker:
    def __init__(self, update_callback: Callable[[float, str], None]):
        self.steps = {
            'ppt_to_image': ProgressStep('Converting PPT to Images', 0.1),
            'ppt_note_to_audio': ProgressStep('Generating Audio', 0.5),
            'create_video': ProgressStep('Creating Video', 0.4)
        }
        self.current_step = None
        self.update_callback = update_callback

    def start_step(self, step_name: str):
        self.current_step = self.steps.get(step_name)
        if self.current_step:
            self.current_step.progress = 0
            self._update_progress()

    def update_step(self, progress: float):
        if self.current_step:
            self.current_step.progress = min(progress, 1.0)
            self._update_progress()

    def complete_step(self):
        if self.current_step:
            self.current_step.progress = 1.0
            self._update_progress()

    def _update_progress(self):
        total_progress = sum(step.progress * step.weight for step in self.steps.values())
        if self.current_step:
            status = f"{self.current_step.name} ({int(total_progress * 100)}%)"
        else:
            status = f"Progress: {int(total_progress * 100)}%"
        self.update_callback(total_progress, status)
