package me.gowdru.notes.search;

import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Test case for {@link LinearSearcher}
 */
public class LinearSearcherTest {

    @Test
    public void testSearch() throws Exception {

        Integer[] items = {1,2,3,4,5,6,7};
        LinearSearcher<Integer> searcher = new LinearSearcher<Integer>();
        assertEquals(4, searcher.search(items, 5));
        assertEquals(6, searcher.search(items, 7));
        assertEquals(0, searcher.search(items, 1));
        assertEquals(-1, searcher.search(items, 10));
        assertEquals(-1, searcher.search(items, -1));
    }
}