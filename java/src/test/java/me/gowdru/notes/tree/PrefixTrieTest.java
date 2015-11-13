package me.gowdru.notes.tree;

import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Created by tg on 11/13/15.
 */
public class PrefixTrieTest {

    @Test
    public void testPrefixCount() throws Exception {
        PrefixTrie root = PrefixTrie.newRoot();
        String strs[] = new String[] {
                "abcd",
                "abcdef",
                "abcdefgh",
                "pqrs",
                "12345",
                "a12345"
        };
        for (String str : strs) {
            root.insert(str);
        }
        assertEquals(6, root.getCount());
        assertEquals(6, root.countPrefixPaths(""));
        assertEquals(4, root.countPrefixPaths("a"));
        assertEquals(3, root.countPrefixPaths("abcd"));
        assertEquals(2, root.countPrefixPaths("abcdef"));
        assertEquals(1, root.countPrefixPaths("abcdefgh"));
        assertEquals(1, root.countPrefixPaths("1"));
        assertEquals(0, root.countPrefixPaths("11221312321"));
        assertEquals(0, root.countPrefixPaths("abcdefghijkl"));

    }
}