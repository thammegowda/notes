package me.gowdru.notes.math.numtheory;

/**
 * Created by tg on 1/9/16.
 */
public class BaseConversion {

    public static int fromHexa(String hex) {
        return Integer.valueOf(hex, 0x10);
    }
    public static int fromOcta(String octa) {
        return Integer.valueOf(octa, 010); //8
    }

    public static int fromBinary(String binary) {
        return Integer.valueOf(binary, 0b10);
    }

    public static void main(String[] args) {
        System.out.println(fromBinary("11111"));
        System.out.println(fromHexa("1F"));
        System.out.println(fromOcta("37"));
    }

}
