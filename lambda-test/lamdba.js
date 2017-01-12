//Function in lambda

function echoMe(payload, context) {
    console.log("we echoed this word: " + payload.word_to_echo_str);
    var return_me = {
        super_secret_init: 42,
        word_to_echo_str: payload.word_to_echo_str + "!"
    };
    context.succeed(return_me);
}

exports.handler = echoMe;

