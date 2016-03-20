package me.gowdru.notes.ds.graph;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Map;

/**
 *
 * Graph Builder
 *
 */
public class GraphBuilder<N, E> {

    public static final String NODE_CMD = "^\\+node\\s*=\\s*";
    public static final String EDGE_CMD = "^\\+edge\\s*=\\s*";

    private Map<String, Node<N, E>> nodeIndex = new HashMap<>();
    private Graph<N, E> graph = new Graph<>();

    public Graph<N, E> read(InputStream stream) throws IOException {
        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(stream))){
            String line;
            while ((line = reader.readLine()) != null){
                line = line.trim();
                if (line.isEmpty() || line.startsWith("#")) {
                    continue; //skip
                }
                if (line.matches(NODE_CMD + ".*")){
                    readNodes(line);
                } else if (line.matches(EDGE_CMD + ".*")){
                    readEdge(line);
                }
            }
        }
        return graph;
    }

    private void readEdge(String line) {
        line = line.replaceAll(EDGE_CMD, "");
        String[] edges = line.split(";");
        for (String edgeCmd : edges) {
            makeEdge(edgeCmd);
        }
    }

    private void makeEdge(String edgeCmd) {
        edgeCmd =  edgeCmd.trim();
        double cost = 0;
        if(edgeCmd.contains(":")){
            String[] parts = edgeCmd.split(":");
            edgeCmd = parts[0].trim();
            cost = Double.valueOf(parts[1].trim());
        }
        boolean directed;
        String[] nodeNames;
        if(edgeCmd.contains("<->")){
            directed = false;
            nodeNames = edgeCmd.split("<->");
        } else if (edgeCmd.contains("->")) {
            directed = true;
            nodeNames = edgeCmd.split("->");
        } else {
            throw new RuntimeException("Invalid Edge format :" + edgeCmd);
        }
        assert nodeNames.length == 2;
        Node<N, E> fromNode = makeNode(nodeNames[0].trim());
        Node<N, E> toNode = makeNode(nodeNames[1].trim());
        Edge<E, N> edge = new Edge<>(toNode, fromNode);
        edge.setCost(cost);
        edge.setDirected(directed);
        graph.add(edge);
    }

    private void readNodes(String line) {
        line = line.replaceAll(NODE_CMD, "");
        String[] nodeNames = line.split(";");
        for (String nodeName : nodeNames) {
            makeNode(nodeName);
        }
    }

    private Node<N, E> makeNode(String nodeName) {
        nodeName = nodeName.trim();
        Node<N, E> node = nodeIndex.get(nodeName);
        if (node == null) {
            node = new Node<>(nodeName);
            nodeIndex.put(nodeName, node);
            graph.add(node);
        }
        return node;
    }

    public void reset(){
        nodeIndex.clear();
        graph = new Graph<>();
    }

}
