import unittest
import os

from novel_toy_tools.implementations.get_experiment_data import ExperimentalDataFromConsolidated

datasheet = r"/data/experimental/OldDataSheet.csv"


class TestExperimentalFromConsolidated(unittest.TestCase):
    def __init__(self, methodName = "runTest"):
        self.data_provider = ExperimentalDataFromConsolidated(datasheet, "/tests/experimental_from_consolidated")
        super().__init__(methodName)

if __name__ == "__main__":
    unittest.main()
    