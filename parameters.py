class Parameter():
    def __init__(self,
        height=700,
        width=800
        ):
        self.height = height 
        self.width = width
    
    def window_size(self):
        return self.width, self.height