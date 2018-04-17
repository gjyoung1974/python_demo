# Instructions for using this App for Demo purposes.


## Used Technologies/Tools:

HTML, CSS, JS, scss, Gulp, NPM, Git, Python

## Docker Workflow

- Install [Docker](https://docker.com)

### Build

```bash
docker build . -t python_demo 
```

This will build the docker file (notice the `dev` tag)

While in the same directory, then:

### Develop

```bash
docker run -it \
   -p 3000:3000 -p 3001:3001 -p 8080:8080 \
   --rm --name python_demo -v $(pwd):/opt/app/src \
   python_demo
```

### CLI Args

```python3

 --init-db    re-initializes the database

  --host      default='0.0.0.0'
  --port',    default=int(os.environ.get('PORT', 8080))
  --debug',   default=False
  --processor-root-uri default=os.environ.get("VGS_PROCESSOR_ROOT_URL")
  --vgs-proxy-uri' configures the VGS proxy uri
```
Env Variables that need to be set

```
VGS_PROCESSOR_ROOT_URL or --processor-root-uri cli arg
HTTP_PROXY, HTTPS_PROXY (env variables) or vgs-proxy-uri cli arg (forward proxy complete address https://user:pass@proxy.com:port)
```

