import random
import datetime


class TimeSeriesStore(object):
    TEMPERATURE_DATA = {}

    def add_temp(self, name, value, time=None):
        if time is None:
            time = datetime.datetime.now()
        if name not in self.TEMPERATURE_DATA:
            self.TEMPERATURE_DATA[name] = []
        print time, name, value
        self.TEMPERATURE_DATA[name].append({
            "t": time,
            "y": value,
        })


    def populate_demo(self, n=30):
        for name in ["T1", "T2", "T3"]:
            prev = random.uniform(18.0, 24.0)
            for i in range(0, n):
                value = prev + random.uniform(-2.0,2.0)
                t = datetime.datetime.now() - datetime.timedelta(minutes=n-i)
                self.add_temp(name, value, t)
                prev = value

    def json(self, dt=None):
        data = {}
        for key in self.TEMPERATURE_DATA:
            jsonVals = []
            vals = self.TEMPERATURE_DATA[key]
            for val in vals:
                if dt is None or val["t"] > dt:
                    tStr = val["t"].strftime("%Y-%m-%dT%H:%M:%SZ") 
                    jsonVals.append({
                        "t": tStr,
                        "y": val["y"],
                    })
            data[key] = jsonVals
        return data
