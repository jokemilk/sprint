#!/usr/bin/env sh

if [ `whoami` != "root" ];then
	echo "非root用户！"
	exit 1
fi

cp sprint.* /usr/bin/
echo "add source sprint.env to your shell env please"
