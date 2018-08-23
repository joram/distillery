import datetime


class TimeSeriesStore(object):
    TEMPERATURE_DATA = []

    def add_value(self, value, time=None):
        if time is None:
            time = datetime.datetime.now()
        self.TEMPERATURE_DATA.append({
            "t": time,
            "y": value,
        })

    def json(self, dt=None):
        jsonVals = []
        for val in self.TEMPERATURE_DATA:
            if dt is None or val["t"] > dt:
                tStr = val["t"].strftime("%Y-%m-%dT%H:%M:%SZ") 
                jsonVals.append({
                    "t": tStr,
                    "y": val["y"],
                })
        return jsonVals

    @property
    def latest_value(self):
        if len(self.TEMPERATURE_DATA) <= 0:
            return -1
        return self.TEMPERATURE_DATA[-1]["y"]


