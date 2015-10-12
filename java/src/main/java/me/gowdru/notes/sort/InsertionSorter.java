package me.gowdru.notes.sort;

import java.util.Arrays;
import java.util.Comparator;

/**
 * This implementation of {@link Sorter} uses insertion sort technique to sort items.
 */
public class InsertionSorter<T> implements Sorter<T> {

    /**
     * performs insertion sort on input items
     * @param items items to be sorted
     * @param comparator comparison assistant
     */
    public void sort(T[] items, Comparator<T> comparator) {
        int n = items.length;
        T tmp;
        //starting from 2nd element; 1st one is already sorted
        for (int i = 1; i < n; i++) {
            int j = i;
            tmp = items[i]; //Need to find new/correct place for this element in this iteration
            //traverse back till the edge of array, pushing the larger items down
            for (; j > 0 && comparator.compare(items[j - 1], tmp) > 0; j--) {
                //Item at 'j-1' is greater than 'j', so push it down
                items[j] = items[j-1];
            }
            items[j] = tmp; //Alas, the correct place
        }
    }
}
