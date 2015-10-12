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

    /**
     * swaps a pair of elements in array
     * @param array - array of items
     * @param pos1 position of an item to be swapped to/with
     * @param pos2 position of another item to be swapped to/with
     */
    public default void swap(T[] array, int pos1, int pos2){
        T tmp = array[pos1];
        array[pos1] = array[pos2];
        array[pos2] = tmp;
    }
}
