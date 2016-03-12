package me.gowdru.notes.ds;

import java.util.ArrayList;
import java.util.List;

/**
 * Min Heap Data structure using array.
 *
 * Note: {@link ArrayList} is used to handle dynamic size of arrays.
 */
public class MinHeap{

    private final int n;
    private List<Integer> array;

    /**
     * Creates a Min heap powered by complete binary tree using arrays.
     */
    public MinHeap() {
        this(2);
    }
    /**
     * Constructs a Min Heap with specified number of children at each node.
     * @param n branch factor of tree (Ex: 2 for binary tree)
     */
    public MinHeap(int n) {
        this.n = n;
        this.array = new ArrayList<>(n);
        assert n >= 1: "Number of children should be positive";
    }

    /**
     * Inserts a new item to heap
     * @param item : the item to be inserted
     */
    public void insert(int item){

        /*
          Procedure:
            1. Insert at the leaf,
            2. heapify up from the leap
         */
        this.array.add(item);
        int pos = this.array.size() - 1;
        this.heapifyUp(pos);
    }

    /**
     * gets the minimum element from heap without removing it.
     * @return the minimum element
     */
    public int peekMin(){
        return this.array.get(0);
    }

    public int extractMin(){
        /*
         * procedure:
         * 1. extract the item at index 0,
         * 2. Move the last item to the position 0
         * 3. Heapify down from the root
         */
        int result = peekMin();
        if (this.array.size() == 1) {
            // only root node
            this.array.clear();
        } else {
            this.array.set(0, this.array.remove(size() - 1)); //move last element to head
            this.heapifyDown(0); //heapify down
        }
        return result;
    }

    /**
     * gets the size of heap (i.e. number of elements in heap)
     * @return size of heap
     */
    public int size(){
        return this.array.size();
    }

    /**
     * checks if heap is empty
     * @return whether or not this heap is empty
     */
    public boolean isEmpty(){
        return this.array.isEmpty();
    }

    /**
     * Preserves heap property by balancing the element at the given pos with its parents
     * @param pos position from which the above portion shall be heapified
     */
    public void heapifyUp(int pos){
        int parentPos;
        Integer parent;
        Integer item = array.get(pos);
        while(pos > 0){
            parentPos = getParentIndex(pos);
            parent = array.get(parentPos);
            if (parent > item){
                array.set(pos, parent); //bring parent down
                pos = parentPos;
            } else {
                break; // done
            }
            //NOTE: recursive implementation would have made life simple :-(
        }
        this.array.set(pos, item);
    }

    /**
     * fixes heap property from a given position to bottom of heap
     * @param pos the position of item below which heap proprty needs to be fixed
     */
    public void heapifyDown(int pos){

        int firstChildIndex = getFirstChildIndex(pos);
        if (firstChildIndex >= size()){
            return; // no children , no need to heapify down
        }
        int lastChildIndex = Math.min(getLastChildIndex(pos), size() - 1);

        int minChild = this.array.get(firstChildIndex);
        int minChildPos = firstChildIndex;
        for (int i = firstChildIndex + 1; i <= lastChildIndex; i++){
            if (this.array.get(i) < minChild) {
                minChild = this.array.get(i);
                minChildPos = i;
            }
        }
        int item = this.array.get(pos);
        if (minChild < item) {
            //swap
            this.array.set(pos, minChild);
            this.array.set(minChildPos, item);
            heapifyDown(minChildPos);//recurse at minChildPos
        } //else we are done
    }

    /**
     * obtains the index of parent item in the heap
     * @param pos position of given item
     * @return parent item's position/index
     */
    public int getParentIndex(int pos){
        return (int) Math.floor((float)(pos - 1) / this.n);
    }

    /**
     * gets position/index of first child of node at given pos
     * @param pos position of given
     * @return position of first child of node
     */
    public int getFirstChildIndex(int pos){
        return pos * n + 1;
    }

    /**
     * gets position/index of last child of node at given pos
     * @param pos position of given
     * @return position of first child of node
     */
    public int getLastChildIndex(int pos){
        return getFirstChildIndex(pos) + n - 1; // first child followed by + remaining n-1 children
    }
}
