<?php
file = fopen("a.php","w");
echo fwrite($file,"1");
fclose($file);
?>

