# caven
Standard structure and Makefile for modular C++ development.

## Navigate the readme
Jump to the section you'd like to read
1. [The problem and the solution (pitch bulshit)](#the-problem-and-the-solution)
2. [Actual information about Caven](#actual-information)

# The problem and the solution (pitch bulshit)

## Compiling in C made easy

Why is it so hard to compile projects in C? Many other languages are so much easier to run, I'll just compare it with Java.

## Java projects and Maven

In Java there is Maven, which for the ones that don't know Java, to put it simply, is amazing. 

Maven provides a standard way of compiling projects.
Adding a dependency to yout code is simply done by including in a xml file another project. And if you want to use import your project from another one the process is the same. Maven provides a standard project structure so that everything fit together like legos. 

Maven provides other useful things, for exemple an online repository for projects. When you don'tn have a dependency in your machine maven seemlessly downloads that dependency so that you can program without worrying about downloading and instaling packages.

So if you want to compile your code you simply type "mvn install" in your terminal and magic happens.

Maven also provides unit test support and other features.


## But it wasn't always like this with Java...

In the bad old days, Java was like C: a nightmare to compile big projects. You needed to compile it with horrible commands like:

```shell
javac -cp "./some_dir/more_jar_files.jar" MyClass.java # for a single dependency
```
"But it is not that ugly" you say... I say: we deserve better!

# Actual information

*Caven allows to easily import other Caven projects*

This feature is what this is all about! Making code into well defined modules, that fit like legos.

## What does caven actually do
Caven allows simple modular development:
 - Caven projects have a well defined structure
 - Caven provides generic makefile (caven_make) for projects with the caven structure.
 - *Caven allows to easily import other Caven projects*

Caven also allows multiple levels of not giving a fuck:
 - Level 1: just import the caven_make in your make file and develop your project with no dependencies
 - Level 2: specify the directories of other caven projects (dependencies) in your makefile

## The Caven project structure

A caven project has the following structure:

F_NAME
+---include (interfaces)
+---src     (source files)
+---Makefile
+---caven_make (caven provides this file)

If you want to get more fancy, here is all the directories caven recognizes:
F_NAME
+---include
|   +---(interfaces.hpp ...)
|   +---hide
|       +--- (hiden_interfaces.hpp ...)
+---src (source files)
+---test
|   +---(unit_tests_executables.cpp ...)      // these unit tests are run automatically with *make test*
|   +---manual
|       +---(unit_tests_executables.cpp ...)  // compiled as executables but aren't run automatically
|
+---executables
    +--- (executables.cpp...)                 // work as executables or examples for your library



## The Caven behaviour
When the project is built with caven, the build folder gets the following structure.

build
+---F_NAME
   +---include
   |  +---F_NAME
   |     +---(header tree)
   +---lib
   |  +---libF_NAME.a
   |
   +---dependencies
      +---FIRST_DEP
      |  +---(same structure as build/F_NAME)
      +---SECOND_DEP
      +---THIRD_dep
      (ect...)

Caven compiles executables by:
 - include all "include" directories
 - link all lib directories and files inside them


   

