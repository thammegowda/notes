package me.gowdru.notes.ir.vsm;

import java.util.List;
import java.util.Map;
import java.util.TreeMap;

/**
 * This implementation of {@link WeightScheme} maps tokens to features and also counts frequency of features.
 * The frequency of the features are meant to be used by vectorizer as scale/magnitude.
 *
 */
public class TermFrequencyScheme implements WeightScheme {

    public boolean normalize;

    public TermFrequencyScheme(boolean normalize) {
        this.normalize = normalize;
    }

    @Override
    public TreeMap<Long, Double> apply(List<String> tokens, Map<String, Long> dict) {
        TreeMap<Long, Double> features = new TreeMap<>();
        tokens.stream()
                .filter(dict::containsKey)     // filter out which are not mapped in dictionary
                .map(dict::get)                // map to feature number
                .forEach(f -> features.put(f, features.getOrDefault(f, 0.0) + 1.0)); // add it to the map,
                                                                                    // increment the frequency every time
        if (normalize) {
            // basic normalization using log
            for (Long key: features.keySet()) {
                features.put(key, Math.log(1 + features.get(key)));
            }

        }
        return features;
    }
}
