#!/usr/bin/python

# Copyright (c) 2013, Jason Nelson
#
# sequ.py : written in python 2.7
# 
# This is my implementation of compliance level 4 of the sequ command (universal sequence.)
# It accepts two number arguments, or an optional third, as well as any number of valid options.
# The program outputs an inclusive sequence of numbers between the first and last arguments, and
# will increment the values by the increment argument if present (default increment is 1 if third
# argument is missing.)  
#
# Options include format, seperator, equal-width, help, version, words, pad, pad-spaces, format-word,
# and number-lines.    
#
# For more details about program usage, try running the program with a '-h' or '--help' option.

import sys
import decimal

#Check if a commmand-line argument is a help option
def help_check(arg):
	if arg == '-h' or arg == '--help':
		return True
	else:
		return False

#Check if a command-line argument is a version option
def version_check(arg):
	if arg == '-v' or arg == '--version':
		return True
	else:
		return False

#Print sequ help information
def print_help():
	print "Usage: sequ [option].. First Last"
	print "  Or:  sequ [option].. First Increment Last"
	print "  Or:  sequ [option].. First Increment (If number-lines is a chosen option)"
	print " "
	print "Prints numbers from First to Last in steps of Increment"
	print " "
	print "Options: "
	print "		-f, --format [format_string]        use printf style floating-point format"
	print "		-s, --seperator [seperator_string]  use seperator_string to seperate numbers"
	print "		-w, --equal-width		    equalize width by padding with zeroes"
	print "		-h, --help			    display help and exit"
	print "		-v, --version			    display version information and exit"
	print "		-W, --words			    use ' ' to seperate numbers"
	print "		-p, --pad [pad_string]		    equalize width by padding with pad_string"
	print "		-P, --pad-spaces		    equalize width by padding with spaces"
	print "		-F, --format-word [format_string]   print alternate sequences of numbers."
	print "						    format_string must be 'arabic', 'floating', "
	print "						    'alpha', 'ALPHA', 'roman', or 'ROMAN' "
	print "		-n, --number-lines		    number lines of a text file presented on the input."
	print "						    The first line in the file will be numbered with First, and each"
	print "						    subsequent line will be numbered with the chosen sequence."		    		
	print "\n"

#Print sequ version information
def print_version():
	print "sequ 1.0"
	print "Copyright (C) 2013, Jason Nelson"
	print "\n"

#Checks if a command-line argument is a number, either integer or floating type is fine.
#http://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-in-python
def number_check(arg):
	try:
		int(arg)
	except ValueError:
		try:
			float(arg)
		except ValueError:
			return False

	return True

#Check if the argument is a single character
def char_check(arg):
	if arg.isalpha() and len(arg) == 1:
		return True
	else:
		return False

#Check if the argument could be a reasonable roman numeral
def roman_check(arg):
	length = len(arg)

	arg = arg.upper()

	for i in range(0, length):
		if arg[i] not in ['I', 'V', 'X', 'M', 'C', 'D', 'L']:
			return False
	
	return True
	
#Check if an argument is a number, character, or roman numeral
def valid_arg_check(arg):
	if number_check(arg) or char_check(arg) or roman_check(arg):
		return True
	else:
		return False



#Check if a command-line argument is an integer.
#http://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-in-python
def is_int(arg):
	try:
		int(arg)
	except ValueError:
		return False
	return True

# Can the string be represented as a float?
def is_float(arg):
	try:
		float(arg)
	except ValueError:
		return False
	return True

#Can the string be represented as a lower case char?
def is_lower_char(arg):	
	if len(arg) > 1:
		return False

	int_val = ord(arg)

	if int_val >= ord('a') and int_val <= ord('z'):
		return True
	else:
		return False	

#Can the string be represented as an upper case char?
def is_upper_char(arg):
	if len(arg) > 1:
		return False

	int_val = ord(arg)

	if int_val >= ord('A') and int_val <= ord('Z'):
		return True
	else:
		return False

#Can the string be represented as a lower case roman numeral?
def is_lower_roman(arg):
	length = len(arg)

	for i in range(0, length):
		if arg[i] not in ['i', 'v', 'x', 'm', 'c', 'd', 'l']:
			return False
	return True  

#Can the string be represented as an upper case roman numeral?
def is_upper_roman(arg):
	length = len(arg)

	for i in range(0, length):
		if arg[i] not in ['I', 'V', 'X', 'M', 'C', 'D', 'L']:
			return False
	return True

#Is this integer increment reasonable?
def int_increment_check(arg):
	if arg[0] == '-':
		if arg[1:].isdigit():
			return True
	if arg.isdigit():
		return True
	else:
		return False

#Check if a command-line argument is a valid/reasonable option
def option_check(arg):
	#Make sure it's not an empty string before checking if it is an option.
	if arg == "":
		print "Invalid option: empty string detected"
		exit(1)

	#If it is a valid option, return true
	if arg[0] == '-' or arg[0] == '--':
		if arg == '-h' or arg == '--help':
			return True
		elif arg == '-v' or arg == '--version':
			return True
		elif arg == '-s' or arg == '--seperator':
			return True
		elif arg == '-f' or arg == '--format':
			return True
		elif arg == '-w' or arg == '--equal-width':
			return True
		elif arg == '-W' or arg == '--words':
			return True
		elif arg == '-p' or arg == '--pad':
			return True
		elif arg == '-P' or arg == '--pad-spaces':
			return True
		elif arg == '-F' or arg == '--format-word':
			return True
		elif arg == '-n' or arg == '--number-lines':
			return True
		else:
			print str(arg) + ": Invalid option"
			exit(1)
	else: 
		return False

#Print sequence of numbers, only use if you're sure start, end, inc, are integers
#Probably could get rid of this routine and write a general one that can print using either integers or floats.
def print_sequence(start, end, inc, sep, equal_width, padded, pad):

	#Figure out how wide to set each string to if equal width is an option
	if len(str(start)) > len(str(end)): 
		size = len(str(start))
	else:
		size = len(str(end))
	
	if inc > 0:	
		for i in range(start, end+1, inc):
			if equal_width:
				sys.stdout.write(str(i).zfill(size) + sep)
			elif padded:
				sys.stdout.write(char_pad(str(i),pad,size) + sep)
			else:
				sys.stdout.write(str(i) + sep)
	elif inc < 0:
		for i in range(start, end-1, inc):
			if equal_width:
				sys.stdout.write(str(i).zfill(size) + sep)
			elif padded:
				sys.stdout.write(char_pad(str(i),pad,size) + sep)
			else:
				sys.stdout.write(str(i) + sep)
	
	if not sep == '\n':
		sys.stdout.write('\n')

#Number each line in a file with an integer value.  Begin with start, increase by increment
def number_file_int(start, end, inc, sep, equal_width, padded, pad, file_stuff):
	
	if len(str(start)) > len(str(end)):
		size = len(str(start))
	else:
		size = len(str(end))

	for i in range(0, end):
		if equal_width:
			sys.stdout.write(str(start+(i * inc)).zfill(size) + sep + file_stuff[i])
		elif padded:
			sys.stdout.write(char_pad(str(start+(i * inc)),pad,size) + sep + file_stuff[i])
		else:
			sys.stdout.write(str(start+(i * inc)) + sep + file_stuff[i])

#Number each line in a file with a floating point value.  Begin with start, increase each value by increment
def number_file_float(start, end, inc, sep, equal_width, form, padded, pad, file_stuff):
	try:
		size = len(str(form % start)) 
	except Exception:
		print str(form) + ": Invalid format."
		exit(1)
	
	for i in range(0, end):
		if equal_width:
			try:
				sys.stdout.write(str( (form % start+(i * inc)).zfill(size)) + sep + file_stuff[i])
			except Exception:
				print str(form) + ": Invalid format."
				exit(1)
		elif padded:
			try:
				sys.stdout.write(str( char_pad(form % start+(i * inc),pad,size)) + sep + file_stuff[i])
			except Exception:
				print str(form) + ": Invalid format."
				exit(1)

		else:
			try:
				sys.stdout.write(str(form % (start+(i*inc))) + sep + file_stuff[i])
			except Exception:
				print str(form) + ": Invalid format."
				exit(1)

#Generate a list of values between start and end, by increments of step.
#http://stackoverflow.com/questions/4189766/python-range-with-step-of-type-float
def float_range(start, end, step):
	tiny = .00000000001
	result = []
	
	if step > 0:
		while start < end+tiny:
			result.append(start)
			start = start + step
	else:
		while start > end-tiny:
			result.append(start)
			start = start + step	

	return result	

#Print sequence of numbers, used when one of start, end, or inc are known to be floating point numbers
#add cases for pad option
def print_float_sequence(start, end, inc, sep, equal_width, form, padded, pad):
	#Figure out how wide to set each string if equal width is an option
	try:
		if len(str(form % start)) > len(str(form % end)): 
			size = len(str(form % start))
		else:
			size = len(str(form % end))
	except Exception:
		print str(form) + ": Invalid format."
		exit(1)
	
	for i in float_range(start, end, inc):
		if equal_width:
			try:
				sys.stdout.write(str(form % i).zfill(size) + sep)
			except Exception:
				print str(form) + ": Invalid format."
				exit(1)
		elif padded:
			try:
				sys.stdout.write(char_pad(str(form % i),pad,size) + sep)
			except Exception:
				print str(form) + ": Invalid format."
				exit(1)
		else:
			try: 
				sys.stdout.write(str(form % i) + sep)
			except Exception:
				print str(form) + ": Invalid format"
				exit(1)

	if not sep == '\n':
		sys.stdout.write('\n')

#Print sequence of characters
def print_char_sequence(start, end, inc, sep):
	if inc > 0:
		if ord(start) > ord(end):
			exit(0)
		for i in range(ord(start), ord(end)+1, inc):
			sys.stdout.write(chr(i) + sep)

	elif inc < 0:
		if ord(start) < ord(end):
			exit(0)

		for i in range(ord(start), ord(end)-1, inc):
			sys.stdout.write(chr(i) + sep)

	if not sep == '\n':
		sys.stdout.write('\n')

# 'number' each line in a file with characters.  Begin with start, increase value by increment
def number_file_alpha(start, end, inc, sep, file_stuff):
	if inc > 0:
		for i in range(0, end):
			if ord(start) + (i*inc) > ord('z'):
				sys.stdout.write(file_stuff[i])
			else:
				sys.stdout.write(chr(ord(start)+(i*inc)) + sep + file_stuff[i])
	elif inc < 0:
		for i in range(0, end):
			if ord(start) + (i*inc) < ord('a'):
				sys.stdout.write(file_stuff[i])
			else:
				sys.stdout.write(chr(ord(start)+(i*inc)) + sep + file_stuff[i])

# 'number' each line in a file with upper case characters.  Begin with start, increase value by increment	
def number_file_ALPHA(start, end, inc, sep, file_stuff):
	if inc > 0:
		for i in range(0, end):
			if ord(start) + (i*inc) > ord('Z'):
				sys.stdout.write(file_stuff[i])
			else:
				sys.stdout.write(chr(ord(start)+(i*inc)) + sep + file_stuff[i])
	elif inc < 0:
		for i in range(0, end):
			if ord(start) + (i*inc) < ord('A'):
				sys.stdout.write(file_stuff[i])
			else:
				sys.stdout.write(chr(ord(start)+(i*inc)) + sep + file_stuff[i])

#I found this routine on: http://code.activestate.com/recipes/81611-roman-numerals/
#It converts its argument from a roman numeral to an integer
def roman_to_int(arg):
	arg = arg.upper()
	
	rom_list = ['M', 'D', 'C', 'L', 'X', 'V', 'I']
	int_list = [1000, 500, 100, 50, 10, 5, 1]
	places = []

	for c in arg:
		if not c in rom_list:
			print "Error, invalid roman numeral"
			exit(1)
	for i in range(len(arg)):
		c = arg[i]
		value = int_list[rom_list.index(c)]
	
		try:
			nextvalue = int_list[rom_list.index(arg[i+1])]
			if nextvalue > value:
				value *= -1
		except IndexError:
			pass

		places.append(value)

	sum = 0
	
	for n in places:
		sum += n

	if int_to_roman(sum) == arg:
		return sum
	else:
		print "Error, invalid roman numeral!"
		exit(1)

#I found this routine on: http://code.activestate.com/recipes/81611-roman-numerals/
#It converts its argument from an integer to a roman numeral
def int_to_roman(arg):
	if arg < 1 or arg > 3999:
		print "Error: roman numerals must be between 1 and 3999"
		exit(1)

	int_list = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
	rom_list = ['M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I']
	result = ""

	for i in range(len(int_list)):
		count = int(arg / int_list[i])
		result += rom_list[i] * count
		arg -= int_list[i] * count
	return result	

#Print sequence of roman numerals
def print_roman_sequence(start, end, inc, upper, sep, equal_width, padded, pad):
	start = roman_to_int(start)
	inc = roman_to_int(inc)
	end = roman_to_int(end)
	width = 0
	result = []

	for i in range(start, end+1, inc):
		if len(int_to_roman(i)) > width:
			width = len(int_to_roman(i))
		
	for j in range(start, end+1, inc):
		if equal_width:
			if upper:
				sys.stdout.write(char_pad(str(int_to_roman(j)), ' ', width) + sep)
			else:
				sys.stdout.write(char_pad(str(int_to_roman(j)).lower(), ' ', width) + sep)
		elif padded:
			if upper:
				sys.stdout.write(char_pad(str(int_to_roman(j)),pad,width) + sep)
			else:
				sys.stdout.write(char_pad(str(int_to_roman(j)),pad,width).lower() + sep)
		else:
			if upper:
				sys.stdout.write(int_to_roman(j) + sep)
			else:
				sys.stdout.write(int_to_roman(j).lower() + sep)

	if not sep == '\n':
		sys.stdout.write('\n')

#Number lines in a file with roman numerals.  The first line is numbered by 'start', and the value
#on subsequent lines increases by the increment.  The routine prevents going beyond the limits of
#what roman numerals can be represented.
def number_file_roman(start, end, inc, upper, sep, equal_width, padded, pad, file_stuff):
	start = roman_to_int(start)
	inc = roman_to_int(inc)
	width = 0
	result = []

	for i in range(start, (start + (inc * end))-1, inc):
		if i < 1 or i > 3999: #roman numerals must be between 1 and 3999
			break
		else:
			if len(int_to_roman(i)) > width:
				width = len(int_to_roman(i))
	#if inc > 0:
	for j in range(0, end):
		if start+(j*inc) > 3999:
			sys.stdout.write(file_stuff[j])
		elif equal_width:
			if upper:
				sys.stdout.write(char_pad(str(int_to_roman(start + (j*inc))),' ', width) + sep + file_stuff[j])
			else:
				sys.stdout.write(char_pad(str(int_to_roman(start + (j*inc))),' ',width).lower() + sep + file_stuff[j])
		elif padded:
			if upper:
				sys.stdout.write(char_pad(str(int_to_roman(start + (j*inc))),pad,width) + sep + file_stuff[j])
			else:
				sys.stdout.write(char_pad(str(int_to_roman(start + (j*inc))),pad,width).lower() + sep + file_stuff[j])
		else:
			if upper:
				sys.stdout.write(str(int_to_roman(start + (j*inc))) + sep + file_stuff[j])
			else:
				sys.stdout.write(str(int_to_roman(start + (j*inc))).lower() + sep + file_stuff[j]) 
	
#Find the argument with the most decimal places, use that to format floating-point numbers when no
#format option is present.
#http://stackoverflow.com/questions/6189956/easy-way-of-finding-decimal-places
def highest_precision(*arg):
	most = 0
	temp = 0
	
	for i in range(0, len(arg)):
		temp = decimal.Decimal(arg[i])
		if temp.as_tuple().exponent < most:
			most = temp.as_tuple().exponent

	return abs(most)

#Pad 'arg' to the left with 'pad_str' to be length of 'size'
def char_pad(arg, pad_str, size):
	for i in range(0, size-1):
		#If the length of the argument is less then the size, start padding
		if len(arg) < size:
			arg = pad_str+arg
	return arg

##################################################################################

def main(): 
	default_seperator = '\n'
	default_increment = 1
	default_format_string = "%.1f"
	default_pad = ' '
	
	num_cmd_line_args = len(sys.argv) #total number of command line arguments
	seperator = default_seperator #string used between numbers
	increment = default_increment #Increment value
	is_equal_width = False #Is the equal width option used?
	form_str = default_format_string #format string
	is_padded = False #Is the padded option used?
	pad = default_pad #pad string
	format_word = " " #format-word provided by option, or inferred from arguments
	is_upper_case = False #upper or lower case roman numerals?
	is_numbered = False #Is there a file to be numbered?
	
	arg_count = 0 #total number arguments
	option_count = 0 #total options
	format_count = 0 #instances of format option
	prec = 0 #precision of argument with most decimal places
	
	first = " " #The first argument (start)
	second = " " #the second argument (end)
	
	num_file_lines = 0 #number of lines in the file
	file_contents = "" #list of all lines of a file
	
	#No arguments were sent in
	if num_cmd_line_args < 2:
		print "Usage error: no arguments"
		print "Try sequ -h for instructions"
		exit(1)
	
	#Figure out how many options and arguments there are
	for i in range(1, 4):
		#Start at the last argument, go backwards until a non-number is encountered
		if valid_arg_check(sys.argv[-i]): 
			arg_count = arg_count+1
		else:
			break
	
	#Check for options
	for i in range (1, num_cmd_line_args-arg_count):
		if option_check(sys.argv[i]):
			option_count = option_count+1
			
			#Count number of format options
			if sys.argv[i] in ['-f', '--format']:
				format_count = format_count+1
	
		else:
			#If something else is in the list of options, the previous item better be format, seperator or pad.
			if sys.argv[i-1] not in ['-f', '--format', '-s', '--seperator', '-p', '--pad', '-F', '--format-word']: 
				print str(sys.argv[i]) + ": Invalid option"
				exit(1)
	
	#Special case where user only wants to see version or help
	if option_count == 1 and arg_count == 0:
		if version_check(sys.argv[1]):
			print_version()
			exit(0)
		if help_check(sys.argv[1]):
			print_help()
			exit(0)
	
	#If the number of arguments is not 2 or 3, get out!
	if arg_count < 2 or arg_count > 3:
		print "Usage error: Incorrect number of arguments"
		print "Try sequ -h for instructions"
		exit(1)
	
			
	#process the options, if there are any, then print the right sequence of numbers
	for i in range(1, num_cmd_line_args-arg_count):
		arg = sys.argv[i]
		
		if arg == '-h' or arg == '--help':
			print_help()
			exit(0)
	
		elif arg == '-v' or arg == '--version':
			print_version()
			exit(0)
	
		elif arg == '-s' or arg == '--seperator':
			seperator = sys.argv[i+1] 
	
		elif arg == '-w' or arg == '--equal-width':
			is_padded = False
			is_equal_width = True
	
		elif arg == '-f' or arg == '--format':
			form_str = sys.argv[i+1]
	 
		elif arg == '-W' or arg == '--words':
			seperator = ' '
	
		elif arg == '-p' or arg == '--pad':
			is_equal_width = False
			is_padded = True
			pad = sys.argv[i+1]
			if len(pad) > 1:
				print str(pad) + ": Invalid pad, must be single character."
				exit(1)
	
		elif arg == '-P' or arg == '--pad-spaces':
			is_equal_width = False
			is_padded = True
			pad = default_pad
	
		elif arg == '-F' or arg == '--format-word':
			if sys.argv[i+1] in ['arabic', 'floating', 'alpha', 'ALPHA', 'roman', 'ROMAN']:
				format_word = sys.argv[i+1]
			else:
				print sys.argv[i+1] + ": Invalid format word."
				exit(1)
		
		elif arg == '-n' or arg == '--number-lines':
			if arg_count > 2:
				print "Usage error: Too many arguments for number-lines option"
				exit(1)
			
			if seperator == default_seperator:
				seperator = ' '
	
			is_numbered = True
			file_contents = sys.stdin.readlines()
			num_file_lines = len(file_contents)
	
	#Assign arguments to the proper variables
	if arg_count == 2 and not is_numbered:
		first = sys.argv[num_cmd_line_args-2]
		second = sys.argv[num_cmd_line_args-1]
	
	elif arg_count == 2 and is_numbered:
		first = sys.argv[num_cmd_line_args-2]
		second = num_file_lines
		increment = sys.argv[num_cmd_line_args-1]
	
	elif arg_count == 3:
		first = sys.argv[num_cmd_line_args-3]
		second = sys.argv[num_cmd_line_args-1]
		increment = sys.argv[num_cmd_line_args-2]
	
	
	#No format word option present, infer format from last argument
	if format_word == " " and not is_numbered:
		if is_int(sys.argv[num_cmd_line_args-1]):
			format_word = "arabic"
		elif is_float(sys.argv[num_cmd_line_args-1]):
			format_word = "floating"
		elif is_lower_char(sys.argv[num_cmd_line_args-1]):
			format_word = "alpha"
		elif is_upper_char(sys.argv[num_cmd_line_args-1]):
			format_word = "ALPHA"
		elif is_lower_roman(sys.argv[num_cmd_line_args-1]):
			format_word = "roman"
		elif is_upper_roman(sys.argv[num_cmd_line_args-1]):
			format_word = "ROMAN"
		else:
			print sys.argv[num_cmd_line_args-1] + ": Error, could not infer format word"
			exit(1)
	#else infer from start arg, depending on number of arguments
	elif format_word == " " and is_numbered:
		if is_int(sys.argv[num_cmd_line_args-2]):
			format_word = "arabic"
		elif is_float(sys.argv[num_cmd_line_args-2]):
			format_word = "floating"
		elif is_lower_char(sys.argv[num_cmd_line_args-2]):
			format_word = "alpha"
		elif is_upper_char(sys.argv[num_cmd_line_args-2]):
			format_word = "ALPHA"
		elif is_lower_roman(sys.argv[num_cmd_line_args-2]):
			format_word = "roman"
		elif is_upper_roman(sys.argv[num_cmd_line_args-2]):
			format_word = "ROMAN"
		else:
			print sys.argv[num_cmd_line_args-2] + ": Error, could not infer format word"
			exit(1)
	
	#Make sure the increment is appropriate for the format word.
	if format_word in ["arabic", "alpha", "ALPHA"]:
		if is_int(increment):	
			if int(increment) == 0:
				print "Error: Invalid increment, cannot be zero."
				exit(1)
		else:
			print "Error: Increment must be an integer."
			exit(1)
		
	
	if format_word == "floating":
		if is_float(increment):
			if float(increment) == 0:
				print "Error: Invalid increment, cannot be zero."
				exit(1)
		else:
			print "Error: Increment must be a floating point number."
			exit(1)
	
	if format_word == "roman":
		if arg_count == 2 and not is_numbered:
			increment = "i"	
	
		if is_lower_roman(increment):
			if roman_to_int(increment) < 1 or roman_to_int(increment) > 3999:
				print "Error: Roman increment must be between 1 and 3999"
				exit(1)
		else:
			print "Error: Increment must be a roman numeral"
			exit(1)
	
	if format_word == "ROMAN":
		if arg_count == 2 and not is_numbered:
			increment = "I"
	
		if is_upper_roman(increment):
			if roman_to_int(increment) < 1 or roman_to_int(increment) > 3999:
				print "Error: Roman increment must be between 1 and 3999"
				exit(1)
		else:
			print "Error: Increment must be an upper case roman numeral."
			exit(1)
	
	#At this point we have all the information needed to print the sequence.  Select the right one and go!
	
	if format_word == "arabic":
		if is_int(first) and is_int(second):
			if is_numbered:
				number_file_int(int(first), int(second), int(increment), seperator, is_equal_width, is_padded, pad, file_contents)
			else:
				print_sequence(int(first), int(second), int(increment), seperator, is_equal_width, is_padded, pad)
		else:
			print "Error: mixed types, both start and end must be integers"
			exit(1)
	
	elif format_word == "floating":
		if is_float(first) and is_float(second):
	
			#No format option, find number of decimal places needed to represent all numbers well
			if format_count == 0: 
				prec = highest_precision(first, second, increment)
				#Rebuild format string
				form_str = form_str[:2] + str(prec) + form_str[3:] 
			if is_numbered:
				number_file_float(float(first), int(second), float(increment), seperator, is_equal_width, form_str, is_padded, pad, file_contents)
			else:
				print_float_sequence(float(first), float(second), float(increment), seperator, is_equal_width, form_str, is_padded, pad)
	
		else:
			print "Error: mixed types, both start and end must be floats"
			exit(1)
	
	elif format_word == "alpha":
		if is_lower_char(first) and is_numbered:
			number_file_alpha(first, int(second), int(increment), seperator, file_contents)
		elif is_lower_char(first) and is_lower_char(second):
				print_char_sequence(first, second, int(increment), seperator)
		else:
			print "Error: mixed types, both start and end must be lower case characters"
	
	elif format_word == "ALPHA":
		if is_upper_char(first) and is_numbered:
			number_file_ALPHA(first, int(second), int(increment), seperator, file_contents)
		elif is_upper_char(first) and is_upper_char(second):
			print_char_sequence(first, second, int(increment), seperator)
		else:
			print "Error: mixed types, both start and end must be upper case characters"
	
	elif format_word == "roman":
		if is_lower_roman(first) and is_numbered:
			number_file_roman(first, int(second), increment, is_upper_case, seperator, is_equal_width, is_padded, pad, file_contents)	
		elif is_lower_roman(first) and is_lower_roman(second):
			print_roman_sequence(first, second, increment, is_upper_case, seperator, is_equal_width, is_padded, pad)
		else:
			print "Error: mixed types, both start and end must be lower case roman numerals"
	
	elif format_word == "ROMAN":
		if is_upper_roman(first) and is_numbered:
			is_upper_case = True
			number_file_roman(first, int(second), increment, is_upper_case, seperator, is_equal_width, is_padded, pad, file_contents)
		elif is_upper_roman(first) and is_upper_roman(second):
			is_upper_case = True
			print_roman_sequence(first, second, increment, is_upper_case, seperator, is_equal_width, is_padded, pad)
		else:
			print "Error: mixed types, both start and end must be upper case roman numerals"
	
# End of main

main()
exit(0)
