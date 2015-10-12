package me.gowdru.notes.search;

import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Created by tg on 10/12/15.
 */
public class BinarySearcherTest {

    @Test
    public void testSearch() throws Exception {

        Integer[] items = {1,2,3,4,5,6,7};
        Searcher<Integer> searcher = new BinarySearcher<Integer>();
        assertEquals(4, searcher.search(items, 5));
        assertEquals(6, searcher.search(items, 7));
        assertEquals(0, searcher.search(items, 1));
        assertEquals(-1, searcher.search(items, 10));
        assertEquals(-1, searcher.search(items, -1));
    }

}