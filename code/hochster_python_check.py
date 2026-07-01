from itertools import permutations
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

def comparable(a, b):
    return (a & b) == a or (a & b) == b

def antichains(n):
    subsets = list(range(1 << n))
    def rec(A, candidates):
        yield tuple(A)
        for i, s in enumerate(candidates):
            new_candidates = [t for t in candidates[i+1:] if not comparable(s, t)]
            yield from rec(A + [s], new_candidates)
    yield from rec([], subsets)

def permute_mask(mask, perm, n):
    new = 0
    for i in range(n):
        if mask & (1 << i):
            new |= 1 << perm[i]
    return new

def canonical(A, n):
    return min(tuple(sorted(permute_mask(m, p, n) for m in A)) for p in permutations(range(n)))

def representatives(n):
    return sorted({canonical(A, n) for A in antichains(n)}, key=lambda A: (len(A), A))

def popcount(x):
    return int(x).bit_count()

def mask_to_subset(mask, n=5):
    return tuple(i+1 for i in range(n) if mask & (1 << i))

def ideal_plain(A, n=5):
    if A == ():
        return "(0)"
    def mon_plain(mask):
        s = mask_to_subset(mask, n)
        return "1" if not s else "*".join(f"x{i}" for i in s)
    return "(" + ", ".join(mon_plain(m) for m in A) + ")"

def is_face(F, A):
    return all((g & F) != g for g in A)

def induced_faces(A, W, n=5):
    return [F for F in range(1 << n) if (F & ~W) == 0 and is_face(F, A)]

def faces_by_dim(faces):
    d = defaultdict(list)
    for F in faces:
        sz = popcount(F)
        if sz >= 1:
            d[sz-1].append(F)
    for k in d:
        d[k].sort()
    return d

def rank_rational(mat):
    if not mat:
        return 0
    rows = len(mat)
    cols = len(mat[0]) if rows else 0
    if cols == 0:
        return 0
    m = [list(map(Fraction, row)) for row in mat]
    r = 0
    for c in range(cols):
        pivot = None
        for i in range(r, rows):
            if m[i][c] != 0:
                pivot = i
                break
        if pivot is None:
            continue
        m[r], m[pivot] = m[pivot], m[r]
        pv = m[r][c]
        m[r] = [x / pv for x in m[r]]
        for i in range(rows):
            if i != r and m[i][c] != 0:
                factor = m[i][c]
                m[i] = [m[i][j] - factor*m[r][j] for j in range(cols)]
        r += 1
        if r == rows:
            break
    return r

def boundary_rank(faces_dim, q, n=5):
    # Rank of boundary C_q -> C_{q-1}, q >= 1.
    qs = faces_dim.get(q, [])
    prev = faces_dim.get(q-1, [])
    if not qs or not prev:
        return 0
    row_index = {F: i for i, F in enumerate(prev)}
    mat = [[0] * len(qs) for _ in range(len(prev))]
    for col, F in enumerate(qs):
        verts = [i for i in range(n) if F & (1 << i)]
        for pos, v in enumerate(verts):
            G = F & ~(1 << v)
            mat[row_index[G]][col] += (-1) ** pos
    return rank_rational(mat)

def reduced_homology_dim_Q(A, W, q, n=5):
    faces = induced_faces(A, W, n)
    face_set = set(faces)
    if q < -1:
        return 0
    if q == -1:
        return 1 if face_set == {0} else 0

    faces_dim = faces_by_dim(faces)
    dimCq = len(faces_dim.get(q, []))

    if q == 0:
        # Augmentation C_0 -> Z has rank 1 when there is at least one vertex.
        rank_dq = 1 if dimCq > 0 else 0
    else:
        rank_dq = boundary_rank(faces_dim, q, n)

    rank_dq1 = boundary_rank(faces_dim, q+1, n) if faces_dim.get(q+1, []) else 0
    return dimCq - rank_dq - rank_dq1

def betti(A, n=5):
    b = defaultdict(int)
    for W in range(1 << n):
        j = popcount(W)
        for i in range(n+1):
            q = j - i - 1
            h = reduced_homology_dim_Q(A, W, q, n)
            if h:
                b[(i, j)] += h
    return dict(sorted(b.items()))

def betti_key(b):
    return tuple(sorted(b.items()))

def total_vector(b):
    max_i = max((i for (i, j) in b), default=0)
    return tuple(sum(v for (i, j), v in b.items() if i == ii) for ii in range(max_i+1))

def pd_reg(b):
    pd = max(i for (i, j), v in b.items() if v)
    reg = max(j - i for (i, j), v in b.items() if v)
    return pd, reg

def format_betti_table(b):
    max_i = max(i for i, j in b)
    max_shift = max(j-i for i, j in b)
    lines = []
    lines.append("       " + " ".join(f"{i:>4}" for i in range(max_i+1)))
    lines.append("total: " + " ".join(f"{sum(v for (i,j),v in b.items() if i == col):>4}" for col in range(max_i+1)))
    for r in range(max_shift+1):
        vals = []
        for i in range(max_i+1):
            val = b.get((i, i+r), 0)
            vals.append(f"{str(val) if val else '.':>4}")
        lines.append(f"{r:>5}: " + " ".join(vals))
    return "\n".join(lines)

def main():
    n = 5
    reps = representatives(n)
    proper = [(idx+1, A) for idx, A in enumerate(reps) if A != () and A != (0,)]

    results = []
    for idx, A in proper:
        results.append((idx, A, betti(A, n)))

    groups = defaultdict(list)
    for idx, A, b in results:
        groups[betti_key(b)].append((idx, A, b))

    group_items = []
    for key, lst in groups.items():
        min_idx = min(x[0] for x in lst)
        ex = sorted(lst, key=lambda x: x[0])[0]
        group_items.append((min_idx, key, lst, ex))
    group_items.sort(key=lambda x: x[0])

    outdir = Path(".")
    all_file = outdir / "all_208_betti_tables_python.txt"
    types_file = outdir / "distinct_betti_table_types_python.txt"

    with all_file.open("w") as f:
        f.write("Betti tables for 208 nonzero proper squarefree monomial ideals in 5 variables up to relabeling\n")
        f.write("Computed by Python via Hochster's formula over Q.\n")
        f.write("Betti numbers are for S/I, where S = k[x1,x2,x3,x4,x5].\n")
        f.write(f"Number of representatives = {len(results)}\n")
        f.write(f"Number of distinct Betti tables = {len(groups)}\n\n")
        for idx, A, b in results:
            pd, reg = pd_reg(b)
            f.write("="*72 + "\n")
            f.write(f"Original table index: {idx}\n")
            f.write(f"Ideal: {ideal_plain(A)}\n")
            f.write(f"Betti dictionary beta_(i,j): {b}\n")
            f.write(f"Total Betti vector: {total_vector(b)}\n")
            f.write(f"pd(S/I) = {pd}; reg(S/I) = {reg}\n")
            f.write(format_betti_table(b) + "\n\n")

    with types_file.open("w") as f:
        f.write("Distinct Betti table types among the 208 nonzero proper representatives\n")
        f.write("Computed by Python via Hochster's formula over Q.\n")
        f.write("Betti numbers are for S/I, where S = k[x1,x2,x3,x4,x5].\n")
        f.write(f"Number of representatives = {len(results)}\n")
        f.write(f"Number of distinct Betti tables = {len(groups)}\n\n")
        for t, (min_idx, key, lst, ex) in enumerate(group_items, 1):
            idx, A, b = ex
            pd, reg = pd_reg(b)
            indices = [x[0] for x in sorted(lst, key=lambda x: x[0])]
            f.write("="*72 + "\n")
            f.write(f"TYPE {t}\n")
            f.write(f"count = {len(lst)}\n")
            f.write(f"example original table index = {idx}\n")
            f.write(f"example ideal = {ideal_plain(A)}\n")
            f.write(f"all original indices with this table = {indices}\n")
            f.write(f"Betti dictionary beta_(i,j) = {dict(key)}\n")
            f.write(f"Total Betti vector = {total_vector(b)}\n")
            f.write(f"pd(S/I) = {pd}; reg(S/I) = {reg}\n")
            f.write(format_betti_table(b) + "\n\n")

    print(f"Number of representatives = {len(results)}")
    print(f"Number of distinct Betti tables = {len(groups)}")
    print(f"Wrote {all_file}")
    print(f"Wrote {types_file}")

if __name__ == "__main__":
    main()
