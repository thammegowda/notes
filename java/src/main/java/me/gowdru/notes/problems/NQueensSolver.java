package me.gowdru.notes.problems;

/**
 * This class has solver for n-queens problem
 * @author Thamme Gowda
 */
public class NQueensSolver {

    private final int n;
    private final int[] queens;
    private int numSolutions = 0;
    private boolean printSolutions;

    /**
     * Creates a n-queens problem solver for nxn chess board
     * @param n chess board size
     * @param printSolutions set true if you desire to print solutions when this solver finds them
     */
    public NQueensSolver(int n, boolean printSolutions) {
        this.n = n;
        this.queens = new int[n];// n queens
        this.printSolutions = printSolutions;
    }


    /**
     * Checks the placement of given rowNum is consistent with all previous rows
     * @param rowNum the row index whose solution needs to be checked
     *               for consistency with problem coonstraints
     * @return true if the solution is consistent
     */
    private boolean isConsistent(int rowNum) {
        for (int i = 0; i < rowNum; i++) {
            if (queens[i] == queens[rowNum]){
                return false;   // same column
            }
            if ((queens[i] - queens[rowNum]) == (rowNum - i)){
                return false;   // same major diagonal
            }
            if ((queens[rowNum] - queens[i]) == (rowNum - i)){
                return false;   // same minor diagonal
            }
        }
        return true; // no conflicts
    }

    /**
     * prints solution
     * @param solNumber solution number for identification
     */
    public void printSolution(final int solNumber){
        System.out.println("\nSolution #" + solNumber);
        for (int i = 0; i < n; i++) { //ith row
            for (int j = 0; j < n; j++) { //jth column
                System.out.printf("%2s", queens[i] == j ? "Q" : "-");
            }
            System.out.println();
        }
    }

    /**
     * Recursively solves n-Queens problem for given row. To begin with, input 0
     * @param rowNum the row index
     */
    private void solveRow(int rowNum) {
        if (rowNum == n) {
            //all previous rows [0 - n-1] are  consistent,
            // so found another solution
            numSolutions++;
            if (printSolutions) {
                printSolution(numSolutions);
            }
            //base case:
            //row number has exceeded the chess board size, so don't advance
            return;
        }

        //trying to place the queen in each cell in the row
        for (int i = 0; i < n; i++) {
            queens[rowNum] = i;
            if (isConsistent(rowNum)){
                //go ahead for the next row
                solveRow(rowNum + 1);
            }
            // else move on to next column
            // possible solutions of next cell will be checked nevertheless to count all possible solutions!
        }
    }

    public static void solve(int n){
        //long st = System.currentTimeMillis();
        NQueensSolver solver = new NQueensSolver(n, true);
        solver.solveRow(0);
        //System.out.println("Time taken      :" + (System.currentTimeMillis() - st) + "ms");
        System.out.println("Total solutions : " + solver.numSolutions);
    }

    public static void countSolutions(int n){
        System.out.println("N :: Solutions\n===============");
        for (int i = 1; i <= n; i++) {
            NQueensSolver solver = new NQueensSolver(i, false);
            solver.solveRow(0);
            System.out.printf("%2d :: %6d\n", i, solver.numSolutions);

        }
    }

    public static void main(String[] args) {
        int n = 8;
        countSolutions(n);
        solve(n);
    }

}
