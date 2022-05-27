"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from Parser import Parser
from CodeWriter import CodeWriter


def translate_file(
        input_file: typing.TextIO, codeWriter) -> None:
    """Translates a single file.

    Args:
        input_file (typing.TextIO): the file to translate.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # Note: you can get the input file's name using:
    # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))

    parser = Parser(input_file)
    input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
    code_writer.set_file_name(input_filename)
    while parser.has_more_commands():
        command_type = parser.command_type()
        if command_type == "C_ARITHMETIC":
            code_writer.write_arithmetic(parser.arg1())
        if command_type == "C_PUSH" or command_type == "C_POP":  # push or pop command
            code_writer.write_push_pop(command_type, parser.arg1(), parser.arg2())
        if command_type == "C_LABEL":
            code_writer.write_label(parser.arg1())
        if command_type == "C_IF":
            code_writer.write_ifgoto(parser.arg1())
        if command_type == "C_GOTO":
            code_writer.write_goto(parser.arg1())
        if command_type == "C_FUNCTION":
            code_writer.write_function(name_of_function=parser.arg1(),
                                       number_of_arguments=parser.arg2())
        if command_type == "C_CALL":
            code_writer.write_call(name_of_function=parser.arg1(),
                                       number_of_arguments=parser.arg2())
        if command_type == "C_RETURN":
            code_writer.write_return()
        parser.advance()



if "__main__" == __name__:
    # Parses the input path and calls translate_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: VMtranslator <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_translate = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
        output_path = os.path.join(argument_path, os.path.basename(
            argument_path))
    else:
        files_to_translate = [argument_path]
        output_path, extension = os.path.splitext(argument_path)
    output_path += ".asm"
    with open(output_path, 'w') as output_file:
        code_writer = CodeWriter(output_file)
        code_writer.write_bootstrap()
        for input_path in files_to_translate:
            filename, extension = os.path.splitext(input_path)
            if extension.lower() != ".vm":
                continue
            with open(input_path, 'r') as input_file:
                translate_file(input_file, code_writer)
        code_writer.check_function_list()
        code_writer.close()
