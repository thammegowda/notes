package me.gowdru.notes.tree;

import java.util.ArrayList;
import java.util.List;

/**
 * An implementation of Binary Search Tree
 * @author Thamme Gowda
 * @see me.gowdru.notes.tree.BinarySearchTree.BSTNode
 */
public class BinarySearchTree {

    /**
     * Binary search Tree node
     */
    private static class BSTNode {

        private List<Integer> values;
        private BSTNode parent;
        private BSTNode left;
        private BSTNode right;

        public BSTNode(int value, BSTNode parent) {
            this(new ArrayList<>(), parent);
            this.addValue(value);
        }
        public BSTNode(List<Integer> values, BSTNode parent) {
            this.values = values;
            this.parent = parent;
        }

        public List<Integer> getValues() {
            return values;
        }

        public void setValues(List<Integer> values) {
            this.values = values;
        }

        public void addValue(int value){
            if (this.values == null) {
                this.values = new ArrayList<>();
            }
            this.values.add(value);
        }

        public BSTNode getParent() {
            return parent;
        }

        public void setParent(BSTNode parent) {
            this.parent = parent;
        }

        public BSTNode getLeft() {
            return left;
        }

        public void setLeft(BSTNode left) {
            this.left = left;
        }

        public BSTNode getRight() {
            return right;
        }

        public void setRight(BSTNode right) {
            this.right = right;
        }

        /**
         * Inserts the argument value at right place in BST
         * @param value the new value to be inserted
         */
        public void insert(int value) {
            if (value == this.values.get(0)) {
                //belongs to same node
                this.addValue(value);
            } else if (value <= this.values.get(0)) {
                //should go left side
                if (this.left == null) {
                    //left sub tree not there yet
                    this.left = new BSTNode(value, this);
                } else {
                    //delegate the task to left sub tree
                    this.left.insert(value);
                }
            } else {
                //should go to the right side
                if (this.right == null) {
                    //right sub tree not there yet
                    this.right = new BSTNode(value, this);
                } else {
                    //delegate the task to right sub tree
                    this.right.insert(value);
                }
            }
        }


    }

    private BSTNode root;

    /**
     * Creates a BST containing argument items
     * @param items items to be inserted in BST
     */
    public BinarySearchTree(int items[]){
        if (items.length < 1) {
            throw new IllegalArgumentException("No items supplied");
        }
        for (int item : items) {
            this.insert(item);
        }
    }

    /**
     * recursively performs in-order traversal on nodes
     * @param node the current node
     * @param items buffer to which the values needs to be appended
     */
    private void inOrderTraverse(BSTNode node, List<Integer> items){
        // left sub tree first
        if (node.left != null) {
            inOrderTraverse(node.left, items);
        }
        // this node next
        if (node.values != null) {
            items.addAll( node.values);
        }
        //right side next
        if (node.right != null) {
            inOrderTraverse(node.right, items);
        }
    }

    /**
     * Retrieves all elements in tree by In-order traversal
     * @return list of all items from all nodes in this tree
     */
    public List<Integer> inOrderTraverse(){
        if (this.root == null) {
            return null;
        }
        List<Integer> inOrderList = new ArrayList<>();
        this.inOrderTraverse(this.root, inOrderList);
        return inOrderList;
    }

    /**
     * Inserts a value into BST
     * @param value the new value to be inserted
     */
    public void insert(int value) {
        //if root is missing, create root
        if (this.root == null) {
            this.root = new BSTNode(value, null);
        } else {
            //else tell root node to (recursively) find a place for this new value
            this.root.insert(value);
        }
    }

    public static void main(String[] args) {
        int items[] = {5 , 4, 6, 3 , 1, 2, 4, 8, 7, 9};
        BinarySearchTree bst = new BinarySearchTree(items);
        System.out.println(bst);
        //NOTE: use debugger to analyse the structure of 'bst' object

        System.out.println("In order :");
        System.out.println(bst.inOrderTraverse());

    }
}
