package me.gowdru.notes.ds.graph;


import java.util.HashSet;
import java.util.Set;

/**
 * Graph Structure
 */
public class Graph<N,E> {

    private String name;
    private final Set<Node<N, E>> nodes;
    private final Set<Edge<E, N>> edges;

    public Graph(){
        this(new HashSet<>(), new HashSet<>());
    }

    public Graph(Set<Node<N, E>> nodes, Set<Edge<E, N>> edges) {
        this.nodes = nodes;
        this.edges = edges;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Set<Node<N, E>> getNodes() {
        return nodes;
    }

    public Set<Edge<E, N>> getEdges() {
        return edges;
    }

    public void add(Node<N, E> node){
        nodes.add(node);
    }

    public void add(Edge<E, N> edge){
        edges.add(edge);
    }

    public int getNodesCount(){
        return this.nodes.size();
    }

    public int getEdgesCount(){
        return this.edges.size();
    }

    public Node<N, E> findNodeBylabel(String label){
        for (Node<N, E> node : nodes) {
            if (node.getLabel().equals(label)) {
                return node;
            }
        }
        return null;
    }

    @Override
    public String toString() {
        return "Graph{" +
                "name='" + name + '\'' +
                ", nodes=" + nodes +
                ", edges=" + edges +
                '}';
    }
}

