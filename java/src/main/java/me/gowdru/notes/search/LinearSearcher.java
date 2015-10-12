package me.gowdru.notes.search;

/**
 *
 * This class implements Linear search algorithm
 */
public class LinearSearcher<T> implements Searcher<T> {

    public int search(T[] items, T key) {
        //for all the elements in array,
        // scanning from one end to another linearly
        for (int i = 0; i < items.length; i++) {
            if (items[i].equals(key)){
                //found! return position
                return i;
            }
        }
        // Not found
        return -1;
    }
}
