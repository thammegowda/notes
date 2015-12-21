package me.gowdru.notes.tree.ed;

import java.util.List;

/**
 * Edit distance matrix used for computing minimum edit distance using
 * Zhang Shasha's algorithm for Tree Edit Distance (ZSTED)
 * <p>
 *  <h2>References</h2>
 *  <a href="http://dl.acm.org/citation.cfm?id=76082">K. Zhang and D. Shasha. 1989.
 *  Simple fast algorithms for the editing distance between trees and related problems.
 *  SIAM J. Comput. 18, 6 (December 1989), 1245-1262. DOI=http://dx.doi.org/10.1137/0218082</a>
 $</a>
 * </p>
 * <pre>
 *
 * </pre>
 * @see ZSTEDComputer
 */
class ZSTEDMatrix {

    private int insertionCost = 1;
    private int deletionCost = 1;
    private int replaceCost = 1;
    private int noEditCost = 0;

    private List<TreeNode> tree1;
    private List<TreeNode> tree2;

    private int nRows;
    private int nCols;
    private int[][] matrix;
    private boolean computed;

    /**
     * Creates a matrix for given trees
     * @param tree1 first tree
     * @param tree2 second tree
     */
    public ZSTEDMatrix(TreeNode tree1, TreeNode tree2) {
        this.tree1 = tree1.postOrderNodes();
        this.tree2 = tree2.postOrderNodes();
        TreeNode empty = new TreeNode("Φ");
        this.tree1.add(0, empty);
        this.tree2.add(0, empty);
        this.nRows = this.tree1.size();
        this.nCols = this.tree2.size();
        // Note: Tree1 nodes as rows and Tree2 nodes as columns
    }

    /**
     * Initializes the matrix and creates base cases
     */
    public void initialize(){
        this.matrix = new int[nRows][nCols];
        //Lemma 3.1 : forestdist(Φ,Φ)= 0;
        matrix[0][0] = noEditCost;

        //Lemma 3.2 : Tree1 v/s empty Tree2 => insert all the nodes
        for (int i = 1; i < nRows; i++){
            matrix[i][0] = matrix[i-1][0] + insertionCost;
        }

        // Lemma 3.3 : Empty Tree1 v/s Tree2 => Delete all the tree2 nodes
        for (int i = 1; i < nCols; i++) {
            matrix[0][i] = matrix[0][i-1] + deletionCost;
        }
    }

    /**
     * Computes the edit distance between trees
     * @return : minimum edit distance between root of two trees
     */
    public int compute(){
        this.initialize();

        TreeNode tree1Root = tree1.get(tree1.size() - 1);
        TreeNode tree2Root = tree2.get(tree2.size() - 1);
        TreeNode tree1Low = tree1Root.getLow();
        TreeNode tree2Low = tree2Root.getLow();

        for (int i = 1; i < nRows; i++) {
            TreeNode i1 = tree1.get(i);
            TreeNode i1Low = i1.getLow();

            for (int j = 1; j < nCols; j++) {
                TreeNode j1 = tree2.get(j);
                TreeNode j1Low = j1.getLow();
                int del = matrix[i][j-1] + deletionCost;
                int insert = matrix[i-1][j] + insertionCost;

                int replacementCost = matrix[i-1][j-1];
                if (i1.getName().equals(j1.getName())) {
                    // no edit required
                    replacementCost += this.noEditCost;
                } else {
                    //replacement is required
                    //check if we need a single node replacement or a subtree replacement
                    if (i1Low.getName().equals(tree1Low.getName())
                            && j1Low.getName().equals(tree2Low.getName())) {
                        //simple Replace, just a single node
                        replacementCost += this.replaceCost;
                    } else {
                        //sub tree replace => replace the subtree rooted at i with j
                        //TODO: reuse existing matrix, #DP
                        replacementCost += new ZSTEDMatrix(i1, j1).compute();
                    }
                }
                //Minimum of three cases (Insert, Delete, Replace)
                matrix[i][j] = Math.min(insert, Math.min(del, replacementCost));
            }
        }
        this.computed = true;
        return matrix[nRows-1][nCols-1];
    }

    /**
     * prints a nicely formatted matrix to STDOUT
     */
    public void prettyPrint(){
        System.out.printf("Matrix %dx%d; Min EdDist=%d\n\t",
                nRows, nCols, getMinEdDistance());
        for (TreeNode node : tree2) {
            System.out.printf("'%s'\t", node.getName());
        }
        System.out.println();
        for (int i = 0; i < nRows; i++) {
            System.out.printf("'%s'\t", tree1.get(i).getName());
            for (int j = 0; j < nCols; j++) {
                System.out.printf("%2d\t", matrix[i][j]);
            }
            System.out.println();
        }
    }

    /**
     * Retrieves minimum edit distance between root nodes of the trees
     * @return minimum edit distance between root  notes of trees
     */
    public int getMinEdDistance(){
        if (!computed) {
            compute();
        }
        return matrix[nRows - 1][nCols - 1];
    }
}
