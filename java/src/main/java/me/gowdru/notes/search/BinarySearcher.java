package me.gowdru.notes.search;

/**
 * Implements Binary Search algorithm.
 * This implementation assumes input array to be sorted
 */
public class BinarySearcher<T extends Comparable> implements Searcher<T> {

    /**
     * Searches for {@code key} in {@code items} within the range of [{@code low}, {@code high}).
     * @param items - array of items
     * @param low the lower bound
     * @param high the higher bound
     * @param key search key
     * @return position > 0 if {@code key} is present is items; -1 when not found
     */
    private int search(T[] items, int low, int high, T key){
        System.out.println(">>" + low + ":" + high);
        int mid = (low + high) / 2;
        int comparison = key.compareTo(items[mid]);
        if (comparison == 0) {
            //base case
            return mid;
        } else if (low > high){
            //no more recursion possible
            //item not found
            return -1;
        } else if (comparison < 0) {
            //key is less than middle
            return search(items, low, mid - 1, key);
        } else {
            //key is greater than middle element
            return search(items, mid + 1, high, key);
        }
    }

    /**
     * Binary search algorithm
     * @param items - array of items
     * @param key - a key item whose position is to be determined
     * @return  position > 0 if {@code key} is present is items; -1 when not found
     */
    public int search(T[] items, T key) {
        return search(items, 0, items.length - 1, key);
    }
}
