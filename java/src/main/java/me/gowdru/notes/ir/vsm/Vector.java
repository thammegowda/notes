package me.gowdru.notes.ir.vsm;

import java.util.TreeMap;

/**
 * Vector model class.
 * An instance of this represents a vector in n-dimensional space.
 * @author Thamme Gowda
 */
public class Vector {

    private final String vectorId;
    public long dimensions[];
    public long scales[];

    /**
     * Creates a vector
     * @param vectorId identifier for vector
     */
    public Vector(String vectorId) {
        this.vectorId = vectorId;
    }

    /**
     * Creates a vector
     * @param vectorId identifier for vector
     * @param features map of dimension -> magnitude entries. Requires entries to be sorted in ascending order of
     *                 dimension numbers
     */
    public Vector(String vectorId, TreeMap<Long, Long> features) {
        this(vectorId);
        this.dimensions = new long[features.size()];
        this.scales = new long[features.size()];
        int idx = 0;
        for (Long dimension : features.keySet()) {
            this.dimensions[idx] = dimension;
            this.scales[idx] = features.get(dimension);
            idx++;
        }
    }

    @Override
    public String toString() {
        StringBuilder builder = new StringBuilder();
        builder.append("(").append(vectorId).append("):{");
        if (dimensions != null && scales != null) {
            for (int i = 0; i < dimensions.length; i++) {
                builder.append(dimensions[i]).append(":").append(scales[i]).append(' ');
            }
        }
        builder.append("}");
        return builder.toString();
    }
}
