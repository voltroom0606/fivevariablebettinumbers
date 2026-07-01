from itertools import permutations
from pathlib import Path

# This script generates the 210 squarefree monomial ideal representatives
# in five variables, up to relabeling by S_5. It also writes reps5.m2,
# which is used by the Macaulay2 Betti-table computation.

N = 5


def subset_is_contained(a, b):
    """Return True if subset a is contained in subset b.

    Subsets are represented by binary masks.
    """
    return (a & b) == a


def comparable(a, b):
    """Two subsets are comparable if one is contained in the other."""
    return subset_is_contained(a, b) or subset_is_contained(b, a)


def all_subsets(n):
    """Return all subsets of [n], represented as bitmasks."""
    subsets = []
    for mask in range(2 ** n):
        subsets.append(mask)
    return subsets


def build_antichains(current_antichain, candidates, output):
    """Recursively build all antichains."""
    output.append(tuple(current_antichain))

    for position in range(len(candidates)):
        chosen_subset = candidates[position]
        new_antichain = current_antichain + [chosen_subset]

        new_candidates = []
        for later_subset in candidates[position + 1:]:
            if not comparable(chosen_subset, later_subset):
                new_candidates.append(later_subset)

        build_antichains(new_antichain, new_candidates, output)


def all_antichains(n):
    """Generate all labeled antichains in the Boolean lattice 2^[n]."""
    output = []
    subsets = all_subsets(n)
    build_antichains([], subsets, output)
    return output


def permute_subset(mask, perm, n):
    """Apply a variable permutation to one subset."""
    new_mask = 0

    for old_position in range(n):
        if mask & (1 << old_position):
            new_position = perm[old_position]
            new_mask = new_mask | (1 << new_position)

    return new_mask


def permute_antichain(A, perm, n):
    """Apply a variable permutation to every subset in an antichain."""
    new_antichain = []

    for subset in A:
        new_subset = permute_subset(subset, perm, n)
        new_antichain.append(new_subset)

    new_antichain.sort()
    return tuple(new_antichain)


def canonical_form(A, n):
    """Choose the lexicographically smallest relabeling of an antichain."""
    best = None

    for perm in permutations(range(n)):
        relabeled = permute_antichain(A, perm, n)
        if best is None or relabeled < best:
            best = relabeled

    return best


def representatives(n):
    """Generate one representative from each relabeling class of antichains."""
    labeled_antichains = all_antichains(n)
    seen = set()
    reps = []

    for A in labeled_antichains:
        C = canonical_form(A, n)
        if C not in seen:
            seen.add(C)
            reps.append(C)

    reps.sort(key=lambda A: (len(A), A))
    return reps


def mask_to_subset(mask, n):
    """Convert a bitmask back to ordinary subset notation."""
    subset = []
    for i in range(n):
        if mask & (1 << i):
            subset.append(i + 1)
    return tuple(subset)


def monomial(mask, n):
    """Convert a subset to the corresponding squarefree monomial."""
    subset = mask_to_subset(mask, n)

    if subset == ():
        return "1"

    factors = []
    for i in subset:
        factors.append("x" + str(i))

    return "*".join(factors)


def ideal_string(A, n):
    """Convert an antichain to the corresponding monomial ideal."""
    if A == ():
        return "(0)"

    generators = []
    for mask in A:
        generators.append(monomial(mask, n))

    return "(" + ", ".join(generators) + ")"


def monomial_latex(mask, n):
    subset = mask_to_subset(mask, n)
    if subset == ():
        return "1"
    return "".join(["x_{" + str(i) + "}" for i in subset])


def ideal_latex(A, n):
    if A == ():
        return r"\(\bigl(0\bigr)\)"
    gens = r",\allowbreak ".join([monomial_latex(mask, n) for mask in A])
    return r"\(\bigl(" + gens + r"\bigr)\)"


def m2_subset(mask, n):
    subset = mask_to_subset(mask, n)
    entries = []
    for i in subset:
        entries.append(str(i))
    return "{" + ",".join(entries) + "}"


def m2_antichain(A, n):
    pieces = []
    for mask in A:
        pieces.append(m2_subset(mask, n))
    return "{" + ",".join(pieces) + "}"


def write_outputs(reps, n):
    proper_reps = []
    original_indices = []

    for index, A in enumerate(reps, start=1):
        if A == ():      # zero ideal (0)
            continue
        if A == (0,):    # unit ideal (1)
            continue
        proper_reps.append(A)
        original_indices.append(index)

    # Human-readable list.
    with open("squarefree_210_ideals.txt", "w") as f:
        f.write("Squarefree monomial ideals in 5 variables up to relabeling\n")
        f.write("Total representatives: 210\n\n")
        for index, A in enumerate(reps, start=1):
            subsets = []
            for mask in A:
                subsets.append(mask_to_subset(mask, n))
            f.write(str(index) + ": " + str(tuple(subsets)) + "   " + ideal_string(A, n) + "\n")

    # LaTeX longtable.
    with open("monomial_ideal_index_table_only.tex", "w") as f:
        f.write(r"""% Requires:
% \usepackage{longtable,booktabs,array}

{\scriptsize
\begin{longtable}{@{}r>{\raggedright\arraybackslash}p{0.86\textwidth}@{}}
\caption{Table of squarefree monomial ideals with 5 variables up to relabeling.}
\label{table:monomial-ideal-index}\\
\toprule
Index & Ideal \\
\midrule
\endfirsthead
\toprule
Index & Ideal \\
\midrule
\endhead
\midrule
\multicolumn{2}{r}{\emph{Continued on next page}}\\
\midrule
\endfoot
\bottomrule
\endlastfoot
""")
        for index, A in enumerate(reps, start=1):
            f.write(str(index) + " & " + ideal_latex(A, n) + r" \\" + "\n")
        f.write(r"""\end{longtable}
}
""")

    # Macaulay2 input file for the 208 nonzero proper representatives.
    with open("reps5.m2", "w") as f:
        f.write("-- This file was generated by the Python script.\n")
        f.write("-- It contains the 208 nonzero proper representatives.\n\n")

        f.write("origIndices = {\n")
        for i in range(len(original_indices)):
            comma = "," if i < len(original_indices) - 1 else ""
            f.write("  " + str(original_indices[i]) + comma + "\n")
        f.write("};\n\n")

        f.write("reps = {\n")
        for i in range(len(proper_reps)):
            comma = "," if i < len(proper_reps) - 1 else ""
            f.write("  " + m2_antichain(proper_reps[i], n) + comma + "\n")
        f.write("};\n")

    print("Wrote squarefree_210_ideals.txt")
    print("Wrote monomial_ideal_index_table_only.tex")
    print("Wrote reps5.m2")
    print("Number of nonzero proper representatives:", len(proper_reps))


def main():
    reps = representatives(N)
    print("Number of representatives:", len(reps))

    if len(reps) != 210:
        print("Warning: expected 210 representatives.")

    write_outputs(reps, N)


main()
