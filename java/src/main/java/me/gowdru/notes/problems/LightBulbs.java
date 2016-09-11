package me.gowdru.notes.problems;

import java.util.BitSet;

public class LightBulbs extends BitSet {

    public boolean isLightOn(int idx) {
        return get(idx);
    }

    public void toggleState(int idx){
        set(idx, !isLightOn(idx));
    }

    public static void main(String[] args) {
        LightBulbs bulbs = new LightBulbs();
        System.out.println(bulbs.isLightOn(1));
        bulbs.toggleState(1);
        System.out.println(bulbs.isLightOn(1));
    }
}
