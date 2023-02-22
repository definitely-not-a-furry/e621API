#e621API
---
e621API is a program that can be used to download large amounts of media (pictures, videos, flash media etc.) from [e621.net](https://e621.net/).
The name might be a little bit misleading: e621API is **not** an application programming interface for e621.
Included with e621API is another program (e6b_manager) that can be used to view and edit [`.e6b` files](https://github.com/definitely-not-a-furry/e621API/blob/main/README.md#e6b-files) 

`config.json`
---
Parameters:
- `silent-mode`: if this is turned on, echo will be reduced to a minimal. This option will be ignored if debug-mode is true
- `debug-mode`: if this is turned on, the terminal will display extended information
- `clear-terminal`: if this is turned on, the terminal will be cleared on startup
- `header-name`: this is what will be shown to the server if you use this program, this is a required option
- `header-version`: the same as `header-name` but for the version of the program
- `username` should be **your own** username. If you don't have an account on e621 (which I doubt), you should fill in your name
- `rate-limit` is the amount of seconds the program waits before it sends a new request. This must be atleast 0.6

`.e6b` files
---
`.e6b` is a file format that can be used to store large amounts of static media links. It is encoded in hexadecimal. `.e6b` files are also is useful for sharing.
