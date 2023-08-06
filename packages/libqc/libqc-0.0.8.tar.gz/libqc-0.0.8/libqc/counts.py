"""
counts
~~~~~~
Stateful counts map.
"""

import re
from pathlib import Path
from typing import Dict, List

from .library import GuideLibrary


class Counts:
    library: GuideLibrary = None
    count_map: Dict[str, int] = None

    def __init__(self, library: GuideLibrary):
        """Holds on to count mapping.

        Params:

            library: Object serving library element names and sequences.
            pattern: Regex pattern to extract element sequences from reads.
        """

        self.library = library
        self.count_map = {}

        # Want all elements to have meaningful 0s.
        for name, _ in self.library:
            self.count_map[name] = 0

    def process(
        reads: List[str], pattern: re.Pattern, library: GuideLibrary
    ) -> List[str]:
        """Adds read to count table.

        Returns:
            The element id found or None

        """

        def _identify_read(read: str) -> str:
            read = read.strip()

            match = pattern.search(read)
            if not match:
                return
            else:
                fragment = match.group(1)

            if fragment is None or fragment == "":
                return

            for name, sg_rna in library:
                if sg_rna in fragment:
                    return name

        names = []
        for read in reads:
            names.append(_identify_read(read))

        return names

    def to_csv(self, sgrna_path: Path = None, gene_path: Path = None):

        if sgrna_path is None:
            sgrna_path = Path("./libqc_sgrna_counts.csv")
        if gene_path is None:
            gene_path = Path("./libqc_gene_counts.csv")

        gene_counts = {}

        with open(sgrna_path, "w") as f:
            f.write("sg_rna,count")
            for name, sg_rna in self.library:
                counts = self.count_map[name]

                gene_name = name.split("_")[0]
                if gene_name not in gene_counts:
                    gene_counts[gene_name] = counts
                else:
                    gene_counts[gene_name] += counts
                f.write(f"\n{name},{counts}")

        with open(gene_path, "w") as f:
            f.write("gene,count")
            for name, counts in gene_counts.items():
                f.write(f"\n{name},{counts}")
