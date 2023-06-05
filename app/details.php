<?php
require_once("./utils.php");

  /*
  *
  *  I've rebuilt this a bit to make it a bit more challenging and
  *  a tad more pretty. Nobody should code like this though.
  *  It's been a long time since I wrote raw mysqli commands...
  */
  $host = "startrek_payroll_mysql";
  $db_name = $_SERVER["MYSQL_DATABASE"];
  $db_username = $_SERVER["MYSQL_USER"];
  $db_password = $_SERVER["MYSQL_PASSWORD"];

  $conn = new mysqli($host, $db_username, $db_password, $db_name);
  if ($conn->connect_error) {
    printHeader(500);
    echo '
    <section id="preview">
    <h2>Error connecting to the database</h2>
    <p> Please, check the docker environment  </p>
    </section>';
    printFooter();
    die("Connection failed: " . $conn->connect_error);
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
  // We need to be sloppy here :P
  $sql = "select id,title,description,content,author_id from posts WHERE id = ".$id;
  $res = $conn->query($sql); // So I inadvertedly patched one of the holes...
  if (!$res) {
    printHeader(500);
    printGenericError("Failed to find that entry");
    echo $conn->error;
    die();        
  } 
  if (!$res->num_rows) {
    printHeader(200);
    printGenericError("Entry not found!");
    echo $conn->error;
    printFooter();
    die();   
  } else {
    printHeader(200);
    echo '
      <div class="grid">
        <section>';
    while ($data = $res->fetch_assoc()) {
      if (isset($_GET['author_id']))
        $author_id = $_GET['author_id'];
      else
        $author_id = $data['author_id'];
        $author_qry = "select * from authors where id = '".$author_id."'";
        $resp = $conn->multi_query($author_qry);
        $author = array(
          'first_name' => "no",
          'last_name' => "no",
          'email' => "no",
        );
        if ($result = $conn->store_result()) {
          $author = $result->fetch_assoc();
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

  ?>

