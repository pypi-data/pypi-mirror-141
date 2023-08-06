# How to use this tool
This is a start of a Prisma Cloud CLI. It contains a script called pc which can be used to trigger API calls.

Make sure this folder is in your path and create the authentication file below.

## Support

These scripts have been developed by Prisma Cloud SAs, they are not Supported by Palo Alto Networks.
Nevertheless, the maintainers will make a best-effort to address issues, and (of course) contributors are encouraged to submit issues and pull requests.

## Authentication

Create an access key from Settings then Access key  
Get the path to console from Compute tab, System, Utilities  

Create a file into home directory .prismacloud/credentials.json with the following structure  

```json
{
  "api_endpoint": "__REDACTED__",
  "pcc_api_endpoint": "__REDACTED__",
  "access_key_id": "__REDACTED__",
  "secret_key": "__REDACTED__"
}
```

## Run the script

```console
pc
```

## Examples
```
pc policies -o csv
pc policies -o json | jq
pc tags
pc stats -t dashboard
pc stats -t dashboard -o json
pc users
pc cloud
pc reports -o json | jq
pc stats -t dashboard  --columns defendersSummary.host --config local 
```

## Global options
The following global options are available

```
--debug, -d, Show debug output
--columns, Select columns to show
--config, Read custom config file ~/.prismacloud/[value].json
--limit, -l, Number of rows to show
--output, -o, Output mode (json/csv/html/markdown/columns)
```

Use -o columns to get a list of columns available for --columns, e.g.:

```
pc images -o columns
pc images -l 1 --columns hostname repoTag.repo osDistro -o csv 
```

## Use cases
Show twistcli latest scans of scanned images and their number of critical CVEs:

```
pc scans --columns time entityInfo.id entityInfo.repoTag.registry entityInfo.repoTag.repo entityInfo.repoTag.tag entityInfo.vulnerabilityDistribution.high entityInfo.vulnerabilityDistribution.critical 
```

Get latest scan from image id
```
pc scans --columns entityInfo.id entityInfo.repoTag.registry entityInfo.repoTag.repo entityInfo.repoTag.tag entityInfo.vulnerabilityDistribution.critical time  --config local  --custom 'imageID=sha256:ef20bafd68d5e55da305c2289a58f367cd90f71ea97b5414a73b0be745f6aab9'
```


