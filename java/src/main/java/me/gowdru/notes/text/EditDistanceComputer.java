package me.gowdru.notes.text;


import me.gowdru.notes.ds.Pair;

import java.util.LinkedList;
import java.util.List;

/**
 *
 * Implementation of string edit distance(Levenshtein distance) in java.
 * <p>
 * <b>References : </b><br/>
 * This algorithm is taken from "IR-Book" :
 * C. Manning et al. (2008). Introduction to Information Retrieval [Online].
 * Available: http://www-nlp.stanford.edu/IR-book/ <br/>
 * http://nlp.stanford.edu/IR-book/html/htmledition/edit-distance-1.html
 * </p>
 *
 */
public class EditDistanceComputer {

    private static final char PAD_CHAR = ' ';
    private String s1;
    private String s2;
    private char[] str1;
    private char[] str2;
    private int[][] m;
    private List<Pair<Integer, Integer>> alignments;
    private int replacementCost = 1;

    public EditDistanceComputer(String s1, String s2) {
        this.str1 = (" " + s1).toCharArray(); //making space for base case
        this.str2 = (" " + s2).toCharArray();
        this.s1 = s1;
        this.s2 = s2;
    }

    public String getString1() {
        return s1;
    }

    public String getString2() {
        return s2;
    }

    /**
     * Computes edit distance matrix
     */
    private void computeMatrix() {
        this.m = new int[str1.length][str2.length];
        for (int i = 1; i < str1.length; i++) {
            m[i][0] = i;
        }
        for (int j = 1; j < str2.length; j++) {
            m[0][j] = j;
        }
        for (int i = 1; i < str1.length; i++) {
            for (int j = 1; j < str2.length; j++) {
                //minimum of row move(insert), column move(delete), diagonal move(same or replace)
                m[i][j] = Math.min(Math.min(m[i - 1][j] + 1, m[i][j - 1] + 1),
                        m[i - 1][j - 1] + (str1[i] == str2[j] ? 0 : replacementCost));
            }
        }
    }

    /**
     * Gets edit distance between strings
     *
     * @return the minimum edit distance
     */
    public int getDistance() {
        return getMatrix()[str1.length - 1][str2.length - 1];
    }

    /**
     * Gets matrix
     *
     * @return edit distance matrix
     */
    public synchronized int[][] getMatrix() {
        if (this.m == null) {
            computeMatrix();
        }
        return m;
    }

    /**
     * Finds string alignment between two strings
     * @return alignment positions for minimum edit distance
     */
    public List<Pair<Integer, Integer>> findAlignment() {
        if (alignments == null) {
            int[][] m = getMatrix();
            List<Pair<Integer, Integer>> positions = new LinkedList<>();
            int i = str1.length - 1;
            int j = str2.length - 1;
            while (i > 0 || j > 0) {
                positions.add(0, new Pair<>(i, j));
                //base case,
                if (i == 0 || j == 0) {
                    if (i == 0) {
                        j--;
                    } else {
                        i--;
                    }
                    continue;
                }
                int min = Math.min(Math.min(m[i - 1][j], m[i][j - 1]), m[i - 1][j - 1]);
                if (min == m[i - 1][j - 1]) {
                    //min is diagonal
                    i--;
                    j--;
                } else if (min == m[i - 1][j]) {
                    //min is next row cell
                    i--;
                } else {
                    //min is next col cell
                    j--;
                }
            }
            this.alignments = positions;
        }
        return this.alignments;
    }

    /**
     * Gets aligned strings
     * @return aligned strings
     */
    public Pair<String, String> getAlignment(){
        return getAlignment(PAD_CHAR);
    }

    /**
     * Prints edit distance matrix
     */
    public void printMatrix(){
        int[][] matrix = getMatrix();
        System.out.printf("%2c", '+');
        for (char aStr2 : str2) {
            System.out.printf("%4c", aStr2);
        }
        System.out.println();

        for (int i = 0; i < matrix.length; i++) {
            int[] row = matrix[i];
            System.out.printf("%2c", str1[i]);
            for (int j = 0; j < row.length; j++) {
                System.out.printf("%4d", matrix[i][j]);
            }
            System.out.println();
        }
    }

    /**
     * gets aligned strings
     * @param padChar padding character for alignment
     * @return a pair of aligned strings
     */
    public Pair<String, String> getAlignment(char padChar){
        List<Pair<Integer, Integer>> poss = findAlignment();
        StringBuilder buffer = new StringBuilder();

        buffer.append(str1[poss.get(0).getK()]);
        for (int i = 1; i < poss.size(); i++) {
            char c = poss.get(i).getK().equals(poss.get(i - 1).getK()) ? padChar : str1[poss.get(i).getK()];
            buffer.append(c);
        }
        String firstString = buffer.toString();

        buffer.setLength(0);
        buffer.append(str2[poss.get(0).getV()]);
        for (int i = 1; i < poss.size(); i++) {
            char c = poss.get(i).getV().equals(poss.get(i - 1).getV()) ? padChar : str2[poss.get(i).getV()];
            buffer.append(c);
        }
        return Pair.create(firstString, buffer.toString());
    }

    public static void main(String[] args) {
        //args = "hello thello".split(" ");
        if (args.length != 2) {
            System.err.println("Invalid args !");
            System.out.println("USAGE : <Str1> <Str2>");
            return;
        }

        EditDistanceComputer computer = new EditDistanceComputer(args[0], args[1]);
        computer.printMatrix();
        System.out.println("Alignment : " + computer.findAlignment());
        Pair<String, String> pair = computer.getAlignment();
        System.out.println(">" + pair.getFirst());
        System.out.println(">" + pair.getSecond());
        System.out.println("Edit distance : " + computer.getDistance());
    }
}
