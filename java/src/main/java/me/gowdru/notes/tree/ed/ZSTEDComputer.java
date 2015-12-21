package me.gowdru.notes.tree.ed;

/**
 * Zhang-Shasha’s tree edit distance Computer
 */
public class ZSTEDComputer {

    public static void main(String[] args) {

        TreeNode tree1 = new TreeNode("a")
                .addChild(new TreeNode("b")
                        .addChild(new TreeNode("c")
                                .addChild(new TreeNode("x")))
                        .addChild(new TreeNode("d")))
                .addChild(new TreeNode("m")
                        .addChild(new TreeNode("n"))
                        .addChild(new TreeNode("o")));

        TreeNode tree2 = new TreeNode("a")
                .addChild(new TreeNode("b")
                        .addChild(new TreeNode("x"))
                        .addChild(new TreeNode("d")))
                .addChild(new TreeNode("m")
                        .addChild(new TreeNode("n"))
                        .addChild(new TreeNode("o")));

        tree1.prettyPrint();
        tree2.prettyPrint();

        ZSTEDMatrix matrix = new ZSTEDMatrix(tree1, tree2);
        matrix.compute();
        matrix.prettyPrint();

    }
}
