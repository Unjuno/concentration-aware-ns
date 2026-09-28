# Reconstructing the n=128 case archive

The verified gzip tar is 177,259,287 bytes, above GitHub's single-file upload
limit. The published Zstandard package is split into two chunks, each below
that limit. The package metadata records chunk and full-stream SHA-256 hashes.

From this directory:

```sh
shasum -a 256 -c <(jq -r '.parts[] | "\(.sha256)  \(.path)"' n128-dt0.001.tar.zst.parts.json)
cat n128-dt0.001.tar.zst.part-* > n128-dt0.001.tar.zst
shasum -a 256 n128-dt0.001.tar.zst
zstd -d n128-dt0.001.tar.zst -o n128-dt0.001.tar.gz
shasum -a 256 n128-dt0.001.tar.gz
tar -tzf n128-dt0.001.tar.gz >/dev/null
```

The reconstructed gzip tar SHA-256 must equal the value in
`manifest.json` (`595d27fe2e0ca061e727624444406419870bff8d06d11a38f911fdcebd19e0f0`).
The package was generated from the already content-verified archive; its
uncompressed tar members were not modified.
