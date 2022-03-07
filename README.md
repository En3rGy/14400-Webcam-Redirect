# Webcam Redirect (14400)

## Description 

The module provides data fetched from a target URL via an internal server on IP 127.0.0.1 and a configurable port.
Target URL and port can be updated during runtime. Fetching https URL is possible.

*Caution 1*: Do not expect any security activities performed by the internal server!

*Caution 2*: The content of the target URL is fetched on setting the target URL only. The URL must be re-set if the content shall be fetched again.

Use Case: Create dynamic images hosted by different URLs, e.g.
- show different colors for current status of rgbw led
- show different status symbols provided by an external source

### Installation
- Create a webcam and connect it:
  - IP-Address: 127.0.0.1
  - Protocol: https
  - IP-Port: 443 (independent of input #3)
  - Path to image: Value of input #1 + a "random" filename, e.g. /14400/img.png
- Create a logic to create and update the target URL depending on your demands

## Inputs

| No. | Name | Initialisation | Description |
| --- | --- | --- | --- |
| 1 |  Base-Path | "/14400" | Path to the server |
| 2 | Port | 0 | Internal port of the server; if not set, HS will pick a free one |
| 3 | Target URL | "" | URL from where the content is fetched; if set as "0", a transparent 4x4 px png image is provided |

## Outputs

| No. | Name | Initialisation | Description |
| --- | --- | --- | --- |
| 1 | Status | "" | Text indicating the current status of the module |

## Others

- Neuberechnung beim Start: Nein
- Baustein ist remanent: Nein
- Baustein Id: 14400
- Kategorie: Datenaustausch

### Change Log

- v0.04
  - Bug: Fixed port & base path
  - Impr.: Added thread save data access
- v0.03
  - Impr.: Return transparent png if target url is empty or 0 
- v0.02
  - Bug: Fixed wrong composition of code of v0.01
- v0.01
    - Initial Release

### Open Issues / Know Bugs

-

### Support

Please use [github issue feature](https://github.com/En3rGy/14400-Webcam-Redirect/issues) to report bugs or rise feature requests.
Questions can be addressed as new threads at the [knx-user-forum.de](https://knx-user-forum.de) also. There might be discussions and solutions already.

### Code

The Python-Code of the module can be accessed via [github](https://github.com/En3rGy/14400-Webcam-Redirect).

### Devleopment Environment

- [Python 2.7.18](https://www.python.org/download/releases/2.7/)
    - Install python markdown module (for generating the documentation) `python -m pip install markdown`
- Python editor [PyCharm](https://www.jetbrains.com/pycharm/)
- [Gira Homeserver Interface Information](http://www.hs-help.net/hshelp/gira/other_documentation/Schnittstelleninformationen.zip)

## Requirements

1. The module shall fetch the content provided by a user configurable URL (*target URL*).
2. The module shall provide a HTTP server on 127.0.0.1 and a user configurable port.
3. The module shall fetch data from http and https URL.
4. The module shall provide the fetched data as response to a incoming GET request.
5. The module shall set the content header field bases on the *target URL* content information.
6. If "0" is set as *target URL*, the module shall set an 4x4 px transparent png-file as *fetched data*.

## Software Design Description

### Definitions

x

### Solution Outline

* Fetch target URL content if corresponding input is set
* Open a http sever within an own thread
* Provide the fetched *target data* if a get request is received by the server (URL is don't care)

## Validation & Verification

* Requirements are verified via unit tests.

## Licence

Copyright 2022 T. Paul

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
