import fastf1 as ff1
from numpy import float32
from pandas.core.frame import DataFrame
from src import plot_drivers
import pandas as pd
from dataclasses import dataclass

@dataclass
class DataPrep:
    """
    Class for preparation of lap data to make a nice plot!
    """
    year: int 
    gp: str
    cache: str

    def get_laps(self) -> pd.DataFrame:
        ff1.Cache.enable_cache(self.cache)  # replace with your cache directory
        session = ff1.get_session(self.year, self.gp, 'R')
        laps = session.load_laps(with_telemetry=True)
        return laps

    def get_reference(self, laps: pd.DataFrame) -> pd.Series:
        """
        Get the reference value to be subtracted for each lap from all drivers times.

        Args:
            laps (pd.DataFrame): Dataframe containing the laps as well as LapTimeNorm and LapTimeSeconds.

        Returns:
            pd.Series: A series with a value for each lap of the race corresponding to a reference value.
        """

        return (
            laps.groupby('LapNumber')["LapTimeSeconds"]
            .apply(self.selective_mean).cumsum()
        )

    def prep_for_lap_plot(self) -> pd.DataFrame:
        """
        Prepare data for plotting a relative gap plot over all laps.

        Returns:
            pd.DataFrame: Dataframe with a column for each driver with an entry for each lap. 
            The enties are the relative gap for that lap from the average laoptime on that lap based on the best time + 10% (to account for pitting)
        """

        df = (
            self.get_laps()
            .assign(LapTimeNorm=lambda df: df.apply(lambda row: row['Time'] - row["LapStartTime"], axis=1))
            .assign(LapTimeSeconds=lambda df: [i.seconds for i in df["LapTimeNorm"]])
        )
        
        ref = self.get_reference(df)
        
        return (
            df
            .groupby(['LapNumber', "Driver"], as_index=False)["LapTimeSeconds"]
            .agg(('first'))
            .pivot(columns="Driver", index="LapNumber", values="LapTimeSeconds")
            .fillna(method='pad')
            .cumsum()
            .apply(lambda row: (row - ref), axis=0)
        )
    
    def selective_mean(self, series:pd.Series, *args)->float:
        print(args)
        best = series.min()
        min_plus_10pc = (best + best*0.1)
        
        mask = ( series >= best ) & (series <= min_plus_10pc)
        
        return series[mask].mean()
