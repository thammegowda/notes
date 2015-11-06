package me.gowdru.notes.math;

import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Created by tg on 10/15/15.
 */
public class GCDTest {

    @Test
    public void testGcdIterative() throws Exception {
        assertEquals(5, GCD.gcdIterative(10, 5));
        assertEquals(2, GCD.gcdIterative(2, 6));
        assertEquals(8, GCD.gcdIterative(24, 16));
    }

    @Test
    public void testGcdRecursive() throws Exception {
        assertEquals(5, GCD.gcdRecursive(10, 5));
        assertEquals(2, GCD.gcdRecursive(2, 6));
        assertEquals(8, GCD.gcdRecursive(24, 16));
    }
}