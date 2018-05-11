<html>
<head>
<title>Hotspot Status</title>
<meta http-equiv="refresh" content="10">
</head>
<body>
<?php
echo "<p>\n";
@readfile('/tmp/hblink.MASTER-1.stat');
echo "</p>\n";
?>
</body>
</html>
