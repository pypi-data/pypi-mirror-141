# Bottle Elastic APM

Simple plugin to use ELK with APM server for your bottle application

### Using default_app

> `default_app()` uses AppStack, so you only need to install it once.

```python
from bottle import default_app, run
from bottle_elastic_apm import ElasticAPM, make_apm_client

ELK_CONFIG = {
    'service_name': 'my-app',
}

app = default_app()
app2 = default_app()

apm_client = make_apm_client(**ELK_CONFIG) # avoid multi client instances
app.install(ElasticAPM(client=apm_client))

@app.get('/')
def index():
    return 'Hello world!'

@app2.get('/2')
def index2():
    return 'Hello world!'

run(app)
```

### Using Bottle()

> `Bottle()` don't uses AppStack, so you need to install on all of them.

```python
from bottle import Bottle, run
from bottle_elastic_apm import ElasticAPM, make_apm_client

ELK_CONFIG = {
    'service_name': 'my-app',
}

app = Bottle()
app2 = Bottle()
app.mount('v2', app2)

apm_client = make_apm_client(**ELK_CONFIG) # avoid multi client instances
app.install(ElasticAPM(client=apm_client))
app2.install(ElasticAPM(client=apm_client))

@app.get('/')
def index():
    return 'Hello world!'

@app2.get('/2')
def index2():
    return 'Hello world!'

run(app)
```


### Avoid capture specific errors

```python
from bottle import default_app
from bottle_elastic_apm import ElasticAPM, make_apm_client

ELK_CONFIG = {
    'service_name': 'my-app',
}

app = default_app()
apm_client = make_apm_client(**ELK_CONFIG) # avoid multi client instances
app.install(ElasticAPM(client=apm_client, avoided_errors={(401, 'JWT: Signature has expired',)}))
```
