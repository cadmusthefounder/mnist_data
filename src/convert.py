from PIL import Image
import numpy as np
import gzip
import os
import sys
import getopt
import shutil

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

def write_data(data, images, labels):
    current_directory = os.path.dirname(os.path.abspath(__file__))

    tmp_directory = os.path.join(current_directory, '..', 'tmp')
    tmp_directories = [os.path.join(tmp_directory, str(i)) for i in range(10)]
    for t in tmp_directories:
        if not os.path.exists(t):
            os.makedirs(t)
    
    for (i, label) in enumerate(labels):
        image = images[i]
        save_filename = os.path.join(tmp_directory, str(int(label)), str(i) + '.png')
        pillow_image = Image.fromarray(image, mode='L')
        pillow_image.save(save_filename)

    output_directory = os.path.join(current_directory, '..', 'output')
    output_filename = os.path.join(output_directory, data)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    shutil.make_archive(output_filename, 'zip', tmp_directory)
    shutil.rmtree(tmp_directory)

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

    write_data(data + '_train', train_images, train_labels)
    write_data(data + '_test', test_images, test_labels)

if __name__== "__main__":
    main(sys.argv)
