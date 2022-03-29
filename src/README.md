## Ejecución de selenium

Para que no haya problemas con las versiones de los navegadores instalados se utiliza selenium en Docker, de ese modo es independiente, y además, funciona tanto en windows y Linux con la misma instalación.

Para arrancar selenium en docker:

```
docker run --name chrome -d -p 4444:4444 --shm-size="2g" selenium/standalone-chrome:latest
```

Con selenium en remoto, la definición el driver se define

```python
driver = Remote( command_executor=’http://localhost:4444/wd/hub’, options=options )
```
