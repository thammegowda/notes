package me.gowdru.notes.ir.vsm;

import org.kohsuke.args4j.CmdLineException;
import org.kohsuke.args4j.CmdLineParser;
import org.kohsuke.args4j.Option;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.*;
import java.nio.charset.Charset;
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
    private boolean removeStopwords = true;
    private boolean debug = true;

    private static Set<String> STOP_WORDS = new HashSet<>(Arrays.asList(
            "a", "an", "and", "are", "as", "at", "be", "but", "by",
            "for", "if", "in", "into", "is", "it",
            "no", "not", "of", "on", "or", "such",
            "that", "the", "their", "then", "there", "the"));

    /**
     * Tokenizes the text stream content into tokens.
     * @param stream the text content stream
     * @return List of tokens in the order of occurrence, no duplicates removed
     * @throws IOException when error occurs
     */
    private List<String> tokenize(InputStream stream) throws IOException {
        List<String> tokens = new ArrayList<>();
        BufferedReader reader = new BufferedReader(new InputStreamReader(stream));
        String line;
        while ((line = reader.readLine()) != null) {
            line = new String(line.getBytes("UTF-8"), Charset.forName("UTF-8"));
            if (ignoreCase) {
                line = line.toLowerCase();
            }
            if (ignorePunctuations) {
                line = line.replaceAll("\\p{P}", "").replaceAll("[<>]", "");
            }
            line = line.trim();
            String[] parts = line.split("\\s+");
            for (String part : parts) {
                if (!part.isEmpty()) {
                    if (removeStopwords && STOP_WORDS.contains(part)) {
                        continue;
                    }
                    tokens.add(part);
                }
            }
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
        Set<String> features = new LinkedHashSet<>();
        long vectorNumber = 0;
        for (File file : files) {
            FileInputStream stream = new FileInputStream(file);
            List<String> tokens = tokenize(stream);
            for (String token : tokens) {
                if (!token.isEmpty() && !dict.containsKey(token)) {
                    dict.put(token, ++vectorNumber);
                    features.add(token + '=' + vectorNumber);
                }
            }
        }
        if (debug) {
            FileWriter writer = new FileWriter("dict.txt");
            for (String feature : features) {
                writer.write(feature);
                writer.write("\n");
            }
            writer.close();
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
        return root.listFiles(File::isFile);
    }

    /**
     * Creates a vector from given tokens
     * @param tokens the list of tokens
     * @param vectorId id for the vector
     * @param dict dictionary
     * @return Vector
     */
    public Vector vectorize(List<String> tokens, String vectorId, Map<String, Long> dict) {
        TreeMap<Long, Double> features = new TreeMap<>();
        for (String token : tokens) {
            //map token to feature
            Long featureDimension = dict.get(token);
            if (featureDimension == null) {
                LOG.debug("Not found in dictionary {}", token);
                continue;
            }
            //if featureDimension is already present, increment the magnitude
            features.put(featureDimension, features.getOrDefault(featureDimension, 0.0) + 1.0);
        }
        return new Vector(vectorId, features);
    }

    /**
     * Launches a console to accept input from console and performs search on vectors using cosine angle measure
     * @param vectors
     * @param dictionary
     * @throws IOException
     */
    public void searchConsole(Vector[] vectors, Map<String, Long> dictionary) throws IOException {
        Scanner prompt = new Scanner(System.in);
        System.out.println("Entering the search console. Total Vectors = " + vectors.length
                + " \nType 'exit' to halt the program.");
        while (true){
            System.out.print(">");
            String query = prompt.nextLine();
            if (query.isEmpty()) {
                System.out.println("Enter search query or type 'exit' to halt");
                continue;
            } else if (query.toLowerCase().equals("exit")) {
                break;
            }

            //convert the query to vector
            List<String> tokens = tokenize(new ByteArrayInputStream(query.getBytes()));
            Vector queryVector = vectorize(tokens, System.currentTimeMillis() + "query", dictionary);
            Map<Double, List<String>> cosθs = new TreeMap<>();
            for (int i = 0; i < vectors.length; i++) {
                double cosθ = queryVector.cosθ(vectors[i]);
                if (Double.isNaN(cosθ)) {
                    continue;
                }
                List<String> ids = cosθs.get(cosθ);
                if (ids == null) {
                    ids = new ArrayList<>();
                    cosθs.put(cosθ, ids);
                }
                ids.add(vectors[i].vectorId);
            }

            //print
            for (Map.Entry<Double, List<String>> i : cosθs.entrySet()) {
                System.out.println(i);
            }
            if (cosθs.isEmpty()) {
                System.out.println("No results found. NaN");
            }

        }
    }

    public static void main(String[] args) throws IOException {
        args = "-d ../data/20newsgroups/20news-bydate-train/sci.crypt/".split(" ");
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
        LOG.info("Found {} tokens", dict.size());

        Vector[] vectors = new Vector[files.length];

        for (int i = 0; i < files.length; i++) {
            List<String> tokens = vsm.tokenize(new FileInputStream(files[i]));
            Vector vector = vsm.vectorize(tokens, files[i].getPath(), dict);
            vectors[i] = vector;

        }
        if (vsm.debug) {
            FileWriter out = new FileWriter("vect2.txt");
            for (Vector vector : vectors) {
                out.write(vector.toString());
                out.write("\n");
            }
            out.close();
        }

       vsm.searchConsole(vectors, dict);
    }
}
