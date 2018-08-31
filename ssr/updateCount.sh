#! /bin/bash

unset http_proxy
unset https_proxy

url='https://raw.githubusercontent.com/rhymeyang/source/gh-pages/tools/rst.md'

srcFile=rst.md
decodeFile='./decode.md'

[[ -e ${srcFile} ]] && rm -f ${srcFile}

wget --no-check-certificate -O ./rst.md ${url}

echo ''> ${decodeFile}

ssr_org_list=($(cat ${srcFile} | grep '^ssr://' | cut -d'/' -f 3))

echo "ssr:"| tee -a ${decodeFile}

for ssr in ${ssr_org_list[@]}
do
    echo ${ssr}
    echo 
    echo ${ssr} | base64 -d | cut -d'/' -f1 | tee -a ${decodeFile}

done

ss_org_list=($(cat ${srcFile} | grep '^ss://' | cut -d'/' -f 3))


echo "ss:" | tee -a ${decodeFile}


for ss in ${ss_org_list[@]}
do
    echo ${ss}
    echo '' | tee -a ${decodeFile}

    echo ${ss} | base64 -d  | tee -a  ${decodeFile}
done

echo '' | tee -a ${decodeFile}
