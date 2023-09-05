# Bigram frequency assignment

## Description

Get most frequent bigram counts from a text file.

Lowercases all words. Words are delimited by any non-word characters. These separators are
not included in the bigrams.

The bigrams are sorted descending by occurrences. 

This repository contains both the script at `src/bigram_frequency.py` and the web API implemented using Flask at `src/flask_app.py`.

## Usage

First, in the repository root, build the docker image:

```bash
docker build -t msd_assignment_bigram .
```

The entrypoint of the container is the Flask development server.

### Running the server

To run the (development) server with the two endpoints, run the following command:

```bash
docker run -p 5000:5000 msd_assignment_bigram
```

The server will be available at `http://localhost:5000`. Your local machine port the server is accessible at can be changed
by changing the first port number in the command.

#### Endpoints

Output is JSON. The format is as follows:

```json
{
  "bigram_counts": [
    16,
    15
  ],
  "bigrams": [
    [
      "of",
      "the"
    ],
    [
      "in",
      "the"
    ]
  ]  
}
```

In case an error is detected, the response will be a JSON object with the following format (HTTP status code 400):

```json
{
  "error": "Error message"
}
```

##### /bigrams_from_file


This endpoint takes a text file as input and returns the bigram frequency of the file. The file should be sent as a
`multipart/form-data` request with the file as the `file` field. The response is a JSON object with the bigram frequency.

```bash
curl -X POST -F "file=@<input_file>" http://localhost:5000/bigrams_from_file
```

where `<input_file>` is the path to the file to be sent. File is expected to be utf-8 encoded. `num_bigrams` can be specified
as a query parameter. If not specified, the default value is 10.

##### /bigrams_from_wiki

This endpoint takes a Wikipedia page as input and returns the bigram frequency of the article (ten most frequent bigrams).

```bash
curl http://localhost:5000/bigrams_from_wiki/<page_title>
```

where `<page_title>` is the title of the Wikipedia page (e.g. `/dev/zero`)


### Running the bigram frequency script

To run the script that generates the bigram frequency, run the following command (in the running docker container, if that's the
way you are running it).

You can specify the input file and the number of bigrams returned as `-n` argument.

```bash
python src/bigram_frequency.py <input_file> -n <number_of_bigrams>
```
