package me.gowdru.notes.math;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.HashMap;
import java.util.Map;

/**
 * Created by tg on 3/20/16.
 */
public class FastFactorial {

    public Map<Integer, BigInteger> memory = new HashMap<>();

    public BigInteger factorial(int n){
        if (n < 0){
           throw new IllegalArgumentException("Argument should be positive");
        }
        if (n == 1 || n == 0 ) {
            return BigInteger.ONE;
        }
        if (memory.containsKey(n)) {
            return memory.get(n);
        }
        BigInteger result = BigInteger.valueOf(n).multiply(factorial(n-1));
        memory.put(n, result);
        return result;
    }

    public static BigInteger stirlingsApprox(int n){
        //n! ~ sqrt(2*PI*n) * (n/e)^n
        BigDecimal factor1 = BigDecimal.valueOf(Math.sqrt(2 * Math.PI * n));
        BigDecimal factor2 = BigDecimal.valueOf(n / Math.E).pow(n);
        return factor1.multiply(factor2).toBigInteger();
    }

    public static void main(String[] args) {
        FastFactorial fact = new FastFactorial();
        for (int i = 1; i <= 20; i++) {
            BigInteger actual = fact.factorial(i);
            BigInteger approx = stirlingsApprox(i);
            System.out.printf("%d : %d = %d : %d \n", i, actual.subtract(approx), actual, approx);
        }
    }
}
