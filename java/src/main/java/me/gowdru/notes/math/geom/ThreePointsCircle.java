package me.gowdru.notes.math.geom;

import java.util.Arrays;

/**
 *
 * This class has a solution for finding the centre and radius
 * of circle given the three points on circumference.
 *
 * @author  Thamme Gowda
 * @since Nov. 25, 2015
 */
public class ThreePointsCircle {


    /**
     * Computes distance between two points
     * @param x1 x coordinate of first point
     * @param y1 y coordinate of first point
     * @param x2 x coordinate of second point
     * @param y2 y coordinate of second point
     * @return distance between the points
     */
    public static double distance(double x1, double y1, double x2, double y2){
        // sqrt((y2-y1)^2 /  (x2-x1)^)
        return Math.sqrt( (Math.pow(y2 - y1, 2) + Math.pow(x2 - x1, 2)) );
    }

    /**
     * Finds center of circle given three points on circumference.
     * @param x1 x coordinate of first point on circumference
     * @param y1 y coordinate of first point on circumference
     * @param x2 x coordinate of second point on circumference
     * @param y2 y coordinate of second point on circumference
     * @param x3 x coordinate of third point on circumference
     * @param y3 y coordinate of second point on circumference
     * @return an array of three values. First two being the x,y coordinates of center. Third one is radius
     */
    public static double[] centerOfCircle(double x1, double y1,
                                          double x2, double y2,
                                          double x3, double y3) {
        //lets pick two lines
        // (x1,y1) -> (x2, y2)
        // (x2, y2) -> (x3,y3)

        //slopes of these two lines
        double m1 = (y2 - y1) / (x2 - x1);
        double m2 = (y3 - y2) / (x3 - x2);

        //mid points of these two lines
        double[] mid1 = {(x1 + x2)/2, (y1 + y2) / 2};
        double[] mid2 = {(x2 + x3)/2, (y2 + y3) / 2};

        // line perpendicular to these two lines are of form
        // y - mid[y] = - (1/m) * (x - mid[x])
        //y = mid[y]  - (1/m) * (x - mid[x])

        //we get two such lines,
        //y = mid1[y]  - (1/m1) * (x - mid1[x])
        //AND, y = mid2[y]  - (1/m2) * (x - mid2[x])

        // these lines intersect at the mid point of circle
        //so the mid point satisfies equations of both the perpendiculars!

        //mid1[1] - (x - mid1[0])/m1 = mid2[1] - (x - mid2[0])/m2;
        //mid1[1] - x/m1 + mid1[0])/m1 = mid2[1] -x/m2 + mid2[0])/m2;
        //- x/m1 + x/m2  = -mid1[1] + mid2[1] + mid2[0]/m2 - mid1[0]/m1;
        //x(-1/m1 + 1/m2) = -mid1[1] + mid2[1] + mid2[0]/m2 - mid1[0]/m1;
        double x = 1/((-1/m1 + 1/m2)) * (-mid1[1] + mid2[1] + mid2[0]/m2 - mid1[0]/m1);

        //with this x, solve y
        double y = mid1[1]  -(1/m1) * (x - mid1[0]);

        double radius1 = distance(x1, y1, x, y);
        double radius2 = distance(x2, y2, x, y);
        double radius3 = distance(x3, y3, x , y);
        assert radius1 == radius2;
        assert radius1 == radius3;
        return new double[]{x, y, radius1};
    }

    public static void main(String[] args) {
        double[] center = centerOfCircle(6, 0, 1, -5, 1, 5);
        System.out.println(Arrays.toString(center));
    }
}
