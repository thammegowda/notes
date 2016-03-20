package me.gowdru.notes.graph;

import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.Set;
import java.util.TreeMap;

/**
 * Simple implementation of Prim's Algorithm.
 * Assumptions:
 * The nodes are numbered from 1 to N.
 * The cost of edges are integers
 * The edges are undirected
 * So the graph is undirected weighted
 */
public class PrimsAlgoSimple {

    public static class Link {
        int toNode;  int cost;
        public Link(int toNode, int cost){
            this.toNode = toNode; this.cost = cost;
        }
    }

    public static int findMST(Map<Integer, List<Link>> graph, int source) {
        int nVs = graph.size();
        Set<Integer> connected = new HashSet<>();
        connected.add(source);
        int mstCost = 0;
        while (connected.size() != nVs){
            // goal is to find next short Node
            int nextNode = 0;
            int minDist = Integer.MAX_VALUE;
            for (Integer connector : connected) {
                for (Link link : graph.get(connector)) {
                    if (connected.contains(link.toNode)) {
                        continue;//skip
                    }
                    if ( link.cost < minDist) {
                        minDist = link.cost;
                        nextNode = link.toNode;
                    }
                }
            }
            if (nextNode == 0) {
                // No more edges are possible
                // graph is disconnected
                break;
            }
            connected.add(nextNode);
            mstCost += minDist;
        }
        return mstCost;
    }

    public static void main(String[] args) throws FileNotFoundException {
        String input = "5 6\n" +
                "1 2 3\n" +
                "1 3 4\n" +
                "4 2 6\n" +
                "5 2 2\n" +
                "2 3 5\n" +
                "3 5 7\n" +
                "1";
        Scanner in = new Scanner(input);
        int nVs = in.nextInt();
        Map<Integer, List<Link>> graph = new TreeMap<>();
        for (int j = 1; j <= nVs; j++) {
            graph.put(j, new ArrayList<>());
        }
        int nEs = in.nextInt();
        for (int j = 0; j < nEs; j++) {
            int node1 = in.nextInt();
            int node2 = in.nextInt();
            int cost = in.nextInt();
            graph.get(node1).add(new Link(node2, cost));
            graph.get(node2).add(new Link(node1, cost));
        }
        int src = in.nextInt();

        int mstCost = findMST(graph, src);
        System.out.println(mstCost);
    }
}
