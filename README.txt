How to use hw4.py This program creates a bitmap index over the supplied data files and performs WAH compression on that index.

Functions:

create_index(input_file, output_path, sorted)

	This function creates a bitmap index from the supplied parameter <input_file>, and places in resulting index in the directory specified by <output_path>
	If <output_path> is None, then the function assumes current working directory. The <sorted> parameter is a boolean value that indicates if <input_file> should
	be sorted lexicographically before the creation of the bitmap index. This will result in an index that can be compressed more efficiently.

compress_index(bitmap_index, output_path, compression_method, word_size)

	This function compresses the bitmap index from the supplied parameter <bitmap_index> and places the resulting index in the directory specified by <output_path>
	If <output_path> is None, then assumes current working directory. The <compression_method> parameter should always be the string "WAH" for Word-Aligned Hybrid, as no other
	compression methods are supported at this time. <word_size> specifies the integer word size to be used in the WAH compression. This should be dependent on the architecture of the system.
	Common values are 8, 16, 32, and 64 bit.

pad_binary(bin_str, size)

	This is an internal function that is used by compress_index to pad a binary string to the proper width for the word size. For example, passing (bin_str = "01", size = 8) will pad
	the left side of the string with '0's to width 8, resulting in "00000001"

pad_literal(chunk, size)

	This is an internal function that is used by compress_index to pad the final literal in each column with 0's to the right until proper word size is reached. For example, if
	(chunk="0111", size=8) is passed to the function, the result will be "01110000"

Usage:

	1. This program should be imported as a module, and then interfaced with using only create_index and compress_index. For example:
        import hw4
        hw4.create_index("animals_small.txt", None, True)
        hw4.compress_index("animals_small.txt_sorted", None, "WAH", 8)

        This script will import the program create the index over a sorted version of animals_small.txt, and compress it using word size 8.
	
	2. Alternatively, the program can be run directly with individual function calls added to the bottom of the script. There are some commented out examples at the bottom of the code.
