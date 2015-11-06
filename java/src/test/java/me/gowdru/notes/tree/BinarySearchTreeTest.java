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
    public void testAll() throws Exception {
        int items[] = {5, 4, 6, 3, 1, 2, 4, 8, 7, 9};
        BinarySearchTree bst = new BinarySearchTree(items);

        int depths[] = {0, 1, 1, 2, 3, 4, 1, 2, 3, 3};
        //validate structure
        for (int i = 0; i < items.length; i++) {
            assertEquals(depths[i], bst.findDepth(items[i]));
        }
        assertEquals(-1 , bst.findDepth(100)); // not found

        Arrays.sort(items);
        //test inorder traversal
        List<Integer> inorderList = bst.inOrderTraverse();
        for (int i = 0; i < items.length; i++) {
            assertEquals(items[i], inorderList.get(i).intValue());
        }
        assertEquals(9, bst.countNodes());
        assertEquals(10, bst.size());
        assertEquals(4, bst.findHeight());




    }
}