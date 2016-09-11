package me.gowdru.notes.problems;
import java.io.*;
import java.util.*;

/**
 * @since 9/4/16
 */
public class LongestIncreasingSubSeq {

    static int findLIS(int[] arr){
        /*
         * This method runs in O(n^2) time and O(n) memory
         * Method: For each item, look at the previous items and update count
         */
        int n = arr.length;
        int mem[] = new int[n];
        int max = Integer.MIN_VALUE;
        for (int i = 0; i < n; i++){
            mem[i] = 1;
            //OPT(i) =  Max{ OPT(j)+1, for all j < i and a[j] < a[i]}
            for (int j = i-1; j >= 0; j--){
                if (arr[j] < arr[i]){ //if it can be previous element in sequence
                    mem[i] = Math.max(mem[i], mem[j] + 1);
                }
            }
            max = Math.max(max, mem[i]);
        }
        return max;
    }

    static int findLISFast(int[] arr){
        /*
         * This method runs in O(n * log(n)) time and O(n) memory
         * Method : When you build BST,
                the increasing subsequence goes to right most branch.
                So, we let the right most branch grow, chop the lefts
         */
        class Node { // BST Node
            int val;
            //Node left; // we dont use this
            Node right;
            Node(int val){this.val = val;}

            void insert(int val){
                assert val != this.val; // dont know how to handle dup vals!
                if (val < this.val){
                    //supposed to go on the left
                    // But we dont grow the left branches!
                    //Insetad, we replace the current node (smaller item stays in tree)
                    this.val = val;
                } else {
                    if (right == null){
                        right = new Node(val);
                    } else {
                        right.insert(val);
                    }
                }
            }
        };

        assert arr.length > 0;
        Node root = new Node(arr[0]);
        for (int i = 1; i < arr.length; i++){
            root.insert(arr[i]);
        }
        // find the length of the right most branch
        int count = 0;
        while (root != null){
            count++;
            root = root.right;
        }
        return count;
    }

    public static void main(String[] args) throws Exception {
        //Scanner in = new Scanner(System.in);
        Scanner in = new Scanner(new FileInputStream("in1.txt"));

        int n = in.nextInt();
        int arr[] = new int[n];
        for(int i = 0; i < n; i++){
            arr[i] = in.nextInt();
        }
        //int res = findLIS(arr);
        int res = findLISFast(arr);
        System.out.println(res);
    }
}
