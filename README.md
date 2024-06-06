Deployed automatically on push to main to:

https://mm.nwolff.info/

Usage statistics collected with umami.js

---

Install elm tools:

    npm install elm elm-format elm-live elm-review

To develop:

    npx elm-live src/Main.elm --open -- --output target/elm.js --debug

To build:

    npx elm make src/Main.elm --output target/elm.js

To review the code:

    npx elm-review --template jfmengels/elm-review-config/application
