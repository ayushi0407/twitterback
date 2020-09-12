
#!/bin/sh
gunicorn project.wsgi --bind=0.0.0.0:80 --workers=3
