load "reps5.m2";

-- Betti table computation for the 208 nonzero proper squarefree
-- monomial ideal representatives in five variables.
-- The ring is over F_67 for efficiency.

S = ZZ/67[x1,x2,x3,x4,x5];
xs = {x1,x2,x3,x4,x5};

monomFromSubset = F -> product apply(F, i -> xs#(i-1));

idealFromRep = A -> monomialIdeal apply(A, monomFromSubset);

distinctKeys = {};
counts = new MutableHashTable;
indicesByKey = new MutableHashTable;
idealsByKey = new MutableHashTable;
tables = new MutableHashTable;

for idx from 0 to (#reps - 1) do (
    A := reps#idx;
    originalIndex := origIndices#idx;

    I := idealFromRep A;
    Q := coker gens I; -- this is S/I

    B := betti res Q;
    K := toString(B);

    if not member(K, distinctKeys) then (
        distinctKeys = append(distinctKeys, K);
        counts#K = 1;
        indicesByKey#K = {originalIndex};
        idealsByKey#K = {toString(I)};
        tables#K = B;
    ) else (
        counts#K = counts#K + 1;
        indicesByKey#K = append(indicesByKey#K, originalIndex);
        idealsByKey#K = append(idealsByKey#K, toString(I));
    );
);

outTypes = openOut "distinct_betti_table_types_m2.txt";

outTypes << "Number of nonzero proper representatives = " << toString(#reps) << endl;
outTypes << "Number of distinct Betti tables = " << toString(#distinctKeys) << endl;
outTypes << endl;

for t from 0 to (#distinctKeys - 1) do (
    K := distinctKeys#t;

    outTypes << "========================================" << endl;
    outTypes << "TYPE " << toString(t+1) << endl;
    outTypes << "count = " << toString(counts#K) << endl;
    outTypes << "original indices = " << toString(indicesByKey#K) << endl;
    outTypes << endl;

    outTypes << toString(tables#K) << endl;
    outTypes << endl;

    outTypes << "Ideals with this Betti table:" << endl;
    scan(idealsByKey#K, s -> outTypes << "  " << s << endl);
    outTypes << endl;
);

close outTypes;

print("Number of nonzero proper representatives = " | toString(#reps));
print("Number of distinct Betti tables = " | toString(#distinctKeys));
print("Wrote distinct_betti_table_types_m2.txt");
