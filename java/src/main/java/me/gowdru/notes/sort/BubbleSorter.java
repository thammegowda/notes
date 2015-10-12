package me.gowdru.notes.sort;

import java.util.Comparator;

/**
 * This implementation of {@link Sorter} uses bubble/sink sorting technique to sort items.
 */
public class BubbleSorter<T> implements Sorter<T> {

    /**
     * performs bubble/sink sort on input items
     * @param items items to be sorted
     * @param comparator comparison assistant
     */
    public void sort(T[] items, Comparator<T> comparator) {
        int n = items.length;
        // n iterations
        T tmp;
        for (int i = 0; i < n; i++) {
            //n-i comparisons, leave out last one on successive iterations
            for (int j = 1; j < n - i; j++) {
                int comparison = comparator.compare(items[j - 1], items[j]);
                if (comparison > 0) {
                    //Item at 'j-1' is greater than 'j', so swap them
                    tmp = items[j-1];
                    items[j-1] = items[j];
                    items[j] = tmp;
                }
            }
        }
    }
}
