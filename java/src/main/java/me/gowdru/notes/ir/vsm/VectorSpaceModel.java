package me.gowdru.notes.ir.vsm;

import org.kohsuke.args4j.CmdLineException;
import org.kohsuke.args4j.CmdLineParser;
import org.kohsuke.args4j.Option;
import org.kohsuke.args4j.spi.StringArrayOptionHandler;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.*;
import java.math.BigInteger;
import java.util.*;

/**
 * Implementation of simple VSM.
 */
public class VectorSpaceModel {

    public static final Logger LOG = LoggerFactory.getLogger(VectorSpaceModel.class);

    @Option(name = "-d", aliases = {"--docs"}, usage = "Directory containing *.txt files", required = true)
    private String corpus;

    private boolean ignoreCase = true;
    private boolean ignorePunctuations = true;

    /**
     * Tokenizes the text stream content into tokens.
     * @param stream the text content stream
     * @return List of tokens in the order of occurrence, no duplicates removed
     * @throws IOException when error occurs
     */
    private List<String> getTokens(InputStream stream) throws IOException {
        List<String> tokens = new ArrayList<>();
        BufferedReader reader = new BufferedReader(new InputStreamReader(stream));
        String line;
        while ((line = reader.readLine()) != null) {
            if (ignoreCase) {
                line = line.toLowerCase();
            }
            if (ignorePunctuations) {
                line = line.replaceAll("\\p{P}", "").replaceAll("[<>]", "");
            }
            line = line.trim();
            Collections.addAll(tokens, line.split("\\s+"));
        }
        return tokens;
    }

    /**
     * Creates a dictionary of tokens from
     * @param files - list of files from which the dictionary needs to be built
     * @return dictionary of token:dimension
     * @throws IOException
     */
    private Map<String, Long> buildDictionary(File[] files) throws IOException {
        Map<String, Long> dict = new HashMap<String, Long>();
        long vectorNumber = 0;
        for (File file : files) {
            FileInputStream stream = new FileInputStream(file);
            List<String> tokens = getTokens(stream);
            for (String token : tokens) {

                if (!token.isEmpty() && !dict.containsKey(token)) {
                    dict.put(token, ++vectorNumber);
                }
            }
        }
        return dict;
    }

    /**
     * Finds all files in a corpus
     * @return array of text files
     */
    private File[] getCorpusFiles(){
        File root = new File(corpus);
        if (!root.exists() || !root.isDirectory()) {
            throw new IllegalArgumentException(corpus + "is not a Directory");
        }
        return root.listFiles((dir, name) -> name.toLowerCase().endsWith(".txt"));
    }

    public static class Vector {
        public long dimesions[];
        public long scales[];
    }

    public static void main(String[] args) throws IOException {
        args = "-d data/ir/vsm/docs".split(" ");
        VectorSpaceModel vsm = new VectorSpaceModel();
        CmdLineParser parser = new CmdLineParser(vsm);
        try {
            parser.parseArgument(args);
        } catch (CmdLineException e) {
            parser.printUsage(System.out);
            return;
        }
        File[] files = vsm.getCorpusFiles();
        LOG.info("Found {} files in {}", files.length, vsm.corpus);
        Map<String, Long> dict = vsm.buildDictionary(files);
        TreeSet<String> sortedSet = new TreeSet<>(dict.keySet());
        System.out.println(sortedSet.size() + "==" + dict.size());
        FileWriter out = new FileWriter("out.txt");
        for (String s : sortedSet) {
            out.write(s + "=" + dict.get(s) + "\n");
        }

        LOG.info("Found {} tokens", dict.size());
    }
}
