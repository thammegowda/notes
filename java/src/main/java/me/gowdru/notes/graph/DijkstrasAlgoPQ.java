package me.gowdru.notes.graph;

import java.io.FileNotFoundException;
import java.util.Collection;
import java.util.HashMap;
import java.util.PriorityQueue;
import java.util.Scanner;

/**
 * @since 8/28/16
 */
public class DijkstrasAlgoPQ {

    static class Edges extends HashMap<Integer, Integer> {}

    static class Graph extends HashMap<Integer, Edges> {

        static final int INFINITY = Integer.MAX_VALUE;

        void addNode(int node){
            assert !containsKey(node);
            put(node, new Edges());
        }

        Collection<Entry<Integer, Integer>> getEdges(int node){
            return get(node).entrySet();
        }

        void addUndirectedEdge(int node1, int node2, int distance){
            assert containsKey(node1);
            assert containsKey(node2);
            assert distance >= 0;
            get(node1).put(node2, distance);
            get(node2).put(node1, distance);
        }

        int nodesCount(){
            return size();
        }

        int[] shortestPaths(int src){
            final int n = nodesCount();
            final class Node implements Comparable<Node> {
                final int label;
                int distance;
                boolean visited;

                public Node(int label, int distance){
                    this.label = label;
                    this.distance = distance;
                }

                @Override
                public int compareTo(Node o) {
                    return Integer.compare(this.distance, o.distance);
                }
            }

            final Node[] nodes = new Node[n+1];
            final PriorityQueue<Node> pq = new PriorityQueue<>();
            for (int i = 1; i <= n; i++) {
                int distance = i == src ? 0 : INFINITY;
                nodes[i] = new Node(i, distance);
                pq.add(nodes[i]);
            }
            while (!pq.isEmpty()) {
                Node next = pq.remove();
                if (next.visited) {
                    continue;
                }
                next.visited = true;
                for (Entry<Integer, Integer> toEdge: getEdges(next.label)){
                    Node toNode = nodes[toEdge.getKey()];
                    if (next.distance == INFINITY
                            || toEdge.getValue() == INFINITY) {
                        continue;
                    }
                    int distance = next.distance + toEdge.getValue();
                    if (distance < toNode.distance){
                        toNode.distance = distance;
                        pq.add(toNode);
                    }
                }
            }
            int dist[] = new int[n+1];
            for (int i = 1; i <= n; i++) {
                dist[i] = nodes[i].distance;
            }
            return dist;
        }
    }


    public static void main(String[] args) throws Exception {
        String input = "1\n" +
                "10 6\n" +
                "3 1\n" +
                "10 1\n" +
                "10 1\n" +
                "3 1\n" +
                "1 8\n" +
                "5 2\n" +
                "3";
        Scanner in = new Scanner(input);
        int t = in.nextInt();
        for (int i = 0; i < t; i++) {
            int nVs = in.nextInt();
            Graph graph = new Graph();

            for (int j = 1; j <= nVs; j++) {
                graph.addNode(j);
            }

            int nEs = in.nextInt();
            for (int j = 1; j <= nEs; j++) {
                int node1 = in.nextInt();
                int node2 = in.nextInt();
                //int cost = in.nextInt();
                int cost = 6;
                graph.addUndirectedEdge(node1, node2, cost);
            }
            int src = in.nextInt();
            int[] dists = graph.shortestPaths(src);
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