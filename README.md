#Instructions for using this App for Demo purposes.

##Prerequisites
- Command Line Access (terminal)
- SublimeText, Atom or another text editor that can help you show the code quickly.
- Browser


###Open terminal

1. Clone this repo locally:

```
$ git clone <repo>

```

###Open another terminal tab
2. Download ngrok (we'll need to adjust the rules once you have ngrok running because it generates a new web address every time)

https://ngrok.com/download

In the directory you downloaded ngrok type:

```
$ ./ngrok start 5000

```

###Back in repo tab

3. Navigate to cloned repo directory and enter the following command.

```
$ make penv

```

```
$ make run
```

*Server is now started*

If you look at your ngrok tab that web-address will be how to access your locally running code online.

4. Open atom in the cloned directory or sublime (atom . or sublime .)



5. Two zones are in play
- reverse_proxy is using our form rule to redact a simple html form that goes through the proxy with our ngrok address/server as our upstream.
- forward_proxy takes the data received on the server and sends it to test endpoint to show how reveal rules (This way we used JSON to post)
