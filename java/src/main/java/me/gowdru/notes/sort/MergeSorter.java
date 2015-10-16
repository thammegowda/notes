package me.gowdru.notes.sort;

import java.util.Arrays;
import java.util.Comparator;

/**
 * This implementation of {@link Sorter} uses merge sorting technique to sort items.
 */
public class MergeSorter<T> implements Sorter<T> {


    /**
     * performs merge sort
     * @param items items to be sorted
     * @param start the start index in array to consider for sorting
     * @param end the end marker in array (exclusive) to sort elements
     * @param comparator the comparison function
     * @param buffer buffer to be used for sorting
     */
    private void mergeSort(T[] items, int start, int end, Comparator<T> comparator, T[] buffer){
        //base case
        if (end - start < 2) {
            //reached the smallest sorted array, size 1
            return;
        }
        int middle = (start + end) / 2;
        mergeSort(items, start, middle, comparator, buffer);   //sort the first half
        mergeSort(items, middle, end, comparator, buffer); //sort the other half
        merge(items, start, middle, end, comparator, buffer);  //merge
        //update original array
        System.arraycopy(buffer, start, items, start, end - start);
    }

    /**
     * Merges parts by sorting them
     * @param items The array containing parts
     * @param start the begin index of part 1
     * @param middle the end index of part 1 and begin index of second part
     * @param end the end marker of second part
     * @param comparator the comparison function
     * @param buffer the buffer to be used for sorting
     */
    private void merge(T[] items, int start, int middle, int end,
                       Comparator<T> comparator, T[] buffer) {
        // going to copy elements from items[] to buffer[], [start:end-1]
        int leftHead = start;
        int rightHead = middle;
        for (int i = start; i < end; i++) {
            if (leftHead < middle &&   //elements remaining in left part and
                    (rightHead >= end   //either the right has no elements left
                            || comparator.compare(items[leftHead], items[rightHead]) < 0)){ //or left head is smaller
                buffer[i] = items[leftHead++];
            } else {
                buffer[i] = items[rightHead++];
            }
        }
    }

    /**
     * performs merge sort on input items
     * @param items items to be sorted
     * @param comparator comparison assistant
     */
    public void sort(T[] items, Comparator<T> comparator) {
        int n = items.length;
        T[] buffer = (T[]) new Object[n];
        mergeSort(items, 0, n, comparator, buffer);
    }

    public static void main(String[] args) {

        Integer[] items = {2, 3, 6, 7, 1, 0, 4, 5};
        Sorter<Integer> sorter = new MergeSorter<>();
        sorter.sort(items, Integer::compare);
        System.out.println(Arrays.toString(items));
    }
}
