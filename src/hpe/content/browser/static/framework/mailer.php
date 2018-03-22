<?php
	$msg_box = '';
	$block_i = '';
	
	if($_POST['name'] == "") { $errors[] = "The field 'NAME' is not filled.<br>"; }
	if($_POST['subject'] == "") { $errors[] = "The field 'SUBJECT' is not filled.<br>"; }
    if($_POST['email'] == "") { $errors[] = "The field 'EMAIL' is not filled.<br>"; }
	if($_POST['message'] == "") { $errors[] = "The field 'MESSAJE' is not filled."; }
 	
	if(empty($errors)){
		$block_i = 1;
		$msg_box .= 'Your mail is send!';
	}else{
		$block_i = 2;
        foreach($errors as $one_error){
			$msg_box .= $one_error;
        }
	}
    
    echo json_encode(array(
		'msg' => $msg_box,
		'block' => $block_i
    ));
	
	
	define("WEBMASTER_EMAIL", "orangeidea@gravity-ecommerce.site");
	$body = str_replace('\n',"","<p><b>Name:</b> ".$_POST['name']."<br><b>Email:</b>".$_POST['email']."<br><b>Message:</b>".$_POST['opis']."</p>");
	$email = 'orangeidea@mail.ru';
	$subj = $_POST['subject'];

	$headers = array();
	$headers[]  = 'MIME-Version: 1.0';
	$headers[] = 'Content-type: text/html; charset=utf-8';
	
	$headers[] = 'To: '.$email.'';
	$headers[] = 'From: <'.WEBMASTER_EMAIL.'>';
	$headers[] = 'Reply-To: '.$_POST['email'];
	$headers[] = 'X-Mailer: PHP/' . phpversion();
	mail($email, $subj, $body, implode("\r\n", $headers),'orangeidea@mail.ru');
?>