package me.gowdru.notes.text;

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

    private char[] str1;
    private char[] str2;
    private int[][] m;

    public EditDistanceComputer(String s1, String s2){
        this.str1 = (" " + s1).toCharArray(); //making space for base case
        this.str2 = (" " + s2).toCharArray();
    }

    /**
     * Computes edit distance matrix
     */
    private void computeMatrix(){
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
                m[i][j] = Math.min(Math.min(m[i-1][j] + 1, m[i][j-1]),
                        m[i-1][j-1] + (str1[i] == str2[j] ? 0 : 1));
            }
        }
    }

    /**
     * Gets edit distance between strings
     * @return the minimum edit distance
     */
    public int getDistance() {
        return getMatrix()[str1.length - 1] [str2.length - 1];
    }

    /**
     * Gets matrix
     * @return edit distance matrix
     */
    public synchronized int[][] getMatrix(){
        if (this.m == null) {
            computeMatrix();
        }
        return m;
    }

}
