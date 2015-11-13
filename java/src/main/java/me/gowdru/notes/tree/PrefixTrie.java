package me.gowdru.notes.tree;

import java.util.HashMap;
import java.util.Map;

/**
 * This class offers a variation of Trie data structure
 * which is specially built for counting number of prefix strings.
 * Visit test case for the usage demo.
 *
 * @author Thamme Gowda N tgowdan@gmail.com
 * @since November 13, 2015
 */
public class PrefixTrie {

    private int count = 1;
    private Map<Character, PrefixTrie> branches = new HashMap<>();

    public static PrefixTrie newRoot(){
        PrefixTrie tree = new PrefixTrie();
        tree.count = 0;
        return tree;
    }

    private PrefixTrie() {
    }

    private PrefixTrie(char[] sequence, int offset) {
        if (offset < sequence.length) {
            char ch = sequence[offset];
            this.branches.put(ch, new PrefixTrie(sequence, offset + 1));
        }
    }

    /**
     * Insert a string to trie
     * @param text the string to be inserted
     */
    public void insert(String text) {
        this.insert(text.toCharArray(), 0);
    }

    /**
     * Inserts a character array to tie
     * @param sequence an array of chars
     * @param offset the offset in array
     */
    public void insert(char[] sequence, int offset){
        if (offset < sequence.length) {
            this.count++;
            char ch = sequence[offset];
            PrefixTrie subTree = branches.get(ch);
            if (subTree != null) {
                // there's already a tree
                subTree.insert(sequence, offset + 1);
            } else {

                // new tree created here
                branches.put(ch, new PrefixTrie(sequence, offset + 1));
            }
        }
    }

    public Map<Character, PrefixTrie> getBranches() {
        return branches;
    }

    /**
     * gets number of prefix strings indexed so far
     * @return number of strings with prefix of this node inserted
     */
    public int getCount() {
        return count;
    }


    @Override
    public String toString() {
        String s = "(" + count + ")";
        if (branches == null || branches.isEmpty()) {
            //nothing needs to be done
        } else if (branches.size() == 1) {
            Character first = branches.keySet().iterator().next();
            PrefixTrie tree = branches.get(first);
            s += first + ((tree != null) ? tree.toString(): "");
        } else {
            s += branches.toString();
        }
        return s;
    }

    public int countPrefixPaths(String text) {
        return countPrefixPaths(text.toCharArray());
    }

    /**
     * Counts number of prefixes seen in the trie
     * @param chars the char sequence
     * @return number of strings in the given trie which have input param as prefix
     */
    public int countPrefixPaths(char[] chars) {

        PrefixTrie tree = this;
        if (chars.length == 0) {
            return tree.count;
        }

        for (int i = 0; tree != null && i < chars.length - 1; i++) {
            tree = tree.branches.get(chars[i]);
        }
        char lastChar = chars[chars.length - 1];
        if (tree != null) {
            tree = tree.branches.get(lastChar);
        }
        //either ran outside of the tree or reached the right place
        return tree == null ? 0 : tree.getCount();
    }
}
