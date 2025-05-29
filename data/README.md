# General Data Engineering

this is a place for storing data sources, and sharing applications in data-science, machine learning, or any data concepts you can contribute. 

---

## data-serv

[over here ⛵](https://github.com/odds-get-evened/data-serv)

### what is it?

it is a micro-service that can send simulated data streams (primarily integer, float, double type ranges).

### why was it made?

for my lack of trust in using my laptop to monitor IoT devices over WiFi/COM/Bluetooth (security issues), I made `data-serv` to stream mock temperatures, but instead of simple randomness, I added thresholds as well to make it less jumpy, and simulate gradual real temps.

### what can i be used for?

the idea here is connect ot the service however many clients you want given resources, and train models via client commands that process the server stream. workarounds 🎄
