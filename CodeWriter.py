"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import os


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!

        self._output_file = output_stream
        self.filename = ""
        self._label_counter = 0
        self._function_label_counter = 0
        self._function_helper_list = []

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        self.filename = filename

    def write_arithmetic(self, command: str) -> None:
        """Writes the assembly code that is the translation of the given 
        arithmetic command.

        Args:
            command (str): an arithmetic command.
        """
        # Your code goes here!
        list = []
        if command == 'add':
            list = self.__add()
        elif command == 'sub':
            list = self.__sub()
        elif command == 'neg':
            list = self.__neg()
        elif command == 'eq':
            list = self.__eq()
        elif command == 'gt':
            list = self.__gt()
        elif command == 'lt':
            list = self.__lt()
        elif command == 'and':
            list = self.__and()
        elif command == 'or':
            list = self.__or()
        elif command == 'not':
            list = self.__not()
        elif command == 'shiftright':
            list = self.__shiftright()
        elif command == 'shiftleft':
            list = self.__shiftleft()

        # writes to the file the list of assembly commands:
        self.__write_list_to_file(list)

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes the assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # if push:
        if command == "C_PUSH":
            self.__write_push(segment, index)
        elif command == "C_POP":
            self.__write_pop(segment, index)

    def write_label(self, name_of_label: str) -> None:
        """Writes the assembly code that is the translation of the given
        command, where command is C_LABEL .

        Args:
            name_of_label (str): name of the label.
        """
        # Your code goes here!
        list = self.__label(name_of_label)
        self.__write_list_to_file(list)

    def write_ifgoto(self, name_of_label: str) -> None:
        """Writes the assembly code that is the translation of the given
        command, where command is C_IF .
        Args:
            name_of_label (str): name of the label.
        """
        # Your code goes here!
        list = self.__ifgoto(name_of_label)
        self.__write_list_to_file(list)


    def write_goto(self, name_of_label: str) -> None:
        """Writes the assembly code that is the translation of the given
        command, where command is C_GOTO .
        Args:
            name_of_label (str): name of the label.
        """
        # Your code goes here!
        list = self.__goto(name_of_label)
        self.__write_list_to_file(list)

    def write_function(self, name_of_function, number_of_arguments) -> None:
        """Writes the assembly code that is the translation of the given
        command, where command is C_FUNCTION .
        Args:
            name_of_function (str): name of the function.
            number_of_arguments(str): number of arguments
        """
        # Your code goes here!
        list = self.__function(name_of_function,number_of_arguments)
        self.__write_list_to_file(list)

    def write_call(self, name_of_function, number_of_arguments) -> None:
        """Writes the assembly code that is the translation of the given
        command, where command is C_CALL .
        Args:
            name_of_function (str): name of the function.
            number_of_arguments(str): number of arguments
        """
        # Your code goes here!
        list = self.__call(name_of_function,number_of_arguments)
        self.__write_list_to_file(list)

    def write_return(self) -> None:
        """Writes the assembly code that is the translation of the given
        command, where command is C_RETURN .
        """
        # Your code goes here!
        list = self.__return()
        self.__write_list_to_file(list)

    def write_bootstrap(self) -> None:
        """Writes bootstrap for the hack computer.
        """
        # Your code goes here!
        list = self.__bootstrap()
        self.__write_list_to_file(list)

    def check_function_list(self):
        """Check if there are more functions in the function's list, if true pop the last one .
        """
        if len(self._function_helper_list) > 0:
            self._function_helper_list.pop()

    def close(self) -> None:
        """Closes the output file."""
        # Your code goes here!
        self._output_file.close()

    # method that write to an open file the assembly commands:
    def __write_list_to_file(self, list_to_write):
        # called only when the output file is open with write option
        for asm_command in list_to_write:
            self._output_file.write(asm_command + '\n')

    # method that write to an open file the push commands:
    def __write_push(self, segment: str, index: int):
        list = []
        if segment == 'constant':
            list = self.__push_constant(index)
        elif segment == 'local':
            list = self.__push_local(index)
        elif segment == 'argument':
            list = self.__push_argument(index)
        elif segment == 'that':
            list = self.__push_that(index)
        elif segment == 'this':
            list = self.__push_this(index)
        elif segment == 'temp':
            list = self.__push_temp(index)
        elif segment == 'pointer':
            list = self.__push_pointer(index)
        elif segment == 'static':
            list = self.__push_static(index)
        # writes to the file the list of assembly commands:
        self.__write_list_to_file(list)

    # method that write to an open file the pop commands:
    def __write_pop(self, segment: str, index: int):
        list = []
        if segment == 'local':
            list = self.__pop_local(index)
        elif segment == 'argument':
            list = self.__pop_argument(index)
        elif segment == 'that':
            list = self.__pop_that(index)
        elif segment == 'this':
            list = self.__pop_this(index)
        elif segment == 'temp':
            list = self.__pop_temp(index)
        elif segment == 'pointer':
            list = self.__pop_pointer(index)
        elif segment == 'static':
            list = self.__pop_static(index)
        # writes to the file the list of assembly commands:
        self.__write_list_to_file(list)

    # Implementation of arithmetic commands:

    def __and(self):
        returned_list = ['@SP',
                         'M=M-1',
                         'A=M',
                         'D=M',
                         '@SP',
                         'M=M-1',
                         'A=M',
                         'D=D&M',
                         'M=D',
                         '@SP',
                         'M=M+1']

        return returned_list

    def __or(self):
        returned_list = ['@SP',
                         'M=M-1',
                         'A=M',
                         'D=M',
                         '@SP',
                         'M=M-1',
                         'A=M',
                         'D=D|M',
                         'M=D',
                         '@SP',
                         'M=M+1']

        return returned_list

    def __not(self):
        returned_list = ['@SP',
                         'M=M-1',
                         'A=M',
                         'D=!M',
                         'M=D',
                         '@SP',
                         'M=M+1']
        return returned_list

    def __neg(self):
        returned_list = ['@SP',
                         'M=M-1',
                         'A=M',
                         'D=-M',
                         'M=D',
                         '@SP',
                         'M=M+1']
        return returned_list

    def __shiftright(self):
        returned_list = ['@SP',
                         'M=M-1',
                         'A=M',
                         'M=M>>',
                         '@SP',
                         'M=M+1']
        return returned_list

    def __shiftleft(self):
        returned_list = ['@SP',
                         'M=M-1',
                         'A=M',
                         'M=M<<',
                         '@SP',
                         'M=M+1']
        return returned_list

    def __sub(self):
        returned_list = ['@SP',
                         'M=M-1',
                         'A=M',
                         'D=M',
                         '@SP',
                         'M=M-1',
                         'A=M',
                         'M=M-D',
                         '@SP',
                         'M=M+1']
        return returned_list

    def __add(self):
        returned_list = ['@SP',
                         'M=M-1',
                         'A=M',
                         'D=M',
                         '@SP',
                         'M=M-1',
                         'A=M',
                         'M=D+M',
                         '@SP',
                         'M=M+1']
        return returned_list

    def __eq(self):
        returned_list = ['@SP',
                         'AM=M-1',
                         'D=M', # the SECOND is pos or 0
                         '@SECOND_IS_POS' + str(self._label_counter),
                         'D;JGE',
                         '@SECOND_IS_NEG' + str(self._label_counter),
                         'D;JLT',
                         '(SECOND_IS_POS' + str(self._label_counter) + ')',
                         '@SP',
                         'A=M-1',
                         'D=M',
                         '@NOT_EQ' + str(self._label_counter),  # FIRST is negative
                         'D;JLT',
                         '@CHECK' + str(self._label_counter), # SECOND is also  positive or 0
                         'D;JGE',
                         '(SECOND_IS_NEG' + str(self._label_counter) + ')',
                         '@SP',
                         'A=M-1',
                         'D=M',
                         '@NOT_EQ' + str(self._label_counter), # FIRST is positive or 0
                         'D;JGE',
                         '@CHECK' + str(self._label_counter),
                          'D;JLT',   # FIRST is also  negative
                         '(CHECK' + str(self._label_counter) + ')',
                         '@SP',
                         'A=M',
                         'D=D-M',  # D is SECOND, M is FIRST
                         '@NOT_EQ' + str(self._label_counter),
                         'D;JNE',  # the difference != 0
                         '@EQ'+ str(self._label_counter),
                         'D;JEQ',   # the difference == 0
                         '(NOT_EQ' + str(self._label_counter) + ')',
                         '@SP',
                         'A=M-1',
                         'M=0',
                         '@FINAL' + str(self._label_counter),
                         'D;JMP',
                         '(EQ' + str(self._label_counter) + ')',
                         '@SP',
                         'A=M-1',
                         'M=-1',
                         '(FINAL' + str(self._label_counter) + ')']
        self._label_counter += 1
        return returned_list


    def __lt(self):
        returned_list = ['@SP',
                         'AM=M-1',
                         'D=M',  # the SECOND is pos or 0
                         '@SECOND_IS_POS' + str(self._label_counter),
                         'D;JGE',
                         '@SECOND_IS_NEG' + str(self._label_counter),
                         'D;JLT',
                         '(SECOND_IS_POS' + str(self._label_counter) + ')',
                         '@SP',
                         'A=M-1',
                         'D=M',
                         '@LT' + str(self._label_counter),  # FIRST is negative
                         'D;JLT',
                         '@CHECK' + str(self._label_counter), # FIRST is also  positive or 0
                         'D;JGE',
                         '(SECOND_IS_NEG' + str(self._label_counter) + ')',
                         '@SP',
                         'A=M-1',
                         'D=M',
                         '@NOT_LT' + str(self._label_counter), # FIRST is positive or 0
                         'D;JGE',
                         '@CHECK' + str(self._label_counter),
                          'D;JLT',   # FIRST is also  negative
                         '(CHECK' + str(self._label_counter) + ')',
                         '@SP',
                         'A=M',
                         'D=D-M',  # D is first, M is second
                         '@LT' + str(self._label_counter),
                         'D;JLT',  # the difference < 0
                         '@NOT_LT' + str(self._label_counter),
                         'D;JGE',   # the difference >= 0
                         '(NOT_LT' + str(self._label_counter) + ')',
                         '@SP',
                         'A=M-1',
                         'M=0',
                         '@FINAL' + str(self._label_counter),
                         'D;JMP',
                         '(LT' + str(self._label_counter) + ')',
                         '@SP',
                         'A=M-1',
                         'M=-1',
                         '(FINAL' + str(self._label_counter) + ')']
        self._label_counter += 1
        return returned_list

    def __gt(self):
        returned_list = ['@SP',
                         'AM=M-1',
                         'D=M',  # the first is pos or 0
                         '@SECOND_IS_POS' + str(self._label_counter),
                         'D;JGE',
                         '@SECOND_IS_NEG' + str(self._label_counter),
                         'D;JLT',
                         '(SECOND_IS_POS' + str(self._label_counter) + ')',
                         '@SP',
                         'A=M-1',
                         'D=M',
                         '@NOT_GT' + str(self._label_counter),  # first is negative
                         'D;JLT',
                         '@CHECK' + str(self._label_counter), # firsy is also  positive or 0
                         'D;JGE',
                         '(SECOND_IS_NEG' + str(self._label_counter) + ')',
                         '@SP',
                         'A=M-1',
                         'D=M',
                         '@GT' + str(self._label_counter),  # first is positive or 0
                         'D;JGE',
                         '@CHECK' + str(self._label_counter),
                          'D;JLT',   # FIRST is also  negative
                         '(CHECK' + str(self._label_counter) + ')',
                         '@SP',
                         'A=M',
                         'D=D-M',  # D is first, M is second
                         '@GT' + str(self._label_counter),
                         'D;JGT',  # the difference > 0
                         '@NOT_GT' + str(self._label_counter),
                         'D;JLE',   # the difference =< 0
                         '(NOT_GT' + str(self._label_counter) + ')',
                         '@SP',
                         'A=M-1',
                         'M=0',
                         '@FINAL' + str(self._label_counter),
                         'D;JMP',
                         '(GT' + str(self._label_counter) + ')',
                         '@SP',
                         'A=M-1',
                         'M=-1',
                         '(FINAL' + str(self._label_counter) + ')']
        self._label_counter += 1
        return returned_list

    # Implementation of push commands:
    def __push_constant(self, index):
        returned_list = ['@' + str(index),
                         'D=A',
                         '@SP',
                         'A=M',
                         'M=D',
                         '@SP',
                         'M=M+1']
        return returned_list

    def __push_local(self, index):
        returned_list = ['@' + str(index),
                         'D=A',
                         '@LCL',
                         'A=D+M',
                         'D=M',
                         '@SP',
                         'A=M',
                         'M=D',
                         '@SP',
                         'M=M+1']
        return returned_list

    def __push_argument(self, index):
        returned_list = ['@' + str(index),
                         'D=A',
                         '@ARG',
                         'A=D+M',
                         'D=M',
                         '@SP',
                         'A=M',
                         'M=D',
                         '@SP',
                         'M=M+1']
        return returned_list

    def __push_this(self, index):
        returned_list = ['@' + str(index),
                         'D=A',
                         '@THIS',
                         'A=D+M',
                         'D=M',
                         '@SP',
                         'A=M',
                         'M=D',
                         '@SP',
                         'M=M+1']
        return returned_list

    def __push_that(self, index):
        returned_list = ['@' + str(index),
                         'D=A',
                         '@THAT',
                         'A=D+M',
                         'D=M',
                         '@SP',
                         'A=M',
                         'M=D',
                         '@SP',
                         'M=M+1']
        return returned_list

    def __push_temp(self, index):
        returned_list = ['@' + str(index),
                         'D=A',
                         '@5',
                         'A=D+A',
                         'D=M',
                         '@SP',
                         'A=M',
                         'M=D',
                         '@SP',
                         'M=M+1']
        return returned_list

    def __push_static(self, index):
        returned_list = ['@' + self.filename + '.' + str(index),
                         'D=M',
                         '@SP',
                         'A=M',
                         'M=D',
                         '@SP',
                         'M=M+1']
        return returned_list

    def __push_pointer(self, index):
        returned_list = ['@' + str(index),
                         'D=A',
                         '@3',
                         'A=D+A',
                         'D=M',
                         '@SP',
                         'A=M',
                         'M=D',
                         '@SP',
                         'M=M+1']
        return returned_list

    def __pop_local(self, index):
        returned_list = ['@' + str(index),
                         'D=A',
                         '@LCL',
                         'D=D+M',
                         '@pop_label',
                         'M=D',
                         '@SP',
                         'M=M-1',
                         'A=M',
                         'D=M',
                         '@pop_label',
                         'A=M',
                         'M=D']
        return returned_list

    def __pop_argument(self, index):
        returned_list = ['@' + str(index),
                         'D=A',
                         '@ARG',
                         'D=D+M',
                         '@pop_label',
                         'M=D',
                         '@SP',
                         'M=M-1',
                         'A=M',
                         'D=M',
                         '@pop_label',
                         'A=M',
                         'M=D']
        return returned_list

    def __pop_this(self, index):
        returned_list = ['@' + str(index),
                         'D=A',
                         '@THIS',
                         'D=D+M',
                         '@pop_label',
                         'M=D',
                         '@SP',
                         'M=M-1',
                         'A=M',
                         'D=M',
                         '@pop_label',
                         'A=M',
                         'M=D']
        return returned_list

    def __pop_that(self, index):
        returned_list = ['@' + str(index),
                         'D=A',
                         '@THAT',
                         'D=D+M',
                         '@pop_label',
                         'M=D',
                         '@SP',
                         'M=M-1',
                         'A=M',
                         'D=M',
                         '@pop_label',
                         'A=M',
                         'M=D']
        return returned_list

    def __pop_temp(self, index):
        returned_list = ['@' + str(index),
                         'D=A',
                         '@5',
                         'D=D+A',
                         '@pop_label',
                         'M=D',
                         '@SP',
                         'M=M-1',
                         'A=M',
                         'D=M',
                         '@pop_label',
                         'A=M',
                         'M=D']
        return returned_list

    def __pop_static(self, index):
        returned_list = ['@SP',
                         'M=M-1',
                         'A=M',
                         'D=M',
                         '@' + self.filename + '.' + str(index),
                         'M=D']
        return returned_list

    def __pop_pointer(self, index):
        returned_list = ['@' + str(index),
                         'D=A',
                         '@3',
                         'D=D+A',
                         '@pop_label',
                         'M=D',
                         '@SP',
                         'M=M-1',
                         'A=M',
                         'D=M',
                         '@pop_label',
                         'A=M',
                         'M=D']
        return returned_list

    def __label(self, name_of_label):
        if len(self._function_helper_list) > 0:
            name_of_function = self._function_helper_list[-1]
            returned_list = ['(' + name_of_function + '$' + name_of_label + ')']

        else:
            returned_list = ['(' + name_of_label + ')']
        return returned_list

    def __ifgoto(self, name_of_label):
        returned_list = ['@SP',
                         'M=M-1',
                         'A=M',
                         'D=M',
                         ]
        if len(self._function_helper_list) > 0:
            name_of_function = self._function_helper_list[-1]
            label_to_append_list = '@' + name_of_function + '$' + name_of_label
        else:
            label_to_append_list = '@' + name_of_label

        returned_list.append(label_to_append_list)
        returned_list.append("D;JNE")
        return returned_list

    def __goto(self, name_of_label):
        if len(self._function_helper_list) > 0:
            name_of_function = self._function_helper_list[-1]
            label_to_append_list = '@' + name_of_function + '$' + name_of_label
        else:
            label_to_append_list = "@" + name_of_label

        returned_list = [label_to_append_list,
                         "0;JMP"]
        return returned_list

    def __function(self,name_of_function, number_of_arguments):
        self._function_helper_list.append(name_of_function)
        list = ["(" + name_of_function + ")"]
        for i in range(int(number_of_arguments)):
            list.append('@0')
            list.append('D=A')
            list.append('@SP')
            list.append('A=M')
            list.append('M=D')
            list.append('@SP')
            list.append('M=M+1')
        return list

    def __return(self):
        # end_frame = LCL
        # *ARG = pop()
        # SP = ARG + 1
        # THAT = *(end_frame - 1)
        # THIS = *(end_frame - 2)
        # ARG = *(end_frame - 3)
        # LCL = *(end_frame - 4)
        # goto return_address
        list = ["@LCL",
                "D=M",
                "@end_frame",
                "M=D",
                "@5",
                'D=D-A',
                'A=D',
                "D=M",
                "@return_address",
                "M=D",
                "@SP",
                "M=M-1",
                "A=M",
                "D=M",
                "@ARG",
                "A=M",
                "M=D",
                "@ARG",
                "D=M+1",
                "@SP",
                "M=D",
                "@end_frame",
                "D=M",
                "@1",
                'D=D-A',
                 'A=D',
                "D=M",
                "@THAT",
                "M=D",
                "@end_frame",
                "D=M",
                "@2",
                'D=D-A',
                'A=D',
                "D=M",
                "@THIS",
                "M=D",
                "@end_frame",
                "D=M",
                "@3",
                'D=D-A',
                'A=D',
                "D=M",
                "@ARG",
                "M=D",
                "@end_frame",
                "D=M",
                "@4",
                'D=D-A',
                'A=D',
                "D=M",
                "@LCL",
                "M=D",
                "@return_address",
                "A=M",
                "0;JMP"]
        return list

    def __call(self,name_of_function, number_of_arguments):
        list = [
            '@' + name_of_function + '$ret.' + str(self._function_label_counter),
            'D=A',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            # push LCL
            '@LCL',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            # push ARG
            '@ARG',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            # push THIS
            '@THIS',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            # push THAT
            '@THAT',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            # ARG = SP - 5 - number of arguments
            'D=M',
            "@" + str(5 + int(number_of_arguments)),
            'D=D-A',
            '@ARG',
            'M=D',
            # LCL = SP
            '@SP',
            'D=M',
            '@LCL',
            'M=D',
            # goto name_of_function
            '@' + name_of_function,
            '0;JMP',
            # (return address)
            '(' + name_of_function + '$ret.' + str(self._function_label_counter) + ')']
        self._function_label_counter += 1
        return list

    def __bootstrap(self):
        list = [
            # SP=256
            '@256',
            'D=A',
            '@SP',
            'M=D',
            # push return address
            '@Bootstrap$ret',
            'D=A',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            # push LCL
            '@LCL',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            # push ARG
            '@ARG',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            # push THIS
            '@THIS',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            # push THAT
            '@THAT',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            # ARG = SP - 5
            '@SP',
            'D=M',
            '@5',
            'D=D-A',
            '@ARG',
            'M=D',
            # LCL = SP
            '@SP',
            'D=M',
            '@LCL',
            'M=D',
            # goto function_name
            '@Sys.init',
            '0;JMP',
            # (return address)
            '(Bootstrap' + '$ret)']
        return list

