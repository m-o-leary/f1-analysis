import f1lib.data_prep
import fastf1
import pandas as pd
import unittest
import pathlib
import shutil


class TestDataPrep(unittest.TestCase):
    """Test the data prep module
    """
    
    @classmethod
    def setUpClass(self)-> None:
        self.CACHE_DIR = pathlib.Path().absolute()
        self.CACHE_DIR = self.CACHE_DIR  / "cache"
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def tearDownClass(self) -> None:
        shutil.rmtree(self.CACHE_DIR)

    def test_initialization(self) -> None:
        dp = f1lib.data_prep.DataPrep(2021,"Turkey", self.CACHE_DIR)
        self.assertIsInstance(dp, f1lib.data_prep.DataPrep)
    
    def test_data_prep_get_laps(self) -> None:
        dp = f1lib.data_prep.DataPrep(2021,"Turkey", self.CACHE_DIR)
        laps = dp.get_laps()
        self.assertIsInstance(laps, pd.DataFrame)
        self.assertTrue(len(laps)>0)

    def test_get_reference(self)->None:
        dp = f1lib.data_prep.DataPrep(2021,"Turkey", self.CACHE_DIR)
        laps = dp.get_laps()
        lts = dict(
            LapTimeSeconds=lambda df: [i.seconds for i in df["LapTime"]])
        ref = dp.get_reference(laps.assign(**lts))

        self.assertIsInstance(ref, pd.Series)
    
    def test_prep_for_lap_plot(self)->None:
        dp = f1lib.data_prep.DataPrep(2021,"Turkey", self.CACHE_DIR)
        data = dp.prep_for_lap_plot()

        self.assertIsInstance(data, pd.DataFrame)
        self.assertTrue(len(data.columns) == 20)



