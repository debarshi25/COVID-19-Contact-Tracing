<?php
$json = file_get_contents('php://input');
$json = json_decode($json);
$command = "python3 db-server.py {$json->id} {$json->date}";
$result = shell_exec($command);
echo json_encode($result);
?>