package me.gowdru.notes.tree;

import org.junit.Test;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import static org.junit.Assert.*;

/**
 * Created by tg on 10/24/15.
 */
public class BinarySearchTreeTest {

    @Test
    public void testInOrderTraverse() throws Exception {
        int items[] = {5 , 4, 6, 3 , 1, 2, 4, 8, 7, 9};
        BinarySearchTree bst = new BinarySearchTree(items);

        Arrays.sort(items);
        List<Integer> inorderList = bst.inOrderTraverse();
        for (int i = 0; i < items.length; i++) {
            assertEquals(items[i], inorderList.get(i).intValue());
        }
    }
}