# Introduction

```bash

██╗░░██╗██████╗░  ░██████╗███████╗░█████╗░██╗░░░██╗██████╗░██╗████████╗██╗░░░██╗
██║░░██║╚════██╗  ██╔════╝██╔════╝██╔══██╗██║░░░██║██╔══██╗██║╚══██╔══╝╚██╗░██╔╝
███████║░░███╔═╝  ╚█████╗░█████╗░░██║░░╚═╝██║░░░██║██████╔╝██║░░░██║░░░░╚████╔╝░
██╔══██║██╔══╝░░  ░╚═══██╗██╔══╝░░██║░░██╗██║░░░██║██╔══██╗██║░░░██║░░░░░╚██╔╝░░
██║░░██║███████╗  ██████╔╝███████╗╚█████╔╝╚██████╔╝██║░░██║██║░░░██║░░░░░░██║░░░
╚═╝░░╚═╝╚══════╝  ╚═════╝░╚══════╝░╚════╝░░╚═════╝░╚═╝░░╚═╝╚═╝░░░╚═╝░░░░░░╚═╝░░░
```

H2-depscan is a completely open-source tool for auditing project dependencies against known vulnerabilities, advisories, and licensing restrictions. As an input, both local repositories and container images are supported. The tool is suited for continuous integration setups, as it has built-in build breaker logic.

### Vulnerability Data sources

- OSV
- NVD
- GitHub
- NPM

## Usage

h2-depscan is an excellent tool for continuous integration (CI) and local development. 


### Full list of options:

```bash
usage: H2-depscan [-h] [--no-banner] [--cache] [--sync] [--suggest] [--risk-audit] [--private-ns PRIVATE_NS] [-t PROJECT_TYPE] [--bom BOM] -i SRC_DIR [-o REPORT_FILE]
              [--no-error]
  -h, --help            show this help message and exit
  --no-banner           Do not display banner
  --cache               Cache vulnerability information in platform specific user_data_dir
  --sync                Sync to receive the latest vulnerability data. Should have invoked cache first.
  --suggest             Suggest appropriate fix version for each identified vulnerability.
  --risk-audit          Perform package risk audit (slow operation). Npm only.
  --private-ns PRIVATE_NS
                        Private namespace to use while performing oss risk audit. Private packages should not be available in public registries by default. Comma
                        separated values accepted.
  -t PROJECT_TYPE, --type PROJECT_TYPE
                        Override project type if auto-detection is incorrect
  --bom BOM             Examine using the given Software Bill-of-Materials (SBoM) file in CycloneDX format. Use cdxgen command to produce one.
  -i SRC_DIR, --src SRC_DIR
                        Source directory
  -o REPORT_FILE, --report_file REPORT_FILE
                        Report filename with directory
  --no-error            Continue on error to prevent build from breaking
```

### Scanning containers locally (Python version)

Scan `latest` tag of the container `h2security/h2-sastscan-slim`

```bash
h2-depscan --no-error --cache --src h2security/h2-sastscan-slim -o containertests/depscan-scan.json -t docker
```

Include `license` to the type to perform license audit.

```bash
h2-depscan --no-error --cache --src h2security/h2-sastscan-slim -o containertests/depscan-scan.json -t docker,license
```

You can also specify the image using the sha256 digest

```bash
h2-depscan --no-error --src debian@sha256:1cfbc587ea5598545ac045ee776965a005b1f0c26d5daf5479b859b092697439 -o containertests/depscan-redmine.json -t docker
```

You can also save container images using docker or podman save command and pass the archive to depscan for scanning.

```bash
docker save -o /tmp/scanslim.tar h2security/h2-sastscan-slim:latest
# podman save --format oci-archive -o /tmp/scanslim.tar h2security/h2-sastscan-slim:latest
depscan --no-error --src /tmp/scanslim.tar -o reports/depscan-scan.json -t docker
```

To scan with default settings

```bash
docker run --rm -v $PWD:/app h2security/h2-depscan scan --src /app --report_file /app/reports/depscan.json
```

To scan with custom environment variables based configuration

```bash
docker run --rm \
    -e VDB_HOME=/db \
    -e NVD_START_YEAR=2010 \
    -e GITHUB_PAGE_COUNT=5 \
    -e GITHUB_TOKEN=<token> \
    -v /tmp:/db \
    -v $PWD:/app h2security/h2-depscan scan --src /app --report_file /app/reports/depscan.json
```

In the above example, `/tmp` is mounted as `/db` into the container. This directory is then specified as `VDB_HOME` for caching the vulnerability information. This way the database can be cached and reused to improve performance.

## Supported languages and package format

dep-scan uses cdxgen command internally to create Software Bill-of-Materials (SBoM) file for the project. This is then used for performing the scans.

The following projects and package-dependency format is supported by cdxgen.

| Language           | Package format                                                               |
| ------------------ | ---------------------------------------------------------------------------- |
| node.js            | package-lock.json, pnpm-lock.yaml, yarn.lock, rush.js                        |
| java               | maven (pom.xml [1]), gradle (build.gradle, .kts), scala (sbt)                |
| php                | composer.lock                                                                |
| python             | setup.py, requirements.txt [2], Pipfile.lock, poetry.lock, bdist_wheel, .whl |
| go                 | binary, go.mod, go.sum, Gopkg.lock                                           |
| ruby               | Gemfile.lock, gemspec                                                        |
| rust               | Cargo.toml, Cargo.lock                                                       |
| .Net               | .csproj, packages.config, project.assets.json, packages.lock.json            |
| docker / oci image | All supported languages excluding OS packages                                |
