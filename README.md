# FastRandom

A shell tool to generate random bytes extremely fast. Uses multiple CPU cores and both AES-NI and ChaCha20 to facilitate even higher utilisation of processing capacity. The output may be used for scrubbing disks, even the fastest NVME SSDs, or for any other purpose where large amounts of irreproducible random bytes are needed.

Prefer redirection `>` instead of pipes and `dd` for maximal speed. This works with both files and block devices.

```
pip install fastrandom
fastrandom -p > /tmp/file.dat    # -p for progress indication
[fastrandom]     15,451 MiB generated at 3.48 GB/s
[Errno 28] No space left on device
```

This tool is about 30 % faster than the best contender that I am aware of, `openssl enc -aes-256-ctr -in /dev/zero`, many times faster than any popular random number generator (like [PCG64](https://www.pcg-random.org/index.html)) and about 50 times faster than `/dev/urandom`. Generating to `/dev/null` I can reach 11 GB/s on a six-core CPU but any actual devices that I have access to, including NVME 4.0 SSDs and even ramdisks, are slower. Please drop a Github issue if you find something faster.
