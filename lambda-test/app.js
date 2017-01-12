const CONF = require("./secure_conf.json"),
      AWS = require("aws-sdk");

var lambda = {};

//console.log(CONF);

function runAFunctionOnLambda(fn_str, payload) {
  var settings = {
    FunctionName: fn_str,
    Payload: JSON.stringify(payload)
  }
  lambda.invoke(settings, handleResponseFromLambda);
}

function handleResponseFromLambda(err, response) {
  if (err) {
    console.log("problem");
    console.dir(err);
    return;
  }
  var data = JSON.parse(response.PayLoad);
  console.log(data);
}

//Setting up amazon webservice
function init() {
  AWS.config = new AWS.Config({
    region: "us-east-1",
    secretAccessKey: CONF.AWS_SECRET_ACCESS_KEY,
    accessKeyId: CONF.AWS_ACCESS_KEY_ID
  });

  lambda = new AWS.Lambda();

  runAFunctionOnLambda("LambdaTest1", {
    word_to_echo_str: "This is from Khanh's test"
  });
}

init();
