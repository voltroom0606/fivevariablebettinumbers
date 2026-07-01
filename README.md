# Betti tables of squarefree monomial ideals in five variables

This repository contains code and output files for the enumeration and Betti table computation of squarefree monomial ideals in five variables up to relabeling.

## Main computational results

- There are 210 squarefree monomial ideal representatives in five variables up to relabeling by the symmetric group `S_5`.
- Removing the zero ideal (0) and the unit ideal (1) leaves 208 nonzero proper representative ideals.
- Among these 208 representatives, there are 134 distinct graded Betti tables for the quotient rings S/I.

The Betti table computation was carried out in Macaulay2 over the finite field `F_67`; given that the paper proves characteristic-independence for monomial ideals in five variables, the computed Betti tables will agree with the Betti tables over any field.

## Repository structure

```text
code/
  generate_squarefree_ideals.py   # Generates the 210 representative ideals and reps5.m2
  compute_betti_tables.m2         # Macaulay2 Betti table computation 
  hochster_python_check.py        # Optional Hochster check by Python and cleaner output

data/
  reps5.m2                             # Macaulay2 input file: the 208 nonzero proper representative ideals
  squarefree_210_ideals.txt            # Readable list of all 210 representative ideals
  monomial_ideal_index_table_only.tex  # LaTeX table of all 210 representatives

output/
  distinct_betti_table_types_m2.txt    # Main Macaulay2 output: 134 Betti table types and ideals realizing each type
  betti_table_types_with_all_ideals_python.txt # Cleaner Betti table output
  betti_ideal_to_type_mapping.csv      # CSV mapping each ideal index to a Betti table type
  betti_type_summary.csv               # CSV summary of the 134 Betti table types
  betti_multiplicity_distribution.tex  # LaTeX table of multiplicities
```

## How to reproduce the computation

First generate the representatives and the Macaulay2 input file:

```bash
python3 code/generate_squarefree_ideals.py
```

This creates `reps5.m2`.

Then run the Macaulay2 computation:

```bash
M2 --script code/compute_134_betti_tables.m2
```

The main output is `distinct_betti_table_types_m2.txt`.

The optional Python/Hochster check can be run with:

```bash
python3 code/hochster_python_check.py
```

## Notes on the computation

The Python enumeration represents subsets of `[5]` using binary masks. It generates all antichains in the Boolean lattice `2^[5]`, applies all permutations in `S_5`, and keeps one canonical representative from each relabeling orbit.

The Macaulay2 script is the main method of computation utilizing commutative algebra. For each representative ideal `I`, it computes the Betti table of `S/I` using:

```macaulay2
betti res coker gens I
```

The Python/Hochster script is included as an independent check and for cleaner formatted output.

## AI-use disclosure

AI tools were used to assist with code drafting, formatting, and debugging. The mathematical arguments and computational outputs were checked by the authors, including agreement between the Macaulay2 minimal-resolution computation and an independent Python implementation of Hochster's formula.

## License

The code in this repository is released under the MIT License. Computational output files are provided for reproducibility and may be used with attribution to the authors and citation of the accompanying paper.
