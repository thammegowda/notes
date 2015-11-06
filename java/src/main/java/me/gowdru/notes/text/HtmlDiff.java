package me.gowdru.notes.text;

import com.google.common.io.Files;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;

/**
 * Created by tg on 11/6/15.
 */
public class HtmlDiff {
    public static void main(String[] args) throws IOException {
        args = "data/html/iphone6sgold.html data/html/iphone6silver.html".split(" ");
        if (args.length != 2) {
            System.err.println("Invalid args");
            System.out.println("USAGE: <HTML_FILE1> <HTML_FILE2>");
            return;
        }
        String file1 = args[0];
        String file2 = args[1];
        System.out.println("Finding diff between " + file1 + " and " + file2);
        String s1 = Files.toString(new File(file1), StandardCharsets.UTF_8);
        String s2 = Files.toString(new File(file2), StandardCharsets.UTF_8);
        System.out.printf("%d x %d ", s1.length(), s2.length());
        //FIXME: insufficient memory
        EditDistanceComputer computer = new EditDistanceComputer(s1, s2);
        computer.printMatrix();

    }
}
