Deployed automatically on push to main to:

https://mm.nwolff.info/

Usage statistics collected with umami.js

---

Requires elm0.19.1

To install elm without being a sudoer:

    npm install elm

To develop:

    elm reactor

Or if you've installed elm-live:

    elm-live src/Main.elm --open -- --output target/elm.js --debug

To build:

    elm make src/Main.elm --output target/elm.js

To review the code you need to install elm-review, then:

    elm-review --template jfmengels/elm-review-config/application
