# bag

```bash
# install
pip install robobag

# install protobuf
brew install protobuf

# generate profile_pb2.py
cd robobag
protoc -I=./ --python_out=./ ./profile.proto

# build package
python3 setup.py sdist

# install from local
pip3 install dist/robobag-0.3.1.tar.gz

# publish to pypi
pip install twine
twine upload dist/*

# use as cli
robobag --help
robobag profile -i /path/to/data.bag
robobag extract -i /path/to/data.bag -p /path/to/data.pb.bin  -t /hdmap -f parquet
robobag extract -i /path/to/data.bag -p /path/to/data.pb.bin  -t /camera_front -f mp4
```

## release

- v0.3.0 add cli
- v0.2.4 init