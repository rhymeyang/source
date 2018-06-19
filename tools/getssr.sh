rstfile='rst.md'

rm -f ${rstfile}
encodedUrls=($(curl https://doub.io/sszhfx/ | grep 'https://doub.pw/qr/qr.php?text=ss' | cut -d' ' -f3| sed  -e 's/href="//g'| cut -d'"' -f 1))

for encodedUrl in $(echo ${encodedUrls[@]})
do
    curl ${encodedUrl} | grep 'qrcode("ssr://' | cut -d'"' -f2 >> ${rstfile}
done

[[ $(git diff ${rstfile}| wc -l) -gt 0 ]] && {
    git add ${rstfile}
    git commit -m "update ssr - $(date)"
    git push 
}
