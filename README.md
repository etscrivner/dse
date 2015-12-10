# Personal Software Process Exercises

This directory contains the programs I created while completing the Personal
Software Process (PSP) exercises. In addition, it contains the data and designs
collected and created when completing the exercises. The folders are organized
as follows:

* _bin_ - Contains the binary files for each exercise.
* _fixtures_ - Contains any data files used to test the exercise programs.
* _lib_ - Contains reusable python libraries created throughout the exercises.
* _tests_ - Contains unit-tests for the reusable library components.
* _data_ - Contains the PSP data collected and produced during the exercises.

## Getting Started

To begin evaluating these programs you should first install all the python
requirements. The best way to do this is to create a new virtual environment:

```shell
$ virtualenv venv
$ source venv/bin/activate
```

Then install the requirements using the following command:

```shell
$ pip install -r requirements.txt
```

## Running An Exercise Program

To run a program created during an exercise, run the following shell command:

```shell
$ ./run.sh bin/1A.py
```
