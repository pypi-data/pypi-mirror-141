"""
libqc
~~~~
Statistical tools for genomic library QC.
"""

import gzip
import os
import re
from multiprocessing import Pool
from pathlib import Path
from typing import List

from .counts import Counts
from .library import Brunello, GuideLibrary


def make_counts(
    fastqs: List[Path],
    regex: re.Pattern,
    library: GuideLibrary = Brunello,
    output_path: Path = None,
) -> Path:
    """Constructs a file enumerating counts for constructs in a chosen library."""

    pool = Pool(os.cpu_count())
    counts = Counts(library.get_iter())

    results = []
    for fastq in fastqs:
        if fastq.suffix == ".gz":
            f = gzip.open(fastq, "rt")
        else:
            f = open(fastq, "r")

        i = 0
        j = 0
        for line in f.readlines():
            if i == 1:
                results.append(
                    pool.apply_async(
                        Counts.process,
                        (
                            line,
                            regex,
                            library.get_iter(),
                        ),
                    )
                )
                j += 1
                if j % 1000 == 0:
                    print(f"Processed {j} reads.")
            if i == 3:
                i = 0
                continue
            i += 1

    pool.close()
    pool.join()

    i = 0
    while len(results) > 0:
        result = results.pop()
        if not result.ready():
            results.insert(0, result)
            continue
        guides = result.get()
        for guide in guides:
            i += 1
            counts.count_map[guide] += 1
            if i % 1000 == 0:
                print(f"Processed {i} guides.")

    counts.to_csv()
