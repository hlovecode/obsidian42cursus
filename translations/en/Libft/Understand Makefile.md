A project contains countless source files, which are placed in several directories according to their types, functions, and modules. A Makefile defines a series of rules to specify which files need to be compiled first, which need to be compiled later, which need to be recompiled, and even to perform more complex operations.

### The Relationship Between Make and Makefile

`make` is a command-line tool that interprets the instructions in a Makefile.
The Makefile describes the compilation order and compilation rules for all files in the entire project.
When `make` executes, it reads the rules in the Makefile.

### Makefile Naming Rules

`Makefile` or `makefile`, commonly named `Makefile`.