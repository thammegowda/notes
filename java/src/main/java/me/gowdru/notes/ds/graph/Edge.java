package me.gowdru.notes.ds.graph;


/**
 * Edge Structure
 */
public class Edge<T, N> {

    private String label;
    private Node<N, T> head;
    private Node<N, T> tail;
    private T data;
    private double cost;
    private boolean directed = false;


    /**
     * Creates an undirected edge
     * @param head
     * @param tail
     */
    public Edge(Node<N, T> head, Node<N, T> tail) {
        this(head, tail, null, false);
    }

    public Edge(Node<N, T> head, Node<N, T> tail, T data, boolean directed) {
        this(head.getLabel() + (directed ? "->" : "<->") + tail.getLabel(), head, tail, directed);
        this.data = data;
    }

    public Edge(String label, Node<N, T> head, Node<N, T> tail, boolean directed) {
        this.label = label;
        this.head = head;
        this.tail = tail;
        head.addEdge(this);
        tail.addEdge(this);
        this.directed = directed;
    }

    public boolean isDirected() {
        return directed;
    }

    public void setDirected(boolean directed) {
        this.directed = directed;
    }

    public double getCost() {
        return cost;
    }

    public void setCost(double cost) {
        this.cost = cost;
    }

    public String getLabel() {
        return label;
    }

    public void setLabel(String label) {
        this.label = label;
    }

    public Node<N, T> getHead() {
        return head;
    }

    public void setHead(Node<N, T> head) {
        this.head = head;
    }

    public Node<N, T> getTail() {
        return tail;
    }

    public void setTail(Node<N, T> tail) {
        this.tail = tail;
    }

    public T getData() {
        return data;
    }

    public void setData(T data) {
        this.data = data;
    }

    @Override
    public String toString() {
        return  label +
               // tail.getLabel() + (directed ? " -> " : " <-> ") + head.getLabel() +
                " (" + cost + ")" +
                (data == null ? "" :  " : "+ data);
    }


    public Node<N, T> otherEnd(Node node){
        if (head.equals(node)){
            return tail;
        }
        if(tail.equals(node)){
            return head;
        }
        throw new IllegalArgumentException(node + " is not an end of "+ this);
    }
}
