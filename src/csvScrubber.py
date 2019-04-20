import sys
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('outputCSV', help='name of csv file to write to')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--threshold', help='minimum packet count of flows', type=int)
group.add_argument('--count', help='keeps the top <count> flows in terms of number of packets', type=int)

args = parser.parse_args()

dirPath = os.path.dirname(os.path.realpath(__file__))

csvFiles = ['webBrowsing.csv', 'fileDownloading.csv', 'videoStreaming.csv', 'videoConferencing.csv']

with open('{}/../trainingData/{}'.format(dirPath, args.outputCSV), 'w') as combinedFile:
    for fileName in csvFiles:
        with open('{}/../trainingData/{}'.format(dirPath, fileName), 'r') as f:
            if args.count:
                # todo
                raise NotImplementedError
            elif args.threshold:
                for line in f:
                    if int(line.split(',')[4]) >= args.threshold:
                        combinedFile.write(line)
