package me.gowdru.notes.tree.ed;

import java.util.ArrayList;
import java.util.List;

/**
 * An instance of this class represents a node in tree.
 *
 */
public class TreeNode {

    private TreeNode parent;
    private List<TreeNode> children = new ArrayList<>();
    private String name;

    public TreeNode(String name) {
        this.name = name;
    }

    public TreeNode setName(String name){
        this.name = name;
        return this;
    }

    public TreeNode addChild(TreeNode node){
        node.setParent(this);
        this.children.add(node);
        return this;
    }

    public TreeNode addChild(int pos, TreeNode node){
        node.setParent(this);
        this.children.add(pos, node);
        return this;
    }

    public List<TreeNode> getChildren() {
        return children;
    }

    public String getName() {
        return name;
    }

    public boolean isLeaf() {
        return children.isEmpty();
    }

    public void setParent(TreeNode parent) {
        this.parent = parent;
    }

    public TreeNode getParent() {
        return parent;
    }

    public TreeNode getLow(){
        TreeNode low = this;
        while (!low.isLeaf()) {
            low = low.getChildren().get(0);
        }
        return low;
    }

    public List<TreeNode> getAncestors(){
        List<TreeNode> ancestors = new ArrayList<>();
        for(TreeNode node = getParent(); node != null; node = node.getParent()){
            ancestors.add(node);
        }
        return ancestors;
    }

    public int size(){
        int n = 1; // this node is counted
        for (TreeNode child : children) {
            n += child.size();
        }
        return n;
    }

    public void prettyPrint() {
        prettyPrint("", true);
    }

    private void prettyPrint(String prefix, boolean isTail) {
        System.out.println(prefix + (isTail ? "└── " : "├── ") + name);
        for (int i = 0; i < children.size() - 1; i++) {
            children.get(i).prettyPrint(prefix + (isTail ? "    " : "│   "), false);
        }
        if (children.size() > 0) {
            children.get(children.size() - 1).prettyPrint(prefix + (isTail ?"    " : "│   "), true);
        }
    }


    public List<TreeNode> postOrderNodes(){
        List<TreeNode> nodes = new ArrayList<>();
        postOrderTraverse(nodes);
        return nodes;
    }

    public void postOrderTraverse(List<TreeNode> buffer){
        for (TreeNode child : children) {
            child.postOrderTraverse(buffer);
        }
        buffer.add(this);
    }

    public int getLevel() {
        int level = 0;
        for (TreeNode node = this; node.getParent() != null; node = node.getParent()){
            level++;
        }
        return level;
    }

    @Override
    public String toString() {
        return "Node('" + name + "')";
    }
}
