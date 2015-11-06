package me.gowdru.notes.text;

import org.junit.Test;

import java.util.Arrays;

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
}