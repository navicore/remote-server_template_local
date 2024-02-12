Running Mistral 7B on AWS
==============

These are my notes for following the very good tutorial about running Mistral 7b
on an AWS GPU VM. https://www.youtube.com/watch?v=88ByWjM-KGM&t=617s

After getting to the point where the presenter ssh's into the VM, I iterated on
things to make a service start the inference via HTTP REST POST with Flask.

Model https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2

Note, the change below using `torch_dtype=torch.float16` is how the model fits
in the limits of the G5 - float16 instead of float32, so there is compromise.

```
import torch

model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2", torch_dtype=torch.float16)
```



Set up remote editing (I don't use VSCode):
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
python3 -m venv venv
source venv/bin/activate
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

Install the `infer.service` file at `/etc/systemd/system/infer.service`

```
sudo systemctl enable infer.service
sudo systemctl start infer.service
```
