#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import print_function
import sys, os
import argparse
import pickle

Verbose = False

def debug(s):
    """docstring for debug"""
    if Verbose:
        sys.stderr.write(str(s) + '\n')

class Sprint():
    """docstring for Sprint"""
    def __init__(self, stack, marks):
        debug('env stack:%s mark:%s' %(stack, marks))
        self.marks_file = None
        self.stack_file = None
        if os.path.exists(stack):
            self.stack_file = open(stack, 'r+')
            self.stack_file.seek(0)
            self.stack = [ i.strip() for i in self.stack_file if len(i.strip()) ]
            if not self.stack:
                self.stack = []
        else:
            self.stack_file = open(stack, 'w+')
            self.stack = []

        if os.path.exists(marks):
            self.marks_file = open(marks, 'r+')
            self.marks = {}
            for l in self.marks_file:
                ll = l.strip().split()
                self.marks[ll[0]] = ll[1]

    def __del__(self):
        if self.marks_file:
            self.marks_file.close()

        if self.stack_file:
            self.stack_file.close()

    def List(self):
        """docstring for Li"""
        if not len(self.marks):
            print('no mark')
            return 0
        for key in self.marks.keys():
            print('%s\t%s' %(key, self.marks[key]))
        return 0

    def Mark(self, arg):
        """docstring for Ma"""
        if arg:
            arg = arg[0].strip()
        else:
            arg = os.path.basename(os.getcwd())
        self.marks[arg] = os.getcwd()
        debug(self.marks)
        self.SaveMarks()
        self.List()
        return 0

    def SaveMarks(self):
        self.marks_file.seek(0)
        #clear content
        self.marks_file.truncate()
        for k in self.marks.keys():
            self.marks_file.write('%s %s\n' %(k, self.marks[k]))
        self.marks_file.flush()

    def DeleteMark(self, arg):
        if not arg:
            print('no input mark')
            return 0
        arg = arg[0]
        if self.marks.has_key(arg):
            print('%s deleted' %(arg))
            self.marks.pop(arg)
        else:
            print('no such mark %s' %mark)
        self.List()
        self.SaveMarks()
        return 0

    def Go(self, mark):
        if self.marks.has_key(mark):
            print(self.marks[mark])
            self.SaveStack(self.marks[mark])
            return 1
        else:
            print('no such mark %s' %mark)
            return 0

    def SaveStack(self, dir = None):
        if dir and dir in self.stack:
            self.stack.remove(dir)
        if dir:
            self.stack.insert(0, dir)
        self.stack_file.seek(0)
        self.stack_file.truncate()
        for d in self.stack:
            self.stack_file.write('%s\n' %(d))
        self.stack_file.flush()

    def Sprint(self):
        if not len(self.stack):
            print('no history')
            return
        index = 1
        for d in self.stack:
            sys.stderr.write('%d %s\n' %(index, d))
            index += 1
        index = raw_input()
        try:
            index = int(index) - 1
        except:
            print('wrong input')
            return 0

        if index >= 0 and index < len(self.stack):
            print(self.stack[index])
            self.SaveStack(self.stack[index])
            return 1
        else:
            print('wrong input')
            return 0

    def SprintDir(self, dir):
        print(dir)
        if os.path.exists(dir):
            dir = os.path.expanduser(dir)
            dir = os.path.realpath(dir)
            self.SaveStack(dir)
        return 1


if __name__ == '__main__':
    parser =argparse.ArgumentParser(description = "Description: sprint to a directory")
    parser.add_argument("dir", nargs = '?')
    parser.add_argument("-l", dest = "ListMark", action = "store_true", help = "list marks")
    parser.add_argument("-s", dest = "Sprint", action = "store_true", help = "list least 20 dir you go")
    parser.add_argument("-m", dest = "Mark", action = "store", nargs = '*',
            help = "mark current dir. name is optional, default is the basename, old mark will be replaced")
    parser.add_argument("-g", dest = "Go", action = "store" ,help = "sprint to the mark")
    parser.add_argument("-d", dest = "DeleteMark", action = "store", nargs = '*', 
            help = "delete a mark")
    parser.add_argument("-v", dest = "Verbose", action = "store_true", help = "Verbose")
    args = parser.parse_args()
    if args.Verbose:
        Verbose = True
    debug(args)
    sprint = Sprint(os.environ.get('_STACK_'), os.environ.get('_MARKS_'))
    if args.dir:
        exit(sprint.SprintDir(args.dir))
    elif 1 == len(sys.argv):
        exit(sprint.SprintDir(os.environ.get('HOME')))
    if args.ListMark:
        exit(sprint.List())
    elif args.Sprint:
        exit(sprint.Sprint())
    elif None != args.Mark:
        exit(sprint.Mark(args.Mark))
    elif args.Go:
        exit(sprint.Go(args.Go))
    elif None != args.DeleteMark:
        exit(sprint.DeleteMark(args.DeleteMark))
    else:
        print(sys.argv[1:])
    exit(1)
