package me.gowdru.notes.search;

/**
 * Defines Contract for Searcher.
 */
public interface Searcher<T> {

    /**
     * search for position of @param key in @param items.
     * @param items - array of items
     * @param key - a key items whose position needs to be determines
     * @return position >= 0 :if found; -1 : if key not found in items
     */
    public int search(T[] items, T key);
}
