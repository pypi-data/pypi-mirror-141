"""
library
~~~~
Stable interfaces for well-characterized libraries.
"""

from io import TextIOWrapper
from pathlib import Path


class GuideLibrary:
    def __next__():
        return NotImplementedError

    def __iter__():
        return NotImplementedError

    @property
    def csv_file() -> TextIOWrapper:
        """Returns a file handler to a CSV file containing the library."""
        return NotImplementedError

    @property
    def fasta_file() -> TextIOWrapper:
        """Returns a file handler to a FASTA file containing the library."""
        return NotImplementedError


class Brunello(GuideLibrary):
    """76,441 gRNA library for human genomes.

    Doench JG, Fusi N, Sullender M, et al. Optimized sgRNA design to maximize
    activity and minimize off-target effects of CRISPR-Cas9. Nat Biotechnol.
    2016;34(2):184-191. doi:10.1038/nbt.3437
    """

    _csv_file_path = Path(__file__).resolve().parent.joinpath("lib/brunello.csv")
    _csv_file_handler = None
    _fasta_file_path = Path(__file__).resolve().parent.joinpath("lib/brunello.fa")
    _fasta_file_handler = None

    def get_iter():
        """Get a fresh iterator of type self."""
        return __class__()

    def _reset(self):
        self._csv_file_handler.close()
        self._csv_file_handler = None

    def __next__(self):
        if self._csv_file_handler is None:
            f = open(self._csv_file_path, "r")
            # Header
            f.readline()
            self._csv_file_handler = f

        line = self._csv_file_handler.readline()
        if line == "":
            self._csv_file_handler.close()
            self._csv_file_handler = None
            raise StopIteration
        else:
            return line.strip().split(",")

    def __iter__(self):
        return self
