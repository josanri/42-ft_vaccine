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

if (!isset($_GET['id'])) {
    printHeader(404);
    echo '
    <section id="preview">
    <h2>Article not found</h2>
    <p> Please, go back to the home page </p>
    </section>';
    printFooter();
    die();
}

$id = $_GET['id'];
$sql = "select title,description,content,author_id from posts WHERE id = $id";
$res = pg_query($conn, $sql);
if (!$res) {
    printHeader(500);
    printGenericError("Failed to find that entry");
    echo pg_last_error($conn);
    die();
}

if (pg_num_rows($res) === 0) {
    printHeader(200);
    printGenericError("Entry not found!");
    echo pg_last_error($conn);
    printFooter();
    die();
} else {
    printHeader(200);
    echo '
    <div class="grid">
      <section>';
    while ($data = pg_fetch_assoc($res)) {
        if (isset($_GET['author_id'])) {
            $author_id = $_GET['author_id'];
        } else {
            $author_id = $data['author_id'];
        }
        $author_qry = "select * from authors where id = '$author_id'";
        $resp = pg_query($conn, $author_qry);
        $author = array(
            'first_name' => "no",
            'last_name' => "no",
            'email' => "no",
        );
        if ($result = pg_fetch_assoc($resp)) {
            $author = $result;
        }

        echo '
        <hgroup>
          <h2>'.$data['title'].'</h2>
          <h3>'.$data['description'].'</h3>
        </hgroup>
        <figure>
          <img src="'.getRandomPhoto().'" alt="Architecture">
          <figcaption>Image from <a href="https://unsplash.com/" target="_blank">unsplash.com</a></figcaption>
        </figure>
        <p>'.$data['content'].'</p>
        <small> Author: '.$author['first_name'].' '.$author['last_name'].' ('.$author['email'].') </small>
        </section>';
    }
    echo '
    </div>
    ';
}
printFooter();
