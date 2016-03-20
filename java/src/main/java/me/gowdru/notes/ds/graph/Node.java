package me.gowdru.notes.ds.graph;

import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Objects;
import java.util.Set;
import java.util.SortedSet;
import java.util.TreeSet;
import java.util.stream.Collectors;

/**
 * Node Structure
 */
public class Node<T, E> {

    public static final Comparator<Edge<?, ?>> ASC_SORTER =
            (o1, o2) -> Double.compare(o2.getCost(), o1.getCost());
    private final String label;
    private T data;
    private SortedSet<Edge<E, T>> edges;
    public Comparator<Edge<?, ?>> edgeComparator = ASC_SORTER;

    public Node(String label) {
        this.label = label;
    }

    public Node(String label, T data) {
        this.label = label;
        this.data = data;
    }

    public String getLabel() {
        return label;
    }

    public T getData() {
        return data;
    }

    public void setData(T data) {
        this.data = data;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        Node<?, ?> node = (Node<?, ?>) o;

        return !(label != null ? !label.equals(node.label) : node.label != null);
    }

    @Override
    public int hashCode() {
        return label != null ? label.hashCode() : 0;
    }

    @Override
    public String toString() {
        return label + (data == null ? "" : ":" + data );
    }

    public Set<Edge<E, T>> getEdges() {
        return edges;
    }

    public void addEdge(Edge<E, T> edge) {
        if (!(Objects.equals(edge.getHead(), this)
                || Objects.equals(edge.getTail(), this))){
            throw new IllegalArgumentException("Unrelated edge:"
                    + edge.getLabel() + " to  node:" + label);
        }
        if (this.edges == null) {
            this.edges = new TreeSet<>(edgeComparator);
        }
        this.edges.add(edge);
    }

    public void addAllEdges(Collection<Edge<E, T>> edges) {
        edges.forEach(this::addEdge);
    }

    public List<Edge<E, T>> getOutwardEdges(){
        if (edges == null || edges.isEmpty()){
            return Collections.emptyList();
        }
        return getEdges().parallelStream()
                .filter(e -> !e.isDirected() || e.getTail().equals(this))
                .collect(Collectors.toList());
    }

}
