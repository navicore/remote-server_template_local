Set up remote editing:
```
mkdir ~/remote-server                                                                                                                         <<<
sshfs ubuntu@34.220.227.12:infer ~/remote-server

```

Check drivers:
```
nvidia-smi
```

ssh to remote server and install transformers
```
pip install git+https://github.com/huggingface/transformers torch gunicorn flask

```

Tear down remote editing:
```
umount ~/remote-server                                                                                                                         <<<
```

MAKING A SERVER:

Test:

```
gunicorn -w 1 -b 0.0.0.0:8080 infer_server:app
```

install the `infer.service` file at `/etc/systemd/system/infer.service`
