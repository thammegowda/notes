package me.gowdru.notes.problems;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

/**
 * You are given a graph with no cycles, each node representing different cities and there are stadiums for baseball games in all cities.
 Each node contains a value representing the population of the city, and a list of neighbors. (feel free to extend data structure)
 Every time there is a baseball game at a city, everyone from all the different cities will go to the city with the baseball game.
 Return the maximum traffic between a city and its neighbours when there is a game at that city, for all cities. (Does not have to be sorted)
 The total run-time after returning everything should be O(n).
 */
public class TrafficSolver {

    static class City {

        public final String label;
        public final int population;
        public final Set<City> neighbors = new HashSet<>();

        public City(String label, int population){
            this.population = population;
            this.label = label;
        }
    }

    private Map<String, Integer> cache = new HashMap<>();

    int findTraffic(City from, City to){
        String key = from.label + "-->" + to.label;
        //System.out.println(key);
        if (cache.containsKey(key)) {
            return cache.get(key);
        }
        int traffic = 0;
        for (City n : from.neighbors) {
            if (n.label.equals(to.label)) {continue;} //
            traffic += findTraffic(n, from);
        }
        traffic += from.population;
        cache.put(key, traffic);
        return traffic;

    }

    private int maxTraffic(City city){
        int traffic = 0;
        for (City n : city.neighbors) {
            traffic = Math.max(traffic, findTraffic(n, city));
        }
        return traffic;
    }

    public static void main(String[] args) {
        City[] cs = new City[6];
        for (int i = 1; i <= 5; i++) {
            City c = new City(""  + i, i);
            cs[i] = c;
        }

        for (int i = 1; i <= 4; i++) {
            cs[i].neighbors.add(cs[5]);
            cs[5].neighbors.add(cs[i]);
        }

        TrafficSolver solver = new TrafficSolver();
        for (int i = 1; i <= 5; i++) {
            int traff = solver.maxTraffic(cs[i]);
            System.out.println(i + " " + traff);
        }

    }

}
