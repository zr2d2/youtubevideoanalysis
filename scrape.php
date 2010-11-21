<?php

include('simple_html_dom.php');

$file = 'comments1.txt';

$Handle = fopen($file, 'w');





for ( $counter = 1; $counter <= 58; $counter += 1) {

echo $counter;

$url = 
'http://www.youtube.com/comment_servlet?all_comments=1&v=9SnQOdEXbNQ&page=' 
. $counter;

$html = file_get_html($url);





foreach($html->find('div.content') as $e) {







foreach($e->find('a.author') as $td) {







$data = $data . htmlspecialchars($td->plaintext) . ' ';





}



foreach($e->find('span.time') as $time) {







$data = $data . htmlspecialchars($time->plaintext) . ' ';





}



foreach($e->find('div.comment-text') as $comment) {



$comment = strip_tags($comment->plaintext);

$comment = str_replace("»¿", "", $comment);

$comment = str_replace("ï", "", $comment);

$comment = str_replace("<br>", "", $comment);

$comment = str_replace("<wbr>", "", $comment);





$data = $data . $comment;

 



}



}



fwrite($Handle, $data); 



}



 fclose($Handle); 



?>
