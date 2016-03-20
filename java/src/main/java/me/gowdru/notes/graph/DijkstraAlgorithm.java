package me.gowdru.notes.graph;

import me.gowdru.notes.ds.graph.Edge;
import me.gowdru.notes.ds.graph.Graph;
import me.gowdru.notes.ds.graph.GraphBuilder;
import me.gowdru.notes.ds.graph.Node;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Created by tg on 2/3/16.
 */
public class DijkstraAlgorithm {

    public static void findShortestPath(Collection<Node> nodes, Node source){

        Set<Node> visited = new HashSet<>();
        Map<Node, Node> connection = new HashMap<>();
        Map<Node, Double> distance = new HashMap<>();
        for (Node node : nodes) {
            distance.put(node, (double) Integer.MAX_VALUE);
        }

        //source is visited
        distance.put(source, 0d);
        visited.add(source);

        while (visited.size() != nodes.size()) {
            double minCost = Integer.MAX_VALUE;
            Edge minEdge = null;
            Node connector = null;
            for (Node<?, ?> node : visited) {
                double connectingCost = distance.get(node);
                for (Edge edge : node.getOutwardEdges()) {
                    Node candidateNode = edge.otherEnd(node);
                    //skip already visited nodes
                    if (visited.contains(candidateNode)) {
                        continue;//skip
                    }
                    if (connectingCost + edge.getCost() < minCost) {
                        minCost = connectingCost + edge.getCost();
                        minEdge = edge;
                        connector = node;
                    }
                }
            }
            if (minEdge == null) {
                throw new RuntimeException("Graph is not connected");
            }
            Node nextNode = minEdge.otherEnd(connector);
            visited.add(nextNode);
            distance.put(nextNode, minCost);
            connection.put(nextNode, connector);
        }

        //Print output
        for (Node node : distance.keySet()) {
            List<Node> path = new ArrayList<>();
            for(Node current = node; current != null; current = connection.get(current)){
                path.add(0, current);
            }
            System.out.println(source.getLabel() + " -> " + node.getLabel()
                    + " Distance=" + distance.get(node)
                    + "\t Path:" + path);
        }
    }


    public static void main(String[] args) throws IOException {
        Graph graph;
        String file = "data/graph/connected-undirected.graph";
        try (FileInputStream stream = new FileInputStream(file)) {
            graph = new GraphBuilder<Object, Integer>().read(stream);
        }
        Node from = graph.findNodeBylabel("1");
        System.out.println(graph);
        findShortestPath(graph.getNodes(), from);
    }

}
