import numpy as np
import tensorflow as tf
import os
import csv
import time
import argparse

currt = lambda: long(time.time() * 1000)

def create_graph(model_path):
    """Creates a graph from saved GraphDef file and returns a saver."""
    # Creates graph from saved graph_def.pb.
    with tf.gfile.FastGFile(model_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

def read_labels(labels_path):
    """Reads list of labels from a file"""
    with open(labels_path, 'rb') as f:
        return [w.strip() for w in f.readlines()]

def run_inference(images, sess, labels, topk=5):
    """
    Runs inference on images
    @param images: (id, data) stream
    @param sess: Tensoflow Session
    @param labels: List of labels
    @returns (id, [(label, score),...]) stream
    """
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    for id, image_data in images:
        predictions = sess.run(softmax_tensor,
                       {'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)
        res = []
        top_nodes = predictions.argsort()[-topk:][::-1]
        for node_id in top_nodes:
            res.append((labels[node_id], predictions[node_id]))
        yield (id, res)

def get_all_images(input, root, suffix=".jpg"):
    if not tf.gfile.Exists(input):
        tf.logging.fatal('Input file does not exist %s', input)
        return
    with open(input) as inf:
        reader = csv.DictReader(inf)
        for rec in reader:
            image_path = os.path.join(root, rec['Id'] + suffix)
            image_data = tf.gfile.FastGFile(image_path, 'rb').read()
            yield (rec['Id'], image_data)

def write_output(filename, data, logdelay=10000):
    """Writes output to csv file """

    if tf.gfile.Exists(filename):
        tf.logging.fatal('Output file already exists at %s', filename)
        return
    count = 0
    with open(filename, 'wb') as outf:
        writer = csv.DictWriter(outf, ['Id', 'label'])
        writer.writeheader()
        st = currt()
        for id, res in data:
            top = res[0][0] # just the top 1
            writer.writerow({'Id': id, 'label': top})
            count += 1
            if currt() - st > logdelay:
                st = currt()
                print("%d :: Count = %d" % (st, count))

    print("Wrote %d records to %s" % (count, filename))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Classify Images')
    parser.add_argument('-i','--in', help='Input CSV file', required=True)
    parser.add_argument('-o','--out', help='Output CSV file path', required=True)
    parser.add_argument('-m','--model', help='model file path (protobuf)', required=True)
    parser.add_argument('-l','--labels', help='labels text file', required=True)
    parser.add_argument('-r','--root', help='path to root directory of input data', required=True)
    args = vars(parser.parse_args())

    # Creates graph from saved GraphDef.
    create_graph(args['model'])
    labels = read_labels(args['labels'])
    print("Labels : %s" % labels)
    images = get_all_images(args['in'], args['root'])
    with tf.Session() as sess:
        res = run_inference(images, sess, labels)
        write_output(args['out'], res)
    print("Done")
