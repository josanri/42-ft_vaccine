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
  die("Connection failed: " . $conn->connect_error);
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
    $res = $conn->query($sql); // So I inadvertedly patched one of the holes...
    if (!$res) {
        printHeader(500);
        printLoginError("(1 qfail) Access denied for user ".$_POST['user']);
        echo $conn->error;
        die();        
    } 
    
    if (!$res->num_rows) {
        printHeader(401);
        printLoginError("(2) Access denied for user ".$_POST['user']);
        echo $conn->error;
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
             while ($data = $res->fetch_assoc()) {
                echo "<tr> <td>".$data['first_name']." ".$data['last_name']."</td> <td>".$data['salary']."</td></tr>";
        }
        echo "</tbody> </table>";
        echo '<a role="button" class="primary" href="/"> Logout </a>';
    }

}
?>
</main>
</body> 
</html>
