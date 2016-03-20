package me.gowdru.notes.graph;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashSet;
import java.util.List;
import java.util.Scanner;
import java.util.Set;

/**
 *Implementation of Floyd Warshal's algo for all pairs shortest paths
 *
 *Assumptions:
 * weighted directed graph
 * vertex names starts from 1 to N
 *
 */
public class FloydsAlgoSimple {

    public static final int INFINITY = Short.MAX_VALUE;

    public static class Edge {
        int from, to, cost;
        public Edge(int from, int to, int cost){
            this.from = from; this.to = to; this.cost = cost;
        }
    }

    public static int[][] findShortestPaths(int nVs, List<Edge> edges) {

        int dists[][] = new int[nVs+1][nVs+1]; //+1 bcoz index starts from 1 in problem

        for (int i = 1; i <= nVs ; i++) { // all distances set to high value
            for (int j = 1; j <= nVs ; j++) {
                dists[i][j] = INFINITY;
            }
        }
        for (Edge edge : edges) { //directed paths initialized
            dists[edge.from][edge.to] = edge.cost;
        }

        for (int i = 1; i <= nVs ; i++) { // same node distance is zero
            dists[i][i] = 0;
        }
        // Dynamic programing begin
        for (int k = 1; k <= nVs; k++) { // connector node
            for (int i = 1; i <= nVs; i++) { //source node
                for (int j = 1; j <= nVs; j++) { // destination node
                    int newDist = dists[i][k] + dists[k][j];
                    if (dists[i][j]> newDist) { //pick this short distance connector
                        dists[i][j] = newDist;
                    }
                }
            }
        }
        return dists;
    }

    public static void main(String[] args) throws Exception {
        String input = "4 5\n" +
                "1 2 5\n" +
                "1 4 24\n" +
                "2 4 6\n" +
                "3 4 4\n" +
                "3 2 7\n" +
                "3\n" +
                "1 2\n" +
                "3 1\n" +
                "1 4";

        Scanner in = new Scanner(input);
        int nVs = in.nextInt();
        List<Edge> edges = new ArrayList<>();
        int nEs = in.nextInt();
        for (int j = 0; j < nEs; j++) {
            edges.add(new Edge(in.nextInt(), in.nextInt(), in.nextInt()));
        }
        int dists[][] = findShortestPaths(nVs, edges);
        int qs = in.nextInt();
        for (int i = 0; i < qs; i++) {
            int from = in.nextInt();
            int to = in.nextInt();
            int dist = dists[from][to];
            if (dist >= INFINITY) {
                dist = -1;
            }
            System.out.println(dist);
            //System.out.printf("%d -> %d = %d\n", from, to, dist);
        }

    }
}
