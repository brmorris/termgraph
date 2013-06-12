#!/usr/bin/env python
# coding=utf-8

# termgraph.py - draw basic graphs on terminal
# https://github.com/mkaz/termgraph

# Marcus Kazmierczak
# http://mkaz.com/


import argparse, sys

#TODO: change tick character
    
class TermGraph():
        
        def __init__(self, width=100, tick='▇', sm_tick = '|', labels = None, data = None ):
            # TODO verify data 

            if len(labels) != len(data):
                print "Error, invalid input data length"
            
            self.tick = tick
            self.sm_tick = sm_tick
            self.labels = labels
            self.width = width
            self.data = data
            self.length = len(self.data)
            self.step = self._get_step();
             
        def _get_step(self):
            # step is width divided by the largest value
            max = 0
            for i in xrange(self.length):
                if self.data[i] > max:
                    max = self.data[i]
            return max / self.width

        def render(self):
            for i in xrange(self.length):
                self._print_blocks(self.labels[i], self.data[i], self.step)
            print

        def _print_blocks(self, label, count, step):
            #TODO: add flag to hide data labels
            blocks = int(count / step)
            print "{}: ".format(label),
            if count < step:
                sys.stdout.write(self.sm_tick)
            else:
                for i in xrange(blocks):
                    sys.stdout.write(self.tick)

            print "{:>7.2f}".format(count)
    

def main():
    args = init()
    if (args['filename']):
        labels, data = read_data(args['filename'])
    else:
        # shouldn't happen since argparse covers empty case
        print ">> Error: No data file specified"
        sys.exit(1)

    termgraph = TermGraph(width = args['width'], labels = labels, data = data)
    termgraph.render()

 
def init():
    parser = argparse.ArgumentParser(description='draw basic graphs on terminal')
    parser.add_argument('filename', nargs=1, help='data file name (comma or space separated)')
    parser.add_argument('--width', type=int, default=50, help='width of graph in characters default:50')
    parser.add_argument('--verbose', action='store_true')
    args = vars(parser.parse_args())
    args['filename'] = args['filename'][0]  # returns as list, we dont want that
    return args


def read_data(filename):
    labels = []
    data = []

    f = open(filename, "r")
    for line in f:
        line = line.strip()
        if line:
            if not line.startswith('#'):
                if line.find(",") > 0:
                    cols = line.split(',')
                else:
                    cols = line.split()
                labels.append(cols[0].strip())
                data_point = cols[1].strip()
                data.append(float(data_point))

    f.close()
    return labels, data


if __name__ == "__main__":
    main()