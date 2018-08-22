import numpy as np
import gzip
import os
import sys
import getopt

params = {
    'train_images' : 'train-images-idx3-ubyte.gz',
    'train_labels' : 'train-labels-idx1-ubyte.gz',
    'test_images' : 't10k-images-idx3-ubyte.gz',
    'test_labels' : 't10k-labels-idx1-ubyte.gz'
}


def load_mnist(images_path, labels_path):
    with gzip.open(labels_path, 'rb') as lbpath:
        labels = np.frombuffer(lbpath.read(), dtype=np.uint8, offset=8)

    with gzip.open(images_path, 'rb') as imgpath:
        images = np.frombuffer(imgpath.read(), dtype=np.uint8, offset=16).reshape(len(labels), 28, 28)
        np.reshape(images, (len(labels), 28, 28))

    return images, labels

def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], 'hd:', ['help=', 'data='])
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                print('{} -d <data>'.format(argv[0]))
                sys.exit()
            elif opt in ('-d', '--data'):
                data = arg
    except getopt.GetoptError:
        print('{} -d <data>'.format(argv[0]))
        sys.exit()

    current_directory = os.path.dirname(os.path.abspath(__file__))
    train_images_file = os.path.join(current_directory, '..', 'data', data, params['train_images'])
    train_labels_file = os.path.join(current_directory, '..', 'data', data, params['train_labels'])
    test_images_file = os.path.join(current_directory, '..', 'data', data, params['test_images'])
    test_labels_file = os.path.join(current_directory, '..', 'data', data, params['test_labels'])

    train_images, train_labels = load_mnist(train_images_file, train_labels_file)
    test_images, test_labels = load_mnist(test_images_file, test_labels_file)

    print(train_images.shape)
    print(train_labels.shape)
    print(test_images.shape)
    print(test_labels.shape)

if __name__== "__main__":
    main(sys.argv)
