package me.gowdru.notes.ds;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Comparator;
import java.util.List;

/**
 * A generic PriorityQueue Data structure with configurable priorities and item types.
 *
 * Note: {@link ArrayList} is used to handle dynamic size of arrays.
 * @since March 12, 2016
 * @author Thamme Gowda N.
 */
public class PriorityQueue<T> {

    private final int n;
    private final List<T> array;
    private final Comparator<T> comparator;

    /**
     * Constructs a Priority Queue with specified number of children at each node.
     * @param n branch factor for heap
     * @param comparator priority comparator
     */
    public PriorityQueue(int n, Comparator<T> comparator) {
        this.n = n;
        this.comparator = comparator;
        this.array = new ArrayList<>(n);
        assert n >= 1: "Number of children should be positive";
    }

    /**
     * Inserts a new item to heap
     * @param item : the item to be inserted
     */
    public void insert(T item){
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
     * Adds all items to this priority Queue
     * @param items collection of items
     */
    public void addAll(Collection<T> items){
        items.forEach(this::insert);
    }

    /**
     * gets the minimum element from heap without removing it.
     * @return the minimum element
     */
    public T peekHead(){
        return this.array.get(0);
    }

    public T extractHead(){
        /*
         * procedure:
         * 1. extract the item at index 0,
         * 2. Move the last item to the position 0
         * 3. Heapify down from the root
         */
        T result = peekHead();
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
        T parent;
        T item = array.get(pos);
        while(pos > 0){
            parentPos = getParentIndex(pos);
            parent = array.get(parentPos);
            if (comparator.compare(parent, item) > 0){
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

        T minChild = this.array.get(firstChildIndex);
        int minChildPos = firstChildIndex;
        for (int i = firstChildIndex + 1; i <= lastChildIndex; i++){
            if (comparator.compare(this.array.get(i), minChild) < 0) {
                minChild = this.array.get(i);
                minChildPos = i;
            }
        }
        T item = this.array.get(pos);
        if (comparator.compare(minChild, item) < 0) {
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
