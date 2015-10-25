package me.gowdru.notes.ir.vsm;

import java.util.List;
import java.util.Map;
import java.util.TreeMap;

/**
 * Defines a Weighing scheme contract
 * @see TermFrequencyScheme
 * @see BinaryScheme
 */
public interface WeightScheme {
    /**
     * apply the weighing scheme.
     * @param tokens List of tokens from which a vector needs to be constructed
     * @param dict dictionary for mapping
     * @return features
     */
    TreeMap<Long, Double> apply(List<String> tokens, Map<String, Long> dict);
}
