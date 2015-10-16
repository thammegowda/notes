package me.gowdru.notes.sort;

import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Created by tg on 10/14/15.
 */
public class MergeSorterTest {

    @Test
    public void testSort() throws Exception {
        Integer[] items = {2, 3, 6, 7, 1, 0, 4, 5};
        Integer[] sorted = {0, 1, 2, 3, 4, 5, 6, 7};
        Sorter<Integer> sorter = new MergeSorter<>();
        sorter.sort(items, Integer::compare);
        for (int i = 0; i < items.length - 1; i++) {
            assertEquals(sorted[i], items[i]);
        }
    }
}