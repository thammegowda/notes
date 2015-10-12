package me.gowdru.notes.sort;

import java.util.Comparator;

/**
 * This implementation of {@link Sorter} that uses selection sort technique to sort items.
 */
public class SelectionSorter<T> implements Sorter<T> {


    /**
     * performs selection sort on input items
     * @param items items to be sorted
     * @param comparator comparison assistant
     */
    public void sort(T[] items, Comparator<T> comparator) {
        int n = items.length;

        for (int i = 0; i < n; i++) {
            int smallerPos = i;
            for (int j = i + 1 ; j < n ; j++) {
                if (comparator.compare(items[j], items[smallerPos]) < 0){
                    //I[j]  < I[smallerPos]
                    smallerPos = j;
                }
            }
            // now the smallest item is pointed by smallerPos
            swap(items, i, smallerPos);
        }
    }
}
