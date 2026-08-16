A project contains countless source files, which are placed in several directories according to their type, function, and module. A Makefile defines a series of rules to specify which files need to be compiled first, which need to be compiled later, which need to be recompiled, and even to perform more complex operations.

### The Relationship Between Make and Makefile

`make` is a command-line tool that interprets the instructions in a Makefile.
The compilation order and rules for all files in the entire project are described in the Makefile.
When `make` executes, it reads the rules in the Makefile, but you need to write the Makefile yourself.

### Makefile Naming Rules

`Makefile` or `makefile`, generally `Makefile` is used.



### PS: Supplementary Information

#### `gcc (g++) <options> <sourcefile>`