# OwenAI
A vocal Chat GPT client, sometimes it's nice to talk to a robot.

## Installation Instructions and Requirements
Clone the repo and install dependencies:
```bash
git clone https://github.com/JaegerJochimsen/OwenAI.git &&\
python -m venv . &&\
./bin/activate &&\
pip install git+https://github.com/openai/whisper.git &&\
pip install -r requirements.txt
```
Create an OpenAI API Key (used for talking with the gpt-3.5-turbo model):
[OpenAI API for Developers](https://openai.com/product#made-for-developers)

## Run Owen locally
```bash
python -m owen_ai
```

## Notes
* Currently, this project has only been built to supported Mac OSX and may require additional setup otherwise
* Owen reads your api key from the terminal at runtime so your keys stay secret and secure
* Currently, Owen can only respond to a single query before he needs to rest. This will be increased in future development

## Future Features
* Add support for Windows/Linux
* Add conversational patter to Owen
* Make Owen's voice configurable by the user via conversation
* Make Owen's role configurable by the user via conversation
* Allow Owen to hold a multi query-response dialogue