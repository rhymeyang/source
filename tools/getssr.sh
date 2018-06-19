rstfile='rst.md'

rm -f ${rstfile}
encodedUrls=($(curl https://doub.io/sszhfx/ | grep 'https://doub.pw/qr/qr.php?text=ss' | cut -d' ' -f3| sed  -e 's/href="//g'| cut -d'"' -f 1))

for encodedUrl in $(echo ${encodedUrls[@]})
do
    curl ${encodedUrl} | grep 'qrcode("ssr://' >> ${rstfile}
done
