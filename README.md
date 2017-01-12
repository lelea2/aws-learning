# aws-learning
Prototype to learn about AWS


* Creae Access and Secret key on AWS: http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSGettingStartedGuide/AWSCredentials.html

### aws-lambda
* What is AWS Lambda?
Function in AWS Cloud, Used for
- Background processing
- Web endpoint
- Serverless (we don't need to manage server)

##### Event Sources

* s3 Buckets
* Kinesis Streams
* SNS
* DynamoDB
* Cognito
* API Gateway


##### Build Lambda function

Eg:
```javascript
exports.handler = function(event, context) {
  console.log('value1=' + event.key1);
  console.log('value2=' + event.key2);
  context.succeed(event.key1 +  ' ' + event.key2);
}

````

* Blueprint
* Memory & Timeout (in advance settings)
* Template testing provided in Lambda


##### AWS Lambda & S3: Image resizing in Lambda

* Create a background task to handle image uploading on S3 (Eg: Lambda function runs on image upload to re-size big image to thumbnail)

* Create 2 bucket in S3:
- shine-lambda-example
- shine-lambda-example-resize

* Configure S3 bucket for Lambda
Under Properties ==> Events ==> Object created -- Lambda function to be called

```npm install async gm```

zip -r CreateThumbnail.zip CreateThumbnail.js node_modules

```javascript
var AWS = require('aws-sdk'); //installed in AWS env, don't need to maintain in package.json
var async = require('async');
var gm = require('gm').subClass({imageMagick: true});
var s3 = new AWS.S3();

exports.handler = function(event, context) {
  var srcBucket = event.Records[0].s3.bucket.name;
  var srcKey = event.Records[0].s3.object.key;
  var dstBucket = srcBucket + " resized";
  var dstKey = "resized-" + srcKey;

  async.waterfall([
    function download(next) {
      s3.getObject({Bucket: srcBucket, Key: srcKey}, next);
    },

    function transform(response, next) {

    },

    function upload(contentType, data, next) {
      s3.putObject({Bucket: dstBucket, Key: dstKey, Body: data}, next);
    }
  ], function (err) {
    context.done();
  });
}

```

##### AWS Lambda with API Gateway

##### Mapping API gateway request with event object (for headers, body, method...)
```
{
  "body" : $input.json('$'),
  "headers": {
    #foreach($header in $input.params().header.keySet())
    "$header": "$util.escapeJavaScript($input.params().header.get($header))" #if($foreach.hasNext),#end

    #end
  },
  "method": "$context.httpMethod",
  "params": {
    #foreach($param in $input.params().path.keySet())
    "$param": "$util.escapeJavaScript($input.params().path.get($param))" #if($foreach.hasNext),#end

    #end
  },
  "query": {
    #foreach($queryParam in $input.params().querystring.keySet())
    "$queryParam": "$util.escapeJavaScript($input.params().querystring.get($queryParam))" #if($foreach.hasNext),#end

    #end
  }
}
```

##### Way to  change http status codes returned by Amazon API Gateway
* http://stackoverflow.com/questions/31329495/is-there-a-way-to-change-the-http-status-codes-returned-by-amazon-api-gateway

```javascript


```

##### JAWS -- Server-less stack on Lambda



#### Key note for https://www.youtube.com/watch?v=ZBxWZ9bgd44

* Declare API with API gateway
* Application logic in AWS Lambda
* Resgiter and login API with Amazon Cognito
* Authorization in AWS IAM
* Generate & connect with client SDK


##### References

http://kennbrodhagen.net/2015/12/06/how-to-create-a-request-object-for-your-lambda-event-from-api-gateway/


