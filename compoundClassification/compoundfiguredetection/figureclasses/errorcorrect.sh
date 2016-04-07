for f in noncompoundimages/pngs/*.png
 do
  echo $f 
  display $f & 
  read response
  if [ $response == '1' ]
  then 
   echo 'wrong'
   mv $f noncompoundimages/pngs/wrong/; 
   y=`basename $f`
   json='noncompoundimages/jsons/'${y:0:-4}.json
   mv $json noncompoundimages/jsons/wrong/
  fi
  killall display
 done
