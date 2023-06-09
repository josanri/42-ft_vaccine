<?php
require_once("./utils.php");

  /*
  *
  *  I've rebuilt this a bit to make it a bit more challenging and
  *  a tad more pretty. Nobody should code like this though.
  *  It's been a long time since I wrote raw mysqli commands...
  */
  $host = "startrek_payroll_postgres"; // Cambia el nombre del host de MySQL a PostgreSQL
  $db_name = $_SERVER["POSTGRES_DB"]; // Utiliza la variable correcta para el nombre de la base de datos de PostgreSQL
  $db_username = $_SERVER["POSTGRES_USER"]; // Utiliza la variable correcta para el nombre de usuario de PostgreSQL
  $db_password = $_SERVER["POSTGRES_PASSWORD"]; // Utiliza la variable correcta para la contraseña de PostgreSQL
  $conn = pg_connect("host=$host dbname=$db_name user=$db_username password=$db_password");
  if (!$conn) {
    printHeader(500);
    echo '
    <section id="preview">
    <h2>Error connecting to the database</h2>
    <p> Please, check the docker environment  </p>
    </section>';
    die("Connection failed: " . pg_last_error($conn));
}

function printLoginError($string) {
  echo '
  <section id="preview">
  <h2>Authentication failed</h2>
  <p> '.$string.' </p>
  </section>';
}

if (!isset($_POST['s'])) {
  printHeader(200);
echo '
    <!-- Preview -->
      <section id="preview">
        <h2>Login</h2>
        <p> Please, enter your username and password to access the payroll  </p>
          <div class="grid">
          <form action="" method="post">
            <input
              type="text"
              name="user"
              placeholder="Username"
              aria-label="User name"
              required
            />
            <input
              type="password"
              name="password"
              aria-label="Password"
              required
            />
            <input type="submit" value="Login" name="s">
          </div>
        </form>
      </section>
      <!-- ./ Preview -->
    ';
}

if ($_POST) {
    $user = $_POST['user'];
    error_log("USERNAME:" . $user);
    $pass = $_POST['password'];
    error_log("PASSWORD:" . $pass);
    $sql = "select first_name, last_name, username, salary from users where username = '$user' and password = '$pass'";
    error_log("QUERY:" . $sql);
    $res = pg_query($conn, $sql);
    if (!$res) {
        printHeader(500);
        printLoginError("(1 qfail) Access denied for user ".$_POST['user']);
        echo pg_last_error($conn);
        die();
    }

    if (pg_num_rows($res) === 0) {
        printHeader(401);
        printLoginError("(2) Access denied for user ".$_POST['user']);
        echo pg_last_error($conn);
        die();
    } else {
        printHeader(200);
        echo '
        <section id="preview">
        <h2> Hello '.$user.' </h2>
        <p>
          Here\'s your payroll info
        </p>
        <section id="tables">
          <figure>
            <table role="grid">
              <thead>
                <th> User </th>
                <th> Salary </th>
            </thead>
            <tbody> ';
             while ($data = pg_fetch_assoc($res)) {
                echo "<tr> <td>".$data['first_name']." ".$data['last_name']."</td> <td>".$data['salary']."</td></tr>";
            }
            echo "</tbody> </table>";
            echo '<a role="button" class="primary" href="/"> Logout </a>';
        }
    }
  ?>
