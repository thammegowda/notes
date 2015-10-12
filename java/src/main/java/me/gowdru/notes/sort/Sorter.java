package me.gowdru.notes.sort;

import java.util.Comparator;

/**
 * Defines contract for Sorter algorithm implementations
 */
public interface Sorter<T> {

    /**
     * sorts {@code items}i in an array by comparing them using {@code comparator}
     * @param items items to be sorted
     * @param comparator comparison assistant
     */
    public void sort(T[] items, Comparator<T> comparator);

}
