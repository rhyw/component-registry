## Useful makefile targets

### Re-initialize db

```
make stopdb             # Stop orphan corgi-db containers
make rmdb               # run `stopdb` and drop dbdata directory
make corgi-db           # re-initialize db with pre-configured enviroment variables
```

Note: `stopdb` is included in `rmdb` by default. Thus to re-initialize a fresh new database,
run `make rmdb` and `make corgi-db` target is all you need.

### Start the web interface

```
make hub
```

This starts the `runserver` command, and the corgi web interface could be accessed via http://localhost:9000/

### TODOs

Add other needed services
Run tests automatically without errors
