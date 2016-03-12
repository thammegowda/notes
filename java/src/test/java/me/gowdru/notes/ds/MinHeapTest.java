package me.gowdru.notes.ds;

import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Created by tg on 3/11/16.
 */
public class MinHeapTest {


    @Test
    public void testHeap() throws Exception {
        MinHeap heap = new MinHeap();
        heap.insert(6);
        heap.insert(4);
        assertEquals(4, heap.peekMin());
        heap.insert(5);
        assertEquals(3, heap.size());
        assertFalse(heap.isEmpty());
        assertEquals(4, heap.peekMin());
        heap.insert(3);
        assertEquals(3, heap.peekMin());
        heap.insert(1);
        assertEquals(1, heap.peekMin());
        heap.insert(8);
        assertEquals(1, heap.peekMin());
        heap.insert(2);
        assertEquals(1, heap.peekMin());
        assertEquals(1, heap.extractMin());
        assertEquals(2, heap.extractMin());
        assertEquals(3, heap.extractMin());
        assertEquals(4, heap.peekMin());
        assertEquals(4, heap.extractMin());
        assertEquals(5, heap.extractMin());
        assertEquals(6, heap.extractMin());
        assertEquals(8, heap.extractMin());
        assertEquals(0, heap.size());
        assertTrue(heap.isEmpty());

    }
}