package me.gowdru.notes.ir.vsm;

import java.util.List;
import java.util.Map;
import java.util.TreeMap;

/**
 *
 * This implementation of {@link WeightScheme} maps tokens to features and sets unit scale for features which are present.
 * Features which are not present are 0 by default
 *
 */
public class BinaryScheme implements WeightScheme {

    private static final BinaryScheme INSTANCE = new BinaryScheme();

    public static BinaryScheme getInstance() {
        return INSTANCE;    
    }
    
    /**
     * Unit scale for features which are present
     */
    private double presenceScale = 1.0;

    @Override
    public TreeMap<Long, Double> apply(List<String> tokens, Map<String, Long> dict) {
        TreeMap<Long, Double> features = new TreeMap<>();

        tokens.stream()
                .filter(dict::containsKey)              // filter out which are not mapped in dictionary
                .map(dict::get)                         // map to feature number
                .filter(f -> !features.containsKey(f))  // filter out features which are already added,
                        // this scheme doesnt account frequency
                .forEach(f -> features.put(f, presenceScale)); // add it to the map
        return features;
    }
}
