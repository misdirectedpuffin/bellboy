# Bellboy

## Installation

```
docker build -t trivago . \
  && docker run \
    --rm \
    -it \
    -v <path/to/repo/trivago/data>:/opt/app/data \
    trivago \
    /bin/bash
```


## Usage

This cli exposes commands that can be viewed with 

```
$ bellboy --help
Usage: bellboy [OPTIONS] COMMAND [ARGS]...

  Entrypoint to CLI.

Options:
  --help  Show this message and exit.

Commands:
  parse  Parse the csv
```

There is a single subcommand `parse` which exposes options listed below.
```

$ bellboy parse --help
Usage: bellboy parse [OPTIONS]

  Parse the csv

Options:
  -s, --http-status INTEGER       Only return uris with this http status.
  -p, --ping                      Make async http requests for validation.
  -f, --output-format [json|xml]  The desired output format.
  -o, --outfile TEXT              Output file name (without extension).
  -i, --infile PATH               The input file.
  --help                          Show this message and exit.
```

#### Example

The following command reads the csv file and outputs a `hotels.xml` file. The `--ping` option specifies that all urls should be requested for a valid response as part of the command.

```
$ bellboy parse -i ./data/hotels.csv -o hotels -f xml -p -s 200 -x 3
```

## Tests

## Implementation Choices

**UTF-8 validation**

Taken from [wikipedia](https://en.wikipedia.org/wiki/UTF-8) in the `Codepage layout` section

> Red cells must never appear in a valid UTF-8 sequence

This means that ordinals 192, 193 and 245-255 would not qualify as valid characters, so we filter hotel names where the ordinal value of the character is equal to one of these values.

**The hotel URL must be valid**

An uri that is a valid format and does not return a valid http response is possibly not a useful resource. Assuming some user experience related to the uri requires a valid http response, we should call the url and check the response. There are thousands of uri's in the data, so we do this with `asyncio` and `aiohttp`. This will still take a while for all calls to return, but the rubric provided with the challenge suggested performance was not a concern.

### Possible Further Work

- Enable two separate subcommands for the parsing and filtering.
- Make `HttpUriValidator` subclass a `Validator`, then introduce validation classes for fields or specific funtionality/filtering.
