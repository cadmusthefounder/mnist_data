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

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()

def load_mnist(images_path, labels_path):
    with gzip.open(labels_path, 'rb') as lbpath:
        labels = np.frombuffer(lbpath.read(), dtype=np.uint8, offset=8)

    with gzip.open(images_path, 'rb') as imgpath:
        images = np.frombuffer(imgpath.read(), dtype=np.uint8, offset=16).reshape(len(labels), 28, 28)
        np.reshape(images, (len(labels), 28, 28))

    return images, labels

def write_data(data, images, labels):
    unique_labels = list(set(labels))

    current_directory = os.path.dirname(os.path.abspath(__file__))
    tmp_directory = os.path.join(current_directory, '..', 'tmp')
    tmp_directories = [os.path.join(tmp_directory, str(unique_labels[i])) for i in range(len(unique_labels))]
    for t in tmp_directories:
        if not os.path.exists(t):
            os.makedirs(t)
    
    print("Saving data as images...")
    printProgressBar(0, len(labels), prefix = 'Progress:', suffix = 'Complete', length = 50)
    for (i, label) in enumerate(labels):
        image = images[i]
        save_filename = os.path.join(tmp_directory, str(label), str(i) + '.png')
        pillow_image = Image.fromarray(image, mode='L')
        pillow_image.save(save_filename)
        printProgressBar(i + 1, len(labels), prefix = 'Progress:', suffix = 'Complete', length = 50)

    output_directory = os.path.join(current_directory, '..', 'output')
    output_filename = os.path.join(output_directory, data)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    print("Creating zip file...")
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
