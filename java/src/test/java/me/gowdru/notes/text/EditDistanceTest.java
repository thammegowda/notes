package me.gowdru.notes.text;

import me.gowdru.notes.ds.Pair;
import org.junit.Test;

import java.util.Arrays;
import java.util.List;

/**
 * Created by tg on 11/6/15.
 */
public class EditDistanceTest {

    @Test
    public void testComputeDistance() throws Exception {
        EditDistanceComputer distance = new EditDistanceComputer("cat", "bat");
        int dist = distance.getDistance();
        assert dist == 1;
        assert 0 == new EditDistanceComputer("abcd", "abcd").getDistance();
        assert 4 == new EditDistanceComputer("abcd", "").getDistance();
        assert 4 == new EditDistanceComputer("", "abcd").getDistance();
        assert 1 == new EditDistanceComputer("abcd", "axcd").getDistance();
    }


    @Test
    public void testAlignment() throws Exception {
        EditDistanceComputer computer = new EditDistanceComputer("abbcd", "acbcdd");
        List<Pair<Integer, Integer>> poss = computer.findAlignment();
        System.out.println(poss);

        Pair<String, String> all = computer.getAlignment();
        System.out.println(all.getK());
        System.out.println(all.getV());
        assert 2 == computer.getDistance();
        computer.printMatrix();
    }
}