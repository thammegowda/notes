package me.gowdru.notes.sort;

import java.util.Comparator;

/**
 * Quick Sort reference implementation with Lamuto Partition scheme
 *
 * @author Thamme Gowda N.
 * @since March 12, 2016
 */
public class QuickSorter<T> implements Sorter<T> {

    @Override
    public void sort(T[] items, Comparator<T> comparator) {
        sort(items, 0, items.length - 1, comparator);
    }

    public void sort(T[] a, int low, int high, Comparator<T> comparator){
        if ( low >= high) {
            // single element OR no elements, already sorted
            return;
        }
        int partition = lamutoPartition(a, low, high, comparator);
        sort(a, low, partition - 1, comparator);
        sort(a, partition + 1, high, comparator);
    }

    public int lamutoPartition(T[] a, int low, int high, Comparator<T> comparator){
        // assume pivot is the last element
        T pivot = a[high];
        int pos = low;
        // this position divides the array into
        // smaller-than-pivot and greater-than-pivot.
        // we start with leftmost pos, but eventually move it towards right.

        // loop over left to right, exclude pivot (pivot item will be exchanged at the end)
        for (int idx = low; idx <= high - 1; idx++){
            //Intuition: we are hoping to put pivot element to 'pos'.
            //          so, anything smaller than pivot should be left of 'pos'
            //          anything larger or equal to pivot shall be right of 'pos'
            //          That means, when a smaller item is seen, we move 'pos' to the right
            //              by adding it to left side.
            //          When a larger item is seen, 'pos' stays wherever it was
            if (comparator.compare(a[idx], pivot) < 0) {
                swap(a, pos, idx);
                pos++;
            }
        }

        // we found the place; so lets move pivot to its final place
        swap(a, pos, high);
        return pos;
    }

}
