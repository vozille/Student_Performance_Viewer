import getopt
import sys


# def main(argv):
#     try:
#         opts, args = getopt.getopt(argv, "h:i:o:", ["inputFile =", "outputFile ="])
#     except getopt.GetoptError:
#         print "ERROR"
#         print "Usage : test.py -i --inputFile <inputfile> -o --outputFile <outputfile> -h help"
#         sys.exit(0)
#     if len(opts) == 0:
#         print "ERROR"
#         print "Usage : test.py -i --inputFile <inputfile> -o --outputFile <outputfile> -h help"
#         sys.exit(0)
#     print opts, args
#     for opt, arg in opts:
#         if opt == '-h':
#             if len(opts) != 1:
#                 print "ERROR"
#                 print "Usage : test.py -i --inputFile <inputfile> -o --outputFile <outputfile> -h help"
#             else:
#                 print arg, opt, '1'
#             return
#         if opt == '-i':
#             print arg, opt, '2'
#         if opt == '-o':
#             print arg, opt, '3'
#
# if __name__ == '__main__':
#     main(sys.argv[1:])

idx = 9
while idx > 0:
    r = idx & - idx
    idx -= r
    print r


