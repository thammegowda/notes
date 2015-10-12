package me.gowdru.notes.sort;

import org.junit.Test;

import java.util.Arrays;

import static org.junit.Assert.*;

/**
 * Test Case for insertion sort
 */
public class InsertionSorterTest {

    @Test
    public void testSort() throws Exception {
        Integer[] items = {2, 3, 6, 7, 1, 0, 4, 5};
        Sorter<Integer> sorter = new InsertionSorter<>();
        sorter.sort(items, Integer::compare);
        for (int i = 0; i < items.length - 1; i++) {
            assertTrue(items[i] <= items[i+1]);
        }
    }
}