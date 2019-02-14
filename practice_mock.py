from random import randint

class MockMAX30100:
    def __init__(self):
        self.bpm = 0.0
    def update(self):
        self.bpm = 70 + randint(-15, 60)
    def get_bpm(self):
        return self.bpm
    def get_avg_bpm(self):
        return self.bpm
    
        
