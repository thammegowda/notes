package me.gowdru.notes.math;

/**
 * Created by tg on 10/15/15.
 */
public class GCD {


    /**
     * Finds GCD by iterative way
     * @param num1 - num1
     * @param num2 - num2
     * @return GCD
     */
    public static long gcdIterative(long num1, long num2){
        //lets store larger one in num1, because we need to find modulus
        long tmp;
        if (num2 > num1) {
            tmp = num1;
            num1 = num2;
            num2 = tmp;
        }
        do {
            tmp = num2;
            num2 = num1 % num2;
            num1 = tmp;
        } while (num2 != 0);

        return num1;
    }


    /**
     * Finds GCD in recursive way
     * @param num1 - num1
     * @param num2 - num2
     * @return GCD of num1 and num2
     */
    public static long gcdRecursive(long num1, long num2){
        //lets store larger one in num1, because we need to find modulus
        if (num1 == 0) {
            return num2;
        } else if (num2 == 0){
            return num1;
        } else if (num1 > num2) {
            return gcdRecursive(num2, num1 % num2);
        } else {
            return gcdRecursive(num1, num2 % num1);
        }
    }

}
