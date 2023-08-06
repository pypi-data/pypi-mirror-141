class DynamicElement:
    def __init__(self, frame: int = 0) -> None:
        self.frame = frame
    
    def render(self) -> str:
        raise NotImplementedError()

    def increment_frame(self):
        self.frame += 1
