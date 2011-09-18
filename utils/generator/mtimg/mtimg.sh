#!/bin/bash
SETTINGFILE='./mtfiles'
FILENUM=`wc -l ${SETTINGFILE} | awk '{print $1}'`
FILES=`cat ${SETTINGFILE} | awk '{print $1}'`
CSSCLASSES=`cat ${SETTINGFILE} | awk '{print $2}'`

i=16
for CLASS in ${CSSCLASSES}
do
	echo "${CLASS}{ background-position: -${i}px 0px; }"
	i=`expr $i + 16`
done

montage -background transparent -tile ${FILENUM}x1 -geometry +0+0 ${FILES} ../../../statics/css/image/mtimg.png
