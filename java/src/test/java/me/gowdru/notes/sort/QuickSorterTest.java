package me.gowdru.notes.sort;

import org.junit.Test;

import java.util.Arrays;

import static org.junit.Assert.*;

/**
 * Created by tg on 3/12/16.
 */
public class QuickSorterTest {

    @Test
    public void testSort() throws Exception {
        QuickSorter<Integer> sorter = new QuickSorter<>();
        Integer[] input = {8, 7, 6, 5, 3, 2, 1};
        sorter.sort(input, (o1, o2) -> o1 - o2);
        Integer[] sorted = {1, 2, 3, 5, 6, 7, 8};
        assertArrayEquals(input, sorted);
    }
}