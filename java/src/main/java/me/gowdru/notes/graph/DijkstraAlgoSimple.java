package me.gowdru.notes.graph;

import me.gowdru.notes.graph.DijkstraAlgorithm;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.Set;
import java.util.TreeMap;

/**
 * Simple implementation of Dijkstra's Algorithm.
 * This implementation is the kind I do in coding challenges ;-)
 * For the real generic implementation check {@link DijkstraAlgorithm}
 *
 * Assumptions:
 * The nodes are numbered from 1 to N.
 * The cost of edges are integers
 * The edges are undirected
 * So the graph is undirected weighted
 */
public class DijkstraAlgoSimple {

    public static class Link {
        int toNode;  int cost;
        public Link(int toNode, int cost){
            this.toNode = toNode; this.cost = cost;
        }
    }

    public static int[] shortestPath(Map<Integer, List<Link>> graph, int source) {
        int nVs = graph.size();
        int dist[] = new int[nVs + 1];
        for (int i = 1; i <= nVs; i++) { //all nodes have high value
            dist[i] = Integer.MAX_VALUE;
        }
        dist[source] = 0;
        Set<Integer> visited = new HashSet<>();
        visited.add(source);

        while (visited.size() != nVs){
            // goal is to find next short Node
            int nextNode = 0;
            int minDist = Integer.MAX_VALUE;
            for (Integer connector : visited) {
                for (Link link : graph.get(connector)) {
                    if (visited.contains(link.toNode)) {
                        continue;//skip
                    }
                    if (dist[connector] + link.cost < minDist) {
                        minDist = dist[connector] + link.cost;
                        nextNode = link.toNode;
                    }
                }
            }
            if (nextNode == 0) {
                // No more edges are possible
                // graph is disconnected
                break;
            }
            visited.add(nextNode);
            dist[nextNode] = minDist;
        }
        return dist;
    }

    public static void main(String[] args) throws FileNotFoundException {
        String input = "1\n" +
                "4 4\n" +
                "1 2 24\n" +
                "1 4 20\n" +
                "3 1 3\n" +
                "4 3 12\n" +
                "1";
        Scanner in = new Scanner(input);
        int t = in.nextInt();
        for (int i = 0; i < t; i++) {
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

            int[] dists = shortestPath(graph, src);
            //System.out.println(t);
            for (int j = 1; j <= nVs; j++) {
                if (j == src) {
                    continue;
                }
                if (dists[j] == Integer.MAX_VALUE) {
                    dists[j] = -1;
                }
                //System.out.printf("%d -> %d : %d\n", src, j, dists[j]);
                System.out.printf("%d ", dists[j]);
            }
            System.out.println();
        }
    }
}
