#!/bin/bash
for i in {1..1000}
do
	success=0
	for file in ./*
	do
		res=$(file $file | grep "ASCII")
		echo $res
		if [ "$res" != "" ]
		then
			success=1
			cat $file
			break
		fi
		res=$(echo $file | grep "flag")
		if [ "$res" != "" ]
		then
			7z x $file
			mv $file $i
			break 
		fi
	done
	if [ $success -eq 1 ]
	then
		break
	fi
done
