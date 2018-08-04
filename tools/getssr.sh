self=${0}
cd $(dirname ${self})

function fun_version_1(){
    #encodedUrls=($(curl https://doub.io/sszhfx/ | grep 'https://doub.pw/qr/qr.php?text=ss' | cut -d' ' -f3| sed  -e 's/href="//g'| cut -d'"' -f 1))
    encodedUrls=($(cat ${indexFile} | grep 'https://doub.pw/qr/qr.php?text=ss'| awk '{print $3" "$7}'| sed  -e 's/href="//g'| awk -F '"' '{print $1" "$2}'))

    for encodedUrl in $(echo ${encodedUrls[@]})
    do
        [[ $(echo ${encodedUrl}| grep 'text=ssr:' | wc -l) -gt 0 ]] && {
            curl ${encodedUrl} | grep 'qrcode("ssr://' | cut -d'"' -f2 >> ${rstfile}
        }
        [[ $(echo ${encodedUrl}| grep 'text=ss:' | wc -l) -gt 0 ]] && {
            curl ${encodedUrl} | grep 'qrcode("ss://' | cut -d'"' -f2 >> ${rstfile}
        }
    done

}

function fun_version_2(){
    savedIndex=(4 5 28 29 52 53 54  74 75 76  97 98 99 120 121 122 143 144 145)
    encodedUrls=($(cat ${backssr} | grep -E '<td>'))

    for index in $(echo ${savedIndex[@]})
    do
        echo ${encodedUrls[index]} >> ${rstfile}
        echo " " >> ${rstfile}
        
    done
    echo " " >> ${rstfile}
}
rstfile='rst.md'
indexFile='/tmp/ssr/ssr.html'
groupfile='groupSsr.md'
tmpDir=/tmp/ssr


[[ -e ${tmpDir} ]] || mkdir -p ${tmpDir}

backssr=${tmpDir}/ssr_$(date +%F_%H-%M-%S).html

# backssr=${tmpDir}/ssr_2018-08-04_15-00-28.html

curl https://doub.io/sszhfx/ >${backssr}
ln -sf ${backssr} ${indexFile}
git reset --hard
git pull origin gh-pages

> ${rstfile}


fun_version_2
fun_version_1


[[ $(git diff ${rstfile}| wc -l) -gt 0 ]] && {
#    python groupSsr.py

#    git add ${rstfile} ${groupfile}
    git add ${rstfile}
    git commit -m "update ssr - $(date)"
    git push 
}








