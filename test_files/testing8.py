import json
import pandas as pd


from datetime import datetime
from datetime import timedelta

now = datetime.now()
aa = now.strftime("%Y-%m-%d")

bb = datetime.now() + timedelta(days = 0.5)
bb = bb.strftime("%Y-%m-%d, %H:%M:%S")
print(aa)
print(bb)