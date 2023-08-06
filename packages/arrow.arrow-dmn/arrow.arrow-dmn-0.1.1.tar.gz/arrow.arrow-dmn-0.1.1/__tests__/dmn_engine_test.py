import logging
import unittest
from pathlib import Path

from arrow_dmn.engine.sync_dmn_engine import SyncDmnEngine


class SequentialBpmnEngineTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.INFO)

    def test_dmn_engine(self):
        engine = SyncDmnEngine()
        ref = engine.deploy(Path(__file__).parent / "dmn/test.xml")
        print(engine.execute(ref, {"temperature": 10, "dayType": "Weekday"}))
