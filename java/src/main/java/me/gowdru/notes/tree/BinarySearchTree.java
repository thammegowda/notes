package me.gowdru.notes.tree;

import sun.reflect.generics.reflectiveObjects.NotImplementedException;

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

        public int getValue(){
            return getValues().get(0);
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
    }

    private BSTNode root;

    public BinarySearchTree(){

    }
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
            BSTNode node = this.root;
            while (true){
                if (value == node.getValues().get(0)) {
                    //found the place. duplicate value
                    node.addValue(value);
                    break;
                } else if (value < node.getValues().get(0)) {
                    //no left tree, create one
                    if (node.getLeft() == null) {
                        //found the place
                        node.setLeft(new BSTNode(value, node));
                        break;
                    } else {
                        node = node.getLeft();
                    }
                } else {
                    if (node.getRight() == null) {
                        //found the place
                        //no right tree, create one
                        node.setRight(new BSTNode(value, node));
                        break;
                    } else {
                        node = node.getRight();
                    }
                }
            }
        }
    }

    /**
     * Counts number of nodes in the tree
     * @return number of nodes in the tree
     */
    public long countNodes(){
        return countChildNodes(this.root);
    }

    /**
     * Counts the number of child nodes including given node
     * @param node the root of sub tree
     * @return number of nodes, duplicates excluded
     */
    private long countChildNodes(BSTNode node) {
        if (node == null) {
            return 0;
        }
        // left + this + right
        return countChildNodes(node.getLeft()) + 1
                + countChildNodes(node.getRight());
    }


    /**
     * Counts number of values inserted into the tree
     * @return number of value items inserted
     */
    public int size() {
        return countChildElements(this.root);
    }

    /**
     * Counts number of child elements, treats duplicates as separate values
     * @param node the root of subtree
     * @return number of values including duplicates
     */
    private int countChildElements(BSTNode node){
        if (node == null) {
            return 0;
        }
        // left + this + right
        return countChildElements(node.getLeft())
                +  node.getValues().size()
                + countChildElements(node.getRight());
    }

    /**
     * Finds the total height of tree
     * @return height of tree
     */
    public int findHeight(){
        //root is zero
        return findHeight(this.root) - 1;
    }

    /**
     * recursively finds height of subtree starting at given node
     * @param node root of sub tree
     * @return height of sub tree
     */
    private int findHeight(BSTNode node){
        if (node == null) {
            return 0;
        }
        //this node (1) + longest sub tree (it could be on left side or right side)
        return 1 + Math.max(findHeight(node.getLeft()), findHeight(node.getRight()));
    }

    /**
     * finds the depth of the node having given value
     * @param value the value whose depth needs to be computed
     * @return the depth of node containing given value
     */
    public int findDepth(int value) {
        int depth = 0;
        //start from root
        BSTNode node = this.root;
        while (node != null) {
            if (value == node.getValues().get(0)){
                //found
                return depth;
            }
            //move down
            depth++;
            // decide left or right
            node = value < node.getValues().get(0) ? node.getLeft() : node.getRight();
        }
        // not found
        return -1;
    }


    /**
     * tells if the tree is empty or not
     * @return true if there are no nodes in the ree
     */
    public boolean isEmpty(){
        return this.root == null;
    }

    /**
     * Finds the min node in the tree
     * @return the node with least value
     */
    private BSTNode findMinNode() {
        BSTNode node;
        //traverse left
        for (node = this.root; node.getLeft() != null; node = node.getLeft());
        return node;
    }

    /**
     * Finds the max node in the tree
     * @return the node with highest value
     */
    private BSTNode findMaxNode() {
        BSTNode node;
        //traverse right
        for (node = this.root; node.getRight() != null; node = node.getRight());
        return node;
    }

    private void delete(int val) {
        //find node
        BSTNode node = this.root;
        while (node != null && node.getValue() != val) {
            node = val < node.getValue()? node.getLeft() : node.getRight();
        }
        if (node != null) {
            //found the node
            //FIXME: implement
            throw new NotImplementedException();
        }
    }

    public static void main(String[] args) {
        int items[] = {5, 4, 6, 3, 1, 2, 4, 8, 7, 9};
        BinarySearchTree bst = new BinarySearchTree(items);
        System.out.println(bst);
        //NOTE: use debugger to analyse the structure of 'bst' object

        System.out.println("In order :");
        //System.out.println(bst.inOrderTraverse());
        //System.out.println(bst.countNodes());
        //System.out.println(bst.countValues());
        System.out.println(bst.findHeight());
        for (int item : items) {
            System.out.println(item + ":" + bst.findDepth(item));
        }


    }
}
