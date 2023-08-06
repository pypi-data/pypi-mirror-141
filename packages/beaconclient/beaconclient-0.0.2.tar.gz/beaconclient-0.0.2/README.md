

## Beacon Client

Welcome to the Beacon Client package for https://getbeacon.xyz. 


### Getting Started

Install `beaconclient` via: 

`pip install beaconclient`

You'll want to head over to `https://getbeacon.xyz/docs` to start linking up your integrations and getting your API key.


### How to use

```
from beaconclient.beacon import Beacon

client = Beacon('<YOUR_API_KEY>')

client.send('Your beacon message')
```