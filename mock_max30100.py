from time import sleep

from bidmc import BidmcData

QUEUE_SIZE = 4


class MockMAX30100:
    def __init__(self, dataset_number='01'):
        self.bpm = 0.0
        self.bpm_queue = []
        self.avg_bpm = 0.0
        self.data = BidmcData(dataset_number)

    def update(self):
        ''' Update the values '''
        current_data = self.data.next()
        self.bpm = int(current_data[' HR']
                       ) if current_data[' HR'] != 'NaN' else 0
        self.spo2 = int(current_data[' SpO2']
                        ) if current_data[' SpO2'] != 'NaN' else 0
        if len(self.bpm_queue) > QUEUE_SIZE:
            self.bpm_queue = self.bpm_queue[1:]
        self.bpm_queue.append(self.bpm)

    def get_bpm(self):
        return self.bpm

    def get_spo2(self):
        return self.spo2

    def get_avg_bpm(self):
        return sum(self.bpm_queue)/len(self.bpm_queue)


if __name__ == "__main__":
    pulseox = MockMAX30100('01')
    while True:
        pulseox.update()
        bpm = pulseox.get_bpm()
        avg_bpm = pulseox.get_avg_bpm()
        spo2 = pulseox.get_spo2()
        print("BPM:{0}\nAVG_BPM:{1}\nSPO2:{2}".format(bpm, avg_bpm, spo2))
        print("="*10)
        sleep(1)
