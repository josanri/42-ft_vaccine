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

  $sql = "select id,title,description,content from posts LIMIT 48";
  $res = $conn->query($sql); // So I inadvertedly patched one of the holes...
  if (!$res) {
    printHeader(500);
    printGenericError("(1 qfail) Access denied for user ".$_POST['user']);
    echo $conn->error;
    printFooter();
    die();        
  } 
  if (!$res->num_rows) {
    printHeader(200);
    printGenericError("No blog entries found!");
    echo $conn->error;
    printFooter();
    die();   
  } else {
    printHeader(200);
    echo '<div class="grid"><section>';
    $counter = 0;
    while ($data = $res->fetch_assoc()) {
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
      if ($counter == 30) {echo '</section><aside>';}
      if ($counter >= 30) {
        echo '
        <a href="/details.php?id='.$data['id'].'"" aria-label="Example" ><img src="'.getRandomPhoto().'" alt="'.$data['title'].'"></a>
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
