package me.gowdru.notes.math;

import java.io.*;
import java.util.*;
/**
 * Created by tg on 3/20/16.
 */
public class FractionReducer {

    public static class Fraction {
        public int n, d;
        public Fraction(int n, int d){
            this.n = n; this.d = d;
        }
        @Override
        public String toString(){
            return String.format("%d/%d", n, d);
        }
    }

    public static int lcm(int a, int b){
        int max = a, min = b;
        if (a < b){
            min = a;
            max = b;
        }
        int lcm = max;
        while(lcm % min != 0){
            lcm += max;
        }
        return lcm;
    }

    public static int lcm(int...ns){
        if(ns.length == 1){
            return ns[0];
        }
        int lcm = lcm(ns[0], ns[1]);
        for(int i=2; i <ns.length; i++){
            lcm = lcm(lcm, ns[i]);
        }
        return lcm;
    }

    public static int gcd(int a, int b){
        while (b != 0) {
            int tmp = a % b;
            a = b;
            b = tmp;
        }
        return a;
    }

    public static int gcd(int...ns){
        int gcd = gcd(ns[0], ns[1]);
        for(int i=2; i <ns.length; i++){
            gcd = gcd(gcd, ns[i]);
        }
        return gcd;
    }

    public static Fraction sum(List<Fraction> fractions){
        //denominators = LCM of denominnators
        int ds[] = new int[fractions.size()];
        for (int i = 0; i < fractions.size(); i++) {
            ds[i] = fractions.get(i).d;
        }
        int lcm = lcm(ds);

        //numerator = (LCM/denominator)*numerator + .....
        int numr = 0;
        for (Fraction fraction : fractions) {
            numr += (lcm / fraction.d) * fraction.n;
        }
        int gcd = gcd(numr, lcm);
        return new Fraction(numr/gcd, lcm/gcd);
    }


    public static void main(String[] args) {

        String src = "1\n" +
                "3\n" +
                "4 5\n" +
                "2 1\n" +
                "1 3";
        Scanner in = new Scanner(src);
        int t = in.nextInt();
        for (int i = 0; i < t; i++) {
            int n = in.nextInt();
            List<Fraction> fractions = new ArrayList<>();
            for (int j = 0; j < n; j++){
                fractions.add(new Fraction(in.nextInt(), in.nextInt()));
            }
            Fraction reduced = sum(fractions);
            System.out.println(reduced);
        }
    }
}
