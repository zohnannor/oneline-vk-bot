(
    lambda TOKEN, GROUP_ID, URL="https://api.vk.com/method/": (
        lambda get: (
            lambda globs={
                "things": get(URL + "groups.getLongPollServer", {"group_id": GROUP_ID})[
                    "response"
                ]
            }: (
                globs.update(
                    {
                        "server": globs["things"]["server"],
                        "key": globs["things"]["key"],
                        "ts": globs["things"]["ts"],
                    }
                ),
                (lambda f: (lambda x: x(x))(lambda y: f(lambda *args: y(y)(*args))))(
                    lambda w: (
                        lambda globs: (
                            globs.update(
                                {
                                    "things": get(
                                        globs["server"],
                                        {
                                            "act": "a_check",
                                            "key": globs["key"],
                                            "ts": globs["ts"],
                                            "wait": "25",
                                        },
                                    ),
                                }
                            ),
                            globs.update({"ts": globs["things"]["ts"]}),
                            [
                                (
                                    lambda peer_id, message: get(
                                        URL + "messages.send",
                                        {
                                            "peer_id": peer_id,
                                            "message": message,
                                            "random_id": 0,
                                        },
                                    )
                                )(
                                    update["object"]["message"]["from_id"],
                                    {
                                        "привет": lambda msg: "Привет, {}!".format(
                                            get(
                                                URL + "users.get",
                                                {"user_ids": msg["from_id"]},
                                            )["response"][0]["first_name"]
                                        ),
                                        "скажи": lambda msg: msg["text"].partition(" ")[
                                            2:
                                        ][0],
                                        "": lambda _: "напиши что-нибудь!",
                                    }.get(
                                        update["object"]["message"]["text"]
                                        .partition(" ")[0]
                                        .lower(),
                                        lambda _: "неизвестная команда!",
                                    )(
                                        update["object"]["message"]
                                    ),
                                )
                                for update in globs["things"]["updates"]
                                if update["type"] == "message_new"
                            ],
                            w(globs),
                        )
                    )
                )(globs),
            )
        )()
    )(
        lambda url, data, request=__import__(
            "urllib.request"
        ).request, parse=__import__("urllib.parse").parse: __import__("json").loads(
            request.urlopen(
                request.Request(
                    url,
                    parse.urlencode(
                        {**data, "access_token": TOKEN, "v": "5.120"}
                    ).encode(),
                )
            )
            .read()
            .decode()
        )
    )
)(
    TOKEN="Your Token",
    GROUP_ID="Your Group ID",
)

