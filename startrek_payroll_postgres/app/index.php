<?php
require_once("./utils.php");

$host = "startrek_payroll_postgres";
$db_name = $_SERVER["POSTGRES_DB"];
$db_username = $_SERVER["POSTGRES_USER"];
$db_password = $_SERVER["POSTGRES_PASSWORD"];
$conn = pg_connect("host=$host dbname=$db_name user=$db_username password=$db_password");
if (!$conn) {
    printHeader(500);
    echo '
    <section id="preview">
    <h2>Error connecting to the database</h2>
    <p> Please, check the docker environment  </p>
    </section>';
    printFooter();
    die("Connection failed: " . pg_last_error($conn));
}

$sql = "select id,title,description,content from posts LIMIT 48";
$res = pg_query($conn, $sql);
if (!$res) {
    printHeader(500);
    printGenericError("(1 qfail) Access denied for user ".$_POST['user']);
    echo pg_last_error($conn);
    printFooter();
    die();
}

if (pg_num_rows($res) === 0) {
    printHeader(200);
    printGenericError("No blog entries found!");
    echo pg_last_error($conn);
    printFooter();
    die();
} else {
    printHeader(200);
    echo '<div class="grid"><section>';
    $counter = 0;
    while ($data = pg_fetch_assoc($res)) {
        if ($counter < 30) {
            echo '
            <hgroup>
            <h2>'.$data['title'].'</h2>
            <h3>'.$data['description'].'</h3>
            </hgroup>
            <figure>
            <img src="'.getRandomPhoto().'" alt="Architecture">
            <figcaption>Image from <a href="https://unsplash.com/" target="_blank">unsplash.com</a></figcaption>
            </figure>
            <a role="button" class="outline" href="/details.php?id='.$data['id'].'"> Read more </a>
            ';
        }
        if ($counter == 30) {
            echo '</section><aside>';
        }
        if ($counter >= 30) {
            echo '
            <a href="/details.php?id='.$data['id'].'" aria-label="Example"><img src="'.getRandomPhoto().'" alt="'.$data['title'].'"></a>
            <p>
            <a href="#" onclick="event.preventDefault()">'.$data['title'].'</a><br>
            <small>'.$data['description'].'</small>
            </p>
            ';
        }
        $counter++;
    }
    echo '  </aside></div>';
}
printFooter();
?>
