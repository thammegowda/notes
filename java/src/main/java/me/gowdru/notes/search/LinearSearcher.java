package me.gowdru.notes.search;

/**
 *
 * This class implements Linear search algorithm
 */
public class LinearSearcher<T> implements Searcher<T> {

    /**
     * performs linear search
     * @param items - array of items
     * @param key - a key item whose position is to be determined
     * @return value > 0 if position found; -1 if not found
     */
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
