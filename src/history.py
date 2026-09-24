from pathlib import Path
import json

class History:
    def __init__(self, path=None):
        self.path = path
        self.total_hist = {}
        self.date = 0

    def get_file(self, path=None):
        if path is not None:
            return Path(path)

        if self.path is not None:
            return Path(self.path)

        raise ValueError("No valid file path")

    def load(self, path=None):
        file = self.get_file(path)

        if not file.exists() or file.stat().st_size == 0:
            print("No previous history")
            self.total_hist = {}
            self.date = 0
            return

        try:
            with open(file, "r", encoding="utf-8") as f:
                self.total_hist = json.load(f)

            if self.total_hist:
                self.date = max(int(date) for date in self.total_hist.keys())
            else:
                self.date = 0

        except Exception as e:
            print(e)

    def save(self, new_hist, path=None, overwrite=False, new_day=False):
        file = self.get_file(path)

        try:
            if overwrite:
                self.total_hist = {}
                self.date = 0

            if new_day:
                self.date += 1
            elif self.date == 0:
                self.date = 1

            self.total_hist[str(self.date)] = new_hist

            with open(file, "w", encoding="utf-8") as f:
                json.dump(
                    self.total_hist,
                    f,
                    indent=4
                )

        except Exception as e:
            print(e)

    def clear(self, path=None):
        file = self.get_file(path)

        self.total_hist = {}
        self.date = 0

        with open(file, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4)

    def check(self):
        total_satisfied = 0 
        for date, value in self.total_hist.items():
            total_satisfied += int(value["satisfied"])
        print(f"You have recorded for {self.date} days")
        print(f"Among these days, you have satisfied the nutrition requirement for {total_satisfied} days!")

    def get_today(self):
        if str(self.date) in self.total_hist:
            return self.total_hist[str(self.date)]
        else:
            return None 