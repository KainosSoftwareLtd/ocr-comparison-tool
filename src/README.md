# OCR comparison tool

Welcome to this repository which provides you with a complete-standalone, automated tool to compare the performance of different OCR services.

This tool was developed to compare the performance of Amazon's, Google's and Microsoft's text detection in a variety of images from: handdrawn characters and words to 'live scene' photographs.
*The blog can be found [here](https://medium.com/)*
<br>

### Disclaimer

> This project was developed using:
> + `python 3.7.4`
> + `python modules version` as described in `requirements.txt`
> + `CharacTER.py` released on 27/06/2019

> *Software versions are subject to change with new releases, to ensure the project runs smoothly without alteration the above versions should be used.*
> *This software was last ran on 14/10/2019*

## Introduction

This tool is fully automated to generate images' transcriptions from disk, pass them, one-by-one, into each [supported OCR service](#amazon) and generate meaningful metrics.

This tool makes use of the command-line interface (CLI) to operate.

The tool currrently supports the following OCR services:
<br>

##### Amazon
___
+ [Textract](https://console.aws.amazon.com/textract/home) is used for detecting *document* text
+ [Rekognition](https://console.aws.amazon.com/rekognition/home) is used for detecting *live scene* text
<br>

##### Google
___
+ [Vision](https://cloud.google.com/vision/) is used for detecting *document* and *live scene* text
<br>

##### Microsoft
___
+ [Computer Vision](https://azure.microsoft.com/en-gb/services/cognitive-services/computer-vision/) is used for detecting *document* and *live scene* text
<br>

## Getting Started

Following the instructions below will enable you to use the tool for comparing your own images.
<br>

### Prerequisites

The following need to be setup before using this tool.
<br>

##### Amazon
___
1. Follow the steps in [this guide](https://docs.aws.amazon.com/rekognition/latest/dg/setting-up.html) to create an account and setup a user
2. Follow steps 2-4 in [this guide](https://docs.aws.amazon.com/textract/latest/dg/setup-awscli-sdk.html) to generate your account's key
<br>

##### Google
___
1. Follow the steps in [this guide](https://cloud.google.com/billing/docs/how-to/manage-billing-account#create_a_new_billing_account) to create a billing activated account
2. Follow the steps in [this guide](https://cloud.google.com/vision/docs/before-you-begin) to enabled Google Vision for a Google Cloud Project
<br>

##### Microsoft
___
1. Follow the steps in [this guide](https://docs.microsoft.com/en-gb/azure/cognitive-services/cognitive-services-apis-create-account?tabs=multiservice%2Clinux) to create an account and link a congitive service resource to it
2. Create a secret file, e.g.
```

vi /path/to/directory/.ms/credentials.txt

```

3. Follow the step 'Get the keys from you resource' in [this guide](https://docs.microsoft.com/en-gb/azure/cognitive-services/cognitive-services-apis-create-account?tabs=multiservice%2Clinux) and store this in the secret file (replace the placeholder key value with your account's key)
```

{
    "key": "XXXXXXXXXXXXXXX00XXX"
}

```
<br>

> **Optional**: It is recommended that you store your service/access keys in a secret '.' file.

```

mv /path/to/saved/credentials.txt /path/to/file/.secret_file.txt

```

>*You will need the pathways to these keys in future steps*
<br>

### Installation

To install this tool to your local machine for comparison purposes, follow the instructions below.

1. Clone this repo to your local machine
```

git clone <HTTPS URL>/ocr_comparison_tool.git


```

2. Move into the ocr_comparison_tool directory
```

cd /path/to/cloned/directory/ocr_comparison_tool/

```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.5. **Optional**: Create a python3 virtual environment
```

python3 -m venv .

```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*then*
```

. bin/activate

```

3. Install the required python libraries
```

pip3 install -r requirements.txt

```
<br>

### Configuration

To configure the [OCR services](#introduction) for this tool, follow the steps below.
<br>

##### Amazon
---
In `./ocr_settings/amazon_settings.py` change the placeholder paths to your specific secret files:
```

environ['AWS_SHARED_CREDENTIALS_FILE']='/path/to/your/secret/credential/.file.txt'
environ['AWS_CONFIG_FILE']='/path/to/your/secret/config/.file.txt'

```
<br>

##### Google
___
In `./ocr_settings/google_settings.py` change the placeholder path to your specific secret file:
```

environ['GOOGLE_APPLICATION_CREDENTIALS']='/path/to/your/secret/credential/.file.json'

```
<br>

##### Microsoft
___
In `./ocr_settings/microsoft_settings.py` change the placeholder path to your specific secret file:
```

MICROSOFT_ACCESS_CREDENTIALS='/path/to/your/secret/credential/.file.json'

```
<br>

##### CharacTER
___
In `./ocr_settings/gateway_settings.py` change the placeholder path to your specific CharacTER.py file:
```

environ['CHARACTER_SCRIPT_PATH']='/path/to/script/CharacTER.py'

```
<br>

## Operation

##### Constraints

+ images must `.jpg` or `.png` format
+ images must be *at least* `50 x 50pxl`
<br>

---

This tool supports a variety of ways to process images and their transcripts:
+ [run using directory](#run-using-directory)
+ [run using single image (transcript auto-generated)](#run-using-single-image-transcript-auto-generated)
+ [run using single image (transcript provided)](#run-using-single-image-transcript-provided)
+ [define images' properties filename](#define-images-properties-filename)
+ [define type of OCR transcript](#define-type-of-ocr-transcript)
<br>

#### Run using directory
```

python3 /path/to/ocr_comparison_tool/cmd.py --dir /path/to/entry_dir

```
<br>

> **Note**: For this option, *entry_dir* must adhere to the following structure:
 ```

entry_dir 
├── props.csv       # properties for images
├── ogl/            # original transcripts*
├── res/            # apis' transcripts*
├── met/            # CharacTER metric scores*
└── imgs/           # images to be transcribed
     ├── img1.jpg
     ├── img2.png
     ├──    .
     ├──    .
     ├──    .
     └── imgn.jpg

```
> Directories: ogl, res and met are **optional*** as they are generated by the tool.
___

#### Run using single image (transcript auto-generated)
```

python3 /path/to/ocr_comparison_tool/cmd.py --img /path/to/image.jpg

```
<br>

> **Note**: This command auto-generates the original transcript and so assumes that *props.csv* is located within the current working directory 
___

#### Run using single image (transcript provided)
```

python3 /path/to/ocr_comparison_tool/cmd.py --ogl /path/to/transcript.txt --img /path/to/image.jpg

```
---

#### Define images' properties filename
```

python3 /path/to/ocr_comparison_tool/cmd.py --prp properties.csv

```
<br>

> **Note**: The property file must be located in the current working directory
---

#### Define type of OCR transcript
```

python3 /path/to/ocr_comparison_tool/cmd.py --med [image/document/both]

```
<br>

> **Note**: Changing the media invokes only the models for that type
<br>

## Authors

+ Applied Innovation - [Kainos](https://www.kainos.com/)

## Acknowledgments

+ [CharacTER metrics](https://github.com/rwth-i6/CharacTER)