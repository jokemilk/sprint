#!/usr/bin/env sh

_STACK_=`echo ~/.sprint.stack`
_MARKS_=`echo ~/.sprint.marks`

help()
{
	echo " 
sprint: sprint to a directory
usage: sprint [-h] [-l] [-s] [-m <name>] [-g Mark] [-d Mark] <dir>
	-h:help
	-l:	list marks
	-s:	list least 20 dir you go
	-m:	mark current dir. name is optional, default is the basename, old mark will be replaced.
	-g: sprint to the mark
	-d: delete a mark
	dir:	dir you want to go, the same as cd
	
"
}

contains()
{
	for i in `echo $1 | tr ' ' '\n'`;do
		if [ "$i" = "$2" ]; then
			return 0
		fi
	done
	return 1
}

list="-h -l -s -m -g"

[ ! -f ${_STACK_} ] && touch ${_STACK_}
[ ! -f ${_MARKS_} ] && touch ${_MARKS_}

sed --h 2>&1 | grep gnu -q

if [ $? = 0 ];then
	gnu_sed=1
else
	gnu_sed=0
fi

#help
if [ "$1" = "-h" ]; then
	help
	exit 0
fi
#list marks
if [ "$1" = "-l" ]; then
	if [ -s ${_MARKS_} ]; then
		cat ${_MARKS_}
	else
		echo "no marks"
	fi
	exit 0
fi
#list history stack
if [ "$1" = "-s" ]; then
	if [ -s ${_STACK_} ]; then
		tail -n20 ${_STACK_}
	else
		echo "no history"
	fi
	exit 0
fi
#mark a dir
if [ "$1" = "-m" ]; then
	current_dir=`pwd`
	[ -n "$2" ] && mark=$2 || mark=`basename ${current_dir}`
	if [ $gnu_sed = 1 ]; then
		sed -i "/^\ ${mark}\ /d" ${_MARKS_}
	else
		sed -i '' "/^\ ${mark}\ /d" ${_MARKS_}
	fi
	echo " ${mark} ${current_dir}" >> ${_MARKS_}
	echo " ${mark} ${current_dir}"
	exit 0
fi
#sprint to a dir
if [ "$1" = "-g" ]; then
	path=$(awk "/\ $2\ /  { print \$2 }" ${_MARKS_})
	if [ -n "$path" ];then
		echo ${path}
		exit 1
	else
		echo "no such mark $2"
		exit 0
	fi
fi
#delete a mark
if [ "$1" = "-d" ]; then
	#wrong input
	[ -z "$2" ] && help && exit 0	
	if [ $gnu_sed = 1 ]; then
		sed -i "/^\ $2\ /d" ${_MARKS_}
	else
		sed -i '' "/^\ $2\ /d" ${_MARKS_}
	fi
	cat ${_MARKS_}
	exit 0
fi
#do nothing, return the input
echo $@
exit 1
