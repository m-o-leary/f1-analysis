import fastf1 as ff1
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib import cm
import numpy as np

ff1.Cache.enable_cache('../doc_cache')  # replace with your cache directory

session = ff1.get_session(2021, 'Austrian Grand Prix', 'Q')
laps = session.load_laps(with_telemetry=True)

lap = laps.pick_fastest()
tel = lap.get_telemetry()