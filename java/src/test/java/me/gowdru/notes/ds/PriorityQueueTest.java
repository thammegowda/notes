package me.gowdru.notes.ds;

import org.junit.Test;

import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

import static org.junit.Assert.*;

/**
 * Created by tg on 3/12/16.
 */
public class PriorityQueueTest {

    @Test
    public void testPQ() throws Exception {
        List<Integer> data = Arrays.asList(8, 7, 1, 2, 6, 9, 10, -1, -20);

        Comparator<Integer> ascending = (o1, o2) -> o1 - o2;
        Comparator<Integer> descending = (o1, o2) -> o2 - o1;
        PriorityQueue<Integer> queue = new PriorityQueue<>(2, ascending);
        queue.addAll(data);
        Collections.sort(data, ascending);
        assertEquals(data.size(), queue.size());
        for (Integer item : data) {
            assertEquals(item, queue.extractHead());
        }

        queue = new PriorityQueue<>(2, descending);
        queue.addAll(data);
        Collections.sort(data, descending);
        assertEquals(data.size(), queue.size());

        for (Integer item : data) {
            assertEquals(item, queue.extractHead());
        }
    }
}