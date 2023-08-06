LibQC
----

A python toolkit for running quality control on CRISPR libraries.

When [amplifying](https://media.addgene.org/cms/filer_public/56/71/5671c68a-1463-4ec8-9db5-761fae99265d/broadgpp-pdna-library-amplification.pdf) sgRNA libraries, it is important to ensure that no single library element is
overrepresented in the resulting pool.
An uneven distribution of library elements will bias the disruption of the
genes they target. 

It becomes impossible to disentangle differences in counts from biological
effect from the initial amplication process as the screen progresses. `libqc`
thus provides a quick and dirty set of statistics and visualizations to verify
library integrity for downstream use.

## Quickstart

`pip install libqc`

```
from libqc import make_counts

make_counts(
    [Path("./foo.fastq.gz", "bar.fastq")], # One or more deep-sequencing files.
    re.compile(r".*AGGACGAAACACCG(.{20})*"), # Regex pattern to match spacers from PCR primers.
)
```

#### Outputs

```
├── libqc_gene_counts.csv # Mapping of genes to read counts.
├── libqc_sgrna_counts.csv # Mapping of sgRNAs to read counts
```

### Iterate through Library Elements

```
>>> from libqc import Brunello
>>> b = Brunello()
>>> next(b)
['A1BG_NM_130786.3_58351502_sense', 'CATCTTCTTTCACCTGAACG']
>>> next(b)
['A1BG_NM_130786.3_58350637_antisense', 'CTCCGGGGAGAACTCCGGCG']
```


## Library Support 

Open an issue for expanded support of additional well-characterized libraries.

### Brunello

76,441 sgRNA library for human genomes.

>  Doench JG, Fusi N, Sullender M, et al. Optimized sgRNA design to maximize
>  activity and minimize off-target effects of CRISPR-Cas9. Nat Biotechnol.
>  2016;34(2):184-191. doi:10.1038/nbt.3437


## Contribute

You won't. No balls.
