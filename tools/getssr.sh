self=${0}
cd $(dirname ${self})

git pull origin gh-pages

rstfile='rst.md'
groupfile='groupSsr.md'

rm -f ${rstfile}
rm -f ${groupfile}

#encodedUrls=($(curl https://doub.io/sszhfx/ | grep 'https://doub.pw/qr/qr.php?text=ss' | cut -d' ' -f3| sed  -e 's/href="//g'| cut -d'"' -f 1))

encodedUrls=($(curl https://doub.io/sszhfx/ | grep 'https://doub.pw/qr/qr.php?text=ss'| awk '{print $3" "$7}'| sed  -e 's/href="//g'| awk -F '"' '{print $1" "$2}'))

for encodedUrl in $(echo ${encodedUrls[@]})
do
    [[ $(echo ${encodedUrl}| grep 'text=ssr:' | wc -l) -gt 0 ]] && {
        curl ${encodedUrl} | grep 'qrcode("ssr://' | cut -d'"' -f2 >> ${rstfile}
    }
    [[ $(echo ${encodedUrl}| grep 'text=ss:' | wc -l) -gt 0 ]] && {
        curl ${encodedUrl} | grep 'qrcode("ss://' | cut -d'"' -f2 >> ${rstfile}
    }
done

[[ $(git diff ${rstfile}| wc -l) -gt 0 ]] && {
    python groupSsr.py

    git add ${rstfile} ${groupfile}
    git commit -m "update ssr - $(date)"
    git push 
}



