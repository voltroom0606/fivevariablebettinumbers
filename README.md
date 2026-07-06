# Betti tables of squarefree monomial ideals in five variables

This repository contains code and output files for the enumeration and Betti table computation of squarefree monomial ideals in five variables up to relabeling.

## Main computational results

- There are 210 squarefree monomial ideal representatives in five variables up to relabeling by the symmetric group $$S_5$$.
- Removing the zero ideal (0) and the unit ideal (1) leaves 208 nonzero proper representative ideals.
- Among these 208 representatives, there are 134 distinct graded Betti tables for the quotient rings $$S/I$$.

The Betti table computation was carried out in Macaulay2 over the finite field $$F_{67}$$; given that the paper proves characteristic-independence for monomial ideals in five variables, the computed Betti tables will agree with the Betti tables over any field.

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

## Explanation of output columns and terms

The computation groups the 208 nonzero proper squarefree monomial ideals in five variables by their graded Betti tables.

### Original index

The `original index` refers to the numbering in the table of 210 squarefree monomial ideal representatives. The zero ideal (0) and the unit ideal (1) are removed before computing Betti tables, leaving 208 nonzero proper representatives. 

For example, if an output says
original indices = {105}
that means the ideal comes from row 105 in the 210-ideal table.

### Betti table type

A `Betti table type` is one distinct graded Betti table. Two different ideals have the same type if their quotient rings $$S/I$$ have identical graded Betti tables.

The computation found 134 distinct Betti table types among the 208 nonzero proper representatives.

### Count

The `count` is the number of representativce ideals realizing a given Betti table type.

For example,

TYPE 92
count = 6

means that six different squarefree monomial ideals, up to relabeling, have the same graded Betti table.

### Graded Betti numbers

For a graded minimal free resolution

... -> $F_2$ -> $F_1$ -> $F_0$ -> $S/I$ -> 0,

we can write each free module as a direct sum of shifted copies of S: 
$$F_i$$ = direct sum over $$j$$ of $$S(-j)^{\beta_{i,j}}$$.

The numbers $$\beta_{i,j}$$ are the graded Betti numbers of $$S/I$$.

Here $$i$$ is the homological degree and $$j$$ is the internal degree. So, $$\beta_{2,4}$$ = 7 means that there are 7 generators in homological degree 2 and internal degree 4 in the minimal free resolution.

### Total Betti vector

The total Betti number in homological degree $$i$$ is obtained by summing over all internal degrees $$j$$:

$$\beta_i$$ = sum over $$j$$ of $$\beta_{i,j}$$.

The total Betti vector is ($$\beta_0$$, $$\beta_1$$, $$\beta_2$$, ..., $$\beta_p$$).

This is the `total` row in a Macaulay2 Betti table. It records the ranks of the free modules in the minimal resolution, but it forgets the degree shifts.

For example, if the nonzero graded Betti numbers are

$$\beta_{0,0}$$ = 1,
$$\beta_{1,1}$$ = 1,
$$\beta_{1,3}$$ = 4,
$$\beta_{2,4}$$ = 7,
$$\beta_{3,5}$$ = 3

then

$$\beta_0$$ = 1,
$$\beta_1$$ = 1 + 4 = 5,
$$\beta_2$$ = 7,
$$\beta_3$$ = 3

so the total Betti vector is

$$(1, 5, 7, 3)$$


### Projective dimension

The projective dimension of $$S/I$$ is the largest homological degree $$i$$ where some graded Betti number $$\beta_{i,j}$$ is nonzero.

In plain text: pd($$S/I$$) = max $$i$$ such that $$\beta_{i,j}$$ is nonzero for some $$j$$.

It is the length of the minimal free resolution.

For example, if the last nonzero Betti number occurs in homological degree 3, then pd($$S/I$$) = 3.

### Regularity

The regularity of $$S/I$$ is

reg($$S/I$$) = max($$j$$ - $$i$$) such that $$\beta_{i,j}$$ is nonzero.

It measures how far the nonzero Betti numbers extend above the linear strand.

For example, if $$\beta_{3,5}$$ is nonzero, then it contributes $$j$$ - $$i$$ = 5 - 3 = 2

to the regularity calculation.

## AI-use disclosure

AI tools were used to assist with code drafting, formatting, and debugging. The mathematical arguments and computational outputs were checked by the authors, including agreement between the Macaulay2 minimal-resolution computation and an independent Python implementation of Hochster's formula.

## License

The code in this repository is released under the MIT License. Computational output files are provided for reproducibility and may be used with attribution to the authors and citation of the accompanying paper.
