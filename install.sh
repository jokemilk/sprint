#!/usr/bin/env sh

if [ $(whoami) != "root" ]; then
	echo "非root用户！"
	exit 1
fi

if [ "$(uname)" = "Darwin" ]; then
	ln -s $PWD/sprint.* /usr/local/bin/
else
	ln -s $PWD/sprint.* /usr/bin/
fi

echo "add source sprint.env to your shell env please"
