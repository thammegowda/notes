package me.gowdru.notes.ds;

/**
 * Data Structure for a pair values
 */
public class Pair<K, V> {

    private final K k;
    private final V v;

    public Pair(K k, V v) {
        this.k = k;
        this.v = v;
    }

    public K getFirst(){
        return k;
    }
    public K getK() {
        return k;
    }

    public V getSecond(){
        return v;
    }

    public V getV() {
        return v;
    }

    @Override
    public String toString() {
        return "(" + k + "," + v + ')';
    }

    public static <K,V> Pair<K,V> create(K k, V v){
        return new Pair<>(k,v);
    }
}
