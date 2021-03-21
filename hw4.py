import math
import os

"""This method takes an input file and creates a bitmap index over it, then writes the output to the"""
"""The supplied output_path. It assumes current working directory if no output_path is supplied"""
def create_index(input_file, output_path, sorted):
    # turn the animal cell into the correct string of bits
    animal = {
        'cat': '1000', 'dog': '0100',
        'turtle': '0010', 'bird': '0001',
    }

    # return a string with correct sequence of 0 and 1 for age bins
    def age(a):
        row = ['0'] * 10  # fill list with 0s
        cell = math.floor((int(a) - 1) / 10)  # find proper index for the 1
        row[cell] = '1'  # insert 1 in proper location
        return ''.join(row)  # return the list as a string

    adopted = {'True': '10', 'False': '01'}

    # if not output path supplied, assume current
    if output_path is None:
        output_path = os.getcwd()

    # create filename for output
    filename = os.path.basename(input_file)

    out = []
    # get file data and sort if necessary
    with open(input_file, 'r') as file:
        for line in file:
            out.append(line[:-1])  # strip trailing newline
    if sorted:
        out.sort()
        filename += "_sorted"

    # create output file
    output = open(os.path.join(output_path, filename),  'wb')

    # iterate through input file and create index for each line
    for line in out:
        builder = []
        cells = line.split(',')  # split line into list of strings, strip trailing newline
        builder.extend([animal[cells[0]], age(cells[1]), adopted[cells[2]]])  # add proper strings to list
        builder.append('\n')
        output.write(''.join(builder).encode())  # join the builder list into a string, encode to bytes and write

    output.close()


# This function takes a string of binary and pads the left side with 0s until size is reached
def pad_binary(bin_str, size):
    bin_lst = list(bin_str)
    while len(bin_lst) < size:
        bin_lst.insert(0, '0')
    return "".join(bin_lst)


# This function pads the right end of the terminal literal with 0s to reach word length
def pad_literal(chunk, size):
    while len(chunk) < size:
        chunk.append("0")
    return "".join(chunk)


def compress_index(bitmap_index, output_path, compression_method, word_size):
    """ Word Aligned Hybrid compression method"""

    total_literals = 0
    total_runs = 0
    chunk_size = word_size - 1

    # read lines from bit index file into a list of rows (arr), slice to strip newline
    arr = []
    with open(bitmap_index, 'r') as file:
        for line in file:
            arr.append(list(line)[:-1])

    total_rows = len(arr)
    data = [list(col) for col in (zip(*arr))]   # transpose the array so columns become rows
    total_columns = len(data)

    # initialize output to hold empty strings so that we can append the compressed columns
    output = ["" for x in range(total_columns)]
    for column in range(total_columns):
        i = 0
        # iterate over each bit in the column
        while i < len(data[column]):
            # extract chunk from current column (chunk is wordsize - 1 bits long)
            chunk = data[column][i:i + chunk_size]
            i += chunk_size

            # if the end of row is reached, encode final chunk as literal and continue to next loop iteration
            if i >= total_rows:
                output[column] += "0" + pad_literal(chunk, chunk_size)
                total_literals += 1
                continue

            # if the chunk has both 1s and 0s, then it's a literal. append to 0 for header indicating literal
            if not (chunk.count('1') == 0 or chunk.count('0') == 0):
                output[column] += "0" + "".join(chunk)
                total_literals += 1

            # if string is not literal, then it must be a run
            else:
                start = i  # start of run
                bit_type = chunk[0]  # save type of run (0's or 1s)
                count = chunk_size  # how many bits in the run there are, starts at (word size -1) because we
                # have at least 1 run
                # loop until end of rows, too many runs for a single byte, or run ends
                # word_size - 2 is the number of available bits for counting runs, so we have **2 countable per byte
                while i < total_rows and (count / chunk_size) <= 2 ** (word_size - 2) - 1 and data[column][i] == bit_type:
                    count += 1
                    i += 1

                run_count = math.floor(count / chunk_size)  # save count of full runs
                total_runs += run_count                   # increment total_runs for output
                i = start + (run_count - 1) * chunk_size  # reset i to the correct location of end of full runs

                # -1 is because i is incremented by chunk size at start of next
                run_encoding = ""  # empty string to hold runs
                if bit_type == "0":  # apply proper header
                    run_encoding += "10"
                else:
                    run_encoding += "11"

                # convert run count to binary, then pad left with 0s to proper width, add to encoding string
                run_encoding += pad_binary(bin(run_count)[2:], word_size - 2)

                # add the run encoding to the output for the column
                output[column] += run_encoding

    # assume cwd if no path supplied
    if output_path is None:
        output_path = os.getcwd()

    # make filename based on parameters
    filename = "" + os.path.basename(bitmap_index) + "_" + compression_method + "_" + str(word_size)

    with open(os.path.join(output_path, filename), 'wb') as file_out:
        for row in output:
            row += '\n'
            file_out.write(row.encode())
    print(f"File: {filename}   \t\tRuns: {total_runs} \t\tLiterals: {total_literals}")


""" Create index over unsorted animals.txt, store bitmap and compressions in a folder called "example"""
"""
create_index("animals.txt", "./Bitmaps", False)
compress_index("./Bitmaps/animals.txt", "./Compressed", "WAH", 8)
compress_index("./Bitmaps/animals.txt", "./Compressed", "WAH", 16)
compress_index("./Bitmaps/animals.txt", "./Compressed", "WAH", 32)
compress_index("./Bitmaps/animals.txt", "./Compressed", "WAH", 64)
"""

""" Create index over sorted animals.txt, store bitmap and compressions in cwd"""
"""
create_index("animals.txt", "./Bitmaps", True)
compress_index("./Bitmaps/animals.txt_sorted", "./Compressed", "WAH", 8)
compress_index("./Bitmaps/animals.txt_sorted", "./Compressed", "WAH", 16)
compress_index("./Bitmaps/animals.txt_sorted", "./Compressed", "WAH", 32)
compress_index("./Bitmaps/animals.txt_sorted", "./Compressed", "WAH", 64)
"""
