<h2>Challenge description:</h2>

```
Someone is trying to hack my server, the username and password for it is ctfuser. They stole my important text file, please get it back for me.
ssh ctfuser@challenges.ctf.sikt.no -p 2200 
```

<h2>Solve:</h2>

I don't know if my solve is the intended solve.

I start by looking in the history for any refrences to a flag.
To my luck some cat commands refrencing flag.txt have been run before.

```
ctfuser@a1838532013d:~$ history | grep flag
  462  cat /tmp/linpeas/flag.txt 
  631  cat /tmp/linpeas/flag.txt 
  633  cat /tmp/linpeas/flag.txt 
  663  history | grep flag
ctfuser@a1838532013d:~$ cat /tmp/linpeas/flag.txt 
SiktCTF{WHo_is_TH3_Re4L_HaCk3R?}ctfuser@a1838532013d:~$ 
``` 


<h2>Flag:</h2>

```
SiktCTF{WHo_is_TH3_Re4L_HaCk3R?}
```