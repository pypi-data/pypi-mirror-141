def config(appname="Kiqpo-app", version="1.0.0", description="This app is build using kiqpo.", url='www.github.com/kiqpo'):
    configYaml = """name: %s
version: %s
description: %s
github: %s

paths:
  kiqpo: /%s/kiqpo.py

dependencies:
  python:
    python: 3.6
    pip: 3.0

  kiqpo:
    kiqpo: 1.0

theme:
  primary: '#0A84FF'
  secondary: '#F2F2F7'
  background: '#ffffff'
  error: '#F44336'
  surface: '#ffffff'
  text-primary: '#000000'
  text-secondary: '#212121'""" % (appname, version, description, url,appname)
    return configYaml
