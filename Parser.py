"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """
    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient 
    access to their components. 
    In addition, it removes all white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Gets ready to parse the input file.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is:
        # input_lines = input_file.read().splitlines()

        input_lines = input_file.read().splitlines()
        valid_input_lines = []
        # remove white spaces:
        for line in input_lines:
            # Ignore blank rows
            if not line:
                continue
            # Handling comments
            ind = line.find("//")
            if ind == (-1):
                valid_input_lines.append(" ".join(line.split()))
            else:  # there is a comment
                new_line = line[0:ind].strip()
                if new_line:  # new line is not ""
                    valid_input_lines.append(" ".join(new_line.split()))
        self._input_lines = valid_input_lines
        self._num_of_lines = len(valid_input_lines)
        self._curr_index = 0
        self._arithmetic_list = {"add", "sub", "neg", "eq", "gt",
                                 "lt", "and", "or", "not", "shiftleft",
                                 "shiftright"}


    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        # Your code goes here!
        return self._curr_index <= self._num_of_lines - 1


    def advance(self) -> None:
        """Reads the next command from the input and makes it the current 
        command. Should be called only if has_more_commands() is true. Initially
        there is no current command.
        """
        # Your code goes here!
        self._curr_index += 1

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        # project 7  so may be: "C_ARITHMETIC", "C_PUSH", "C_POP"

        type_command = self._input_lines[self._curr_index].split(' ')[0]

        if type_command in self._arithmetic_list:
            return "C_ARITHMETIC"
        elif type_command == "push":
            return "C_PUSH"
        elif type_command == "pop":
            return "C_POP"
        elif type_command == "label":
            return "C_LABEL"
        elif type_command == "if-goto":
            return "C_IF"
        elif type_command == "goto":
            return "C_GOTO"
        elif type_command == "function":
            return "C_FUNCTION"
        elif type_command == "call":
            return "C_CALL"
        elif type_command == "return":
            return "C_RETURN"


    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of 
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned. 
            Should not be called if the current command is "C_RETURN".
        """
        # C_ARITHMETIC :
        if self.command_type() == "C_ARITHMETIC":
            return self._input_lines[self._curr_index].split(' ')[0]
        # other case: pop or push or goto or if-goto or label:
        return self._input_lines[self._curr_index].split(' ')[1]


    def arg2(self) -> str:
        """
        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP", 
            "C_FUNCTION" or "C_CALL".
        """
        # project 7  so may be: "C_PUSH", "C_POP"
        return self._input_lines[self._curr_index].split(' ')[2]

