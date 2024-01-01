module Main exposing (MailmergeQuery, Model, Msg(..), main)

import Browser exposing (Document)
import File exposing (File)
import File.Select as Select
import Html exposing (Attribute, Html, button, div, h2, h5, text)
import Html.Attributes exposing (class, style)
import Html.Events exposing (onClick, preventDefaultOn)
import Json.Decode as D
import Result exposing (andThen, fromMaybe)
import Task
import Xml.Decode exposing (Decoder, path, run, single, stringAttr)
import Zip exposing (Zip)
import Zip.Entry as Entry


acceptedFiles : List String
acceptedFiles =
    [ ".xml,application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document" ]


type MailmergeQuery
    = Empty
    | Error String
    | Query String


main : Program () Model Msg
main =
    Browser.document
        { init = init
        , update = update
        , subscriptions = subscriptions
        , view = view
        }


type alias Model =
    { hover : Bool
    , fileName : Maybe String
    , queryInfo : MailmergeQuery
    }


init : () -> ( Model, Cmd Msg )
init _ =
    ( Model False Nothing Empty, Cmd.none )


type Msg
    = Pick
    | DragEnter
    | DragLeave
    | GotFiles File (List File)
    | GotZip (Maybe Zip)


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Pick ->
            ( model, Select.files acceptedFiles GotFiles )

        GotFiles file _ ->
            ( { model | fileName = Just (File.name file), hover = False }, readArchive file )

        GotZip maybeZip ->
            case maybeZip of
                Nothing ->
                    ( { model | queryInfo = Error "Not a word file" }, Cmd.none )

                Just zip ->
                    ( { model | queryInfo = retrieveMailmergeQuery zip }, Cmd.none )

        DragEnter ->
            ( { model | hover = True }, Cmd.none )

        DragLeave ->
            ( { model | hover = False }, Cmd.none )


readArchive : File -> Cmd Msg
readArchive file =
    file
        |> File.toBytes
        |> Task.map Zip.fromBytes
        |> Task.perform GotZip


mergeQueryDecoder : Decoder String
mergeQueryDecoder =
    path [ "w:mailMerge", "w:query" ] (single (stringAttr "w:val"))


retrieveMailmergeQuery : Zip -> MailmergeQuery
retrieveMailmergeQuery zip =
    Zip.getEntry "word/settings.xml" zip
        |> fromMaybe "No settings.xml zip entry in file"
        |> andThen (Entry.toString >> Result.mapError (\_ -> "Cannot retrieve settings.xml zip entry contents"))
        |> andThen (run mergeQueryDecoder >> Result.mapError (\_ -> "Cannot retrieve merge query (make sure you upload an unmerged file)"))
        |> (\result ->
                case result of
                    Ok query ->
                        Query query

                    Err error ->
                        Error error
           )


subscriptions : Model -> Sub Msg
subscriptions _ =
    Sub.none


view : Model -> Document Msg
view model =
    Document "Word Mailmerge Datasource"
        [ div [ class "container" ]
            [ h2 [ class "mt-2 mb-4" ] [ text "Retrieve the filters and orderings used in a word mailmerge" ]
            , dropZone model.hover
            , case model.fileName of
                Nothing ->
                    text ""

                Just name ->
                    h5 [] [ text name ]
            , case model.queryInfo of
                Empty ->
                    text ""

                Error error ->
                    div [ class "alert alert-danger" ] [ text error ]

                Query query ->
                    div [ class "alert alert-success" ] [ text query ]
            ]
        ]


dropZone : Bool -> Html Msg
dropZone hover =
    div
        [ class "dropzone"
        , style "border"
            (if hover then
                "6px dashed purple"

             else
                "6px dashed #ccc"
            )
        , hijackOn "dragenter" (D.succeed DragEnter)
        , hijackOn "dragover" (D.succeed DragEnter)
        , hijackOn "dragleave" (D.succeed DragLeave)
        , hijackOn "drop" dropDecoder
        ]
        [ text "Drop a Word Mailmerge file"
        , text ""
        , button [ onClick Pick ] [ text "or select one" ]
        ]


dropDecoder : D.Decoder Msg
dropDecoder =
    D.at [ "dataTransfer", "files" ] (D.oneOrMore GotFiles File.decoder)


hijackOn : String -> D.Decoder msg -> Attribute msg
hijackOn event decoder =
    preventDefaultOn event (D.map hijack decoder)


hijack : msg -> ( msg, Bool )
hijack msg =
    ( msg, True )
