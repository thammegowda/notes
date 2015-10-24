package me.gowdru.notes.ir.vsm;

import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Created by tg on 10/23/15.
 */
public class VectorTest {

    @Test
    public void testDotProduct() throws Exception {

        //lets alias x,y,z = 1,2,3
        // say v1 = x + 2y + 3z
        // say v2 = 2x + y + z
        // v1.v2 = 2 + 2 + 3 = 7
        Vector v1 = new Vector("v1");
        v1.dimensions = new long[]{1, 2, 3};
        v1.scales = new double[] {1.0, 2.0, 3.0};

        Vector v2 = new Vector("v2");
        v2.dimensions = new long[]{1, 2, 3};
        v2.scales = new double[] {2.0, 1.0, 1.0};

        assertEquals(7.0, v1.dotProduct(v2), 0.000000);

        v1 = new Vector("v1");
        v1.dimensions = new long[]{1, 2};
        v1.scales = new double[] {1.0, 2.0};

        v2 = new Vector("v2");
        v2.dimensions = new long[]{1, 3};
        v2.scales = new double[] {2.0, 3.0};
        assertEquals(2.0, v1.dotProduct(v2), 0.0000);




    }
}