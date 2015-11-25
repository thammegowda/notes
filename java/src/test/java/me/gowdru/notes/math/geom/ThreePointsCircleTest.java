package me.gowdru.notes.math.geom;

import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Created by tg on 11/25/15.
 */
public class ThreePointsCircleTest {

    @Test
    public void testCenterOfCircle() throws Exception {
        double[] center = ThreePointsCircle.centerOfCircle(6, 0, 1, -5, 1, 5);
        assertEquals(1.0, center[0], 0.00);
        assertEquals(0.0, center[1], 0.00);

        center = ThreePointsCircle.centerOfCircle( 1, -5, 1, 5, -4, 0);
        assertEquals(1.0, center[0], 0.00);
        assertEquals(0.0, center[1], 0.00);
    }
}