<?php
if(isset($_FILES['uploaded'])) {
    $target_path  =  "./uploads/";
    $target_path .= basename( $_FILES[ 'uploaded' ][ 'name' ] );
    $temp_name = $_FILES[ 'uploaded' ][ 'tmp_name' ];
    if (!file_exists($target_path)) {
        if( !move_uploaded_file($temp_name , $target_path ) ) {
                // No
                echo "upload image failed";
            }
            else {
                // Yes!
                echo "upload image succeed";
            }
        }
        else{
            echo $temp_name . " 文件已经存在。 ";  
        } 
}
?>
