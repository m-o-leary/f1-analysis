import fastf1 as ff1
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import pandas as pd
import pathlib

def plot_relative_pace(laptimes: ff1.core.Laps, session : str="fp3") -> None:
    """
    Provided with Laps object, plot the relative pace.
    """
    fig = ((laptimes[[session]] - laptimes[[session]].min())
        .sort_values(session, ascending=False)
        .plot(kind='barh', figsize=(7,10)))
    plt.grid()
    plt.show()

def get_driver_best_lap_per_session(all_laps: ff1.core.Laps, pivot_value: str = 'session' ) -> pd.DataFrame:
    """
    Take in a Laps object amd return a dataframe indexed by driver
    and a column for each session with the miniumum time.
    """
    _df = pd.DataFrame(
        all_laps.groupby([pivot_value, "Driver"]).apply(
            lambda x: x['LapTime'].dt.total_seconds().min()
        )
    )\
    .reset_index()\
    .pivot(index="Driver", columns=pivot_value, values=0)
    
    return _df

def get_weekend_sessions(year: int, gp: str) -> ff1.core.Laps:
    """
    Retrieve a Laps objext with all info for all sessions in requested weekend.
    """
    
    sessions = [
        ("practice(1)", "fp1"), 
        ("practice(2)", "fp2"), 
        ("practice(3)", "fp3"), 
        ("quali()", "quali"), 
        ("race()", "race")
    ]
        
    weekend: ff1.core.Session = ff1.get_session(year, gp)
    
    session_list : list = []
    
    for sesh, name in sessions:
        print(f"Getting : {name}")
        _func = f"weekend.get_{sesh}"
        try:
            _sesh = eval(_func, {'weekend': weekend }).load_laps()
            _sesh["session"] = name
            session_list.append(_sesh)
        except ff1.api.SessionNotAvailableError as e:
            print(f"cannot retrieve session: {name}")
            

    return pd.concat(session_list)

if __name__ == "__main__":

    PATH = pathlib.Path().resolve().parent
    CACHE_PATH = PATH / "cache"
    
    ff1.Cache.enable_cache(CACHE_PATH)
    plot_relative_pace(
    get_driver_best_lap_per_session(
        get_weekend_sessions(2021, "Russian Grand Prix")), "quali")