# SwitchBotIntegration
Integrating the SwitchBotAPI to control devices.

## The Inspiration

I work remotely and have a light on my desk that I turn on to let my family know when I'm on a call for work.  The problem is that I have to stand up to reach the light.

I purchased a SwitchBot and wrote this small application so that I can turn on the light by running a script.

Today: Not having to stand.  Tomorrow: Who knows?...

## Setup

This requires a json config file in the root directory named `switchbot_config.json`.

#### Example:

```json
{
  "token": "yourswitchbottokenhere",
  "desklight_device_id": "XX12345689"
}
```

## SwitchBotAPI

Documentation for setting up the SwitchBotAPI and getting your developer token:

https://github.com/OpenWonderLabs/SwitchBotAPI
