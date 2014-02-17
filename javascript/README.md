<hr />

# Tinkerforge

Tinkerforge is a Node.JS package that provides the
Tinkerforge API bindings for all Tinkerforge bricks
and bricklets.

## How to Install

```
npm install Tinkerforge
```

## How to Use

To be able to use the bindings first the API must be
included in the code in following way:

```js
var Tinkerforge = require('Tinkerforge');
```

After that all the classes and their functionalities
provided by the binding can be accessed like:

```js
var IPConnection = Tinkerforge.IPConnection;
var BrickletDualButton = Tinkerforge.BrickletDualButton;
```

After that to create an instance of a class:

```js
IPConnection = new IPConnection();
BrickletDualButton = new BrickletDualButton();
```

## Examples

### Enumeration
```js

```
### Getter Call
```js

```
### Setter Call
```js

``

### Callback
```js

```
## License

CC0

