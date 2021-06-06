# caven
Standard structure and Makefile for modular C/C++ development.

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
javac -cp "./some_dir/more_jar_files.jar" MyClass.java # for a sindle dependency
```
"But it is not that ugly" you say... I say: we deserve better!


