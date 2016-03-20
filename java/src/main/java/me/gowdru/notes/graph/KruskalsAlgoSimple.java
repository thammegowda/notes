package me.gowdru.notes.graph;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashSet;
import java.util.List;
import java.util.Scanner;
import java.util.Set;

/**
 * Created by tg on 3/20/16.
 */
public class KruskalsAlgoSimple {
    public static class Edge {
        int node1, node2, cost;
        public Edge(int node1, int node2, int cost){
            this.node1 = node1; this.node2 = node2; this.cost = cost;
        }
    }

    public static class Connection {
        private List<Set<Integer>> sets = new ArrayList<>();

        public boolean isConnected(int node1, int node2) {
            if (node1 == node2){
                return true;
            }
            for (Set<Integer> set : sets) {
                if (set.contains(node1) && set.contains(node2)){
                    return true;
                }
            }
            return false; // not connected
        }

        public void connect(int node1, int node2) {
            int first = -1; int second = -1;
            for (int i = 0; i < sets.size(); i++) {
                Set<Integer> set = sets.get(i);
                if (set.contains(node1)) {
                    first = i;
                }
                if (set.contains(node2)) {
                    second = i;
                }
            }
            if (first == second) {
                if (first == -1) {  // new component
                    Set<Integer> set = new HashSet<>();
                    set.add(node1); set.add(node2);
                    sets.add(set);
                    return;
                }
                throw new RuntimeException("Connecting the already connected! => cycle");
            }

            if (first == -1) { // grow second
                sets.get(second).add(node1);
            } else if (second == -1) { // grow first
                sets.get(first).add(node2);
            } else { // merge two
                sets.get(first).addAll(sets.get(second));
                sets.remove(second);
            }
        }
    }

    public static List<Edge> findMST(int nVs, List<Edge> graph, int source) {

        Connection connection = new Connection();
        Comparator<Edge> sorter = (e1, e2) -> {
            if (e1.cost == e2.cost) {
                // as per the problem description https://www.hackerrank.com/challenges/kruskalmstrsub
                return Integer.compare(e1.node1 + e1.cost + e1.node2,
                        e2.node1 + e2.cost + e2.node2);
            }
            return Integer.compare(e1.cost, e2.cost);
        };
        Collections.sort(graph, sorter);
        //connected.add(source);
        List<Edge> mst = new ArrayList<>();
        int i = 0;
        while (mst.size() < nVs && i < graph.size()){
            Edge next = graph.get(i);
            i++;
            if (connection.isConnected(next.node1, next.node2)){
                continue; //skip to avoid cycle
            }
            mst.add(next);
            connection.connect(next.node1, next.node2);
        }
        return mst;
    }

    public static void main(String[] args) throws Exception {
        String input = "4 5\n" +
                "1 2 1\n" +
                "3 2 150\n" +
                "4 3 99\n" +
                "1 4 100\n" +
                "3 1 200\n" +
                "4";
        Scanner in = new Scanner(input);
        int nVs = in.nextInt();
        List<Edge> edges = new ArrayList<>();
        int nEs = in.nextInt();
        for (int j = 0; j < nEs; j++) {
            edges.add(new Edge(in.nextInt(), in.nextInt(), in.nextInt()));
        }
        int src = in.nextInt();

        List<Edge> mst = findMST(nVs, edges, src);
        int cost = 0;
        //System.out.println();
        for (Edge edge : mst) {
            //System.out.println(edge.node1 + " - " + edge.node2 + " = " + edge.cost);
            cost += edge.cost;
        }
        System.out.println(cost);
    }
}
