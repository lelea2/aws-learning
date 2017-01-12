//Lambda function notify email account when image is uploaded to s3 account

'use strict';

// Dependencies
var AWS = require('aws-sdk');

// Set my region
AWS.config.update({region: 'us-west-1'});

// Get reference to SES client
var ses = new AWS.SES();

// action
exports.handler = function(event, context) {
  // Grab stuff from event
  var s3Url = 'https://s3.amazonaws.com/';
  var srcBucket = event.Records[0].s3.bucket.name;
  var srcKey    = event.Records[0].s3.object.key;
  var objectUrl = s3Url + srcBucket + '/' + srcKey;
  var originalBucket = srcBucket.match(/.*?(?=resized|$)/i)[0];
  var originalObjectUrl = s3Url + originalBucket + '/' + objectUrl.match(/resized-(.*?)(;|$)/)[1];
  console.log(objectUrl);
  console.log(originalObjectUrl);

  // Set some variables
  var toAddress = 'kareendao88@gmail.com';
  var subject = 'New Image Upload!';
  var htmlMessage = '<div style="width:500px;font-family: Calibri,Candara,Segoe,Optima,Arial,sans-serif; font-size:14px;"> \
              <h3>New Image Upload!</h3> \
              <p> \
                <a href="' + originalObjectUrl + '" target="_blank"> \
                  <img align="right" src="' + objectUrl + '" style="float:right; padding-left:5px; border:0;s"> \
                </a> \
                Administrator,<br> \
                A user has uploaded an image into <i>' + originalBucket + '</i>.<br><br> \
                \
                To view the image, click the thumbnail image or <a href="' + originalObjectUrl + '" target="_blank">this link</a>. \
              </p> \
            </div>';

  // Try to send SES
  var params = {
    Destination: {
      BccAddresses: [],
      CcAddresses: [],
      ToAddresses: [toAddress]
    },
      Message: { /* required */
      Body: { /* required */
        Html: {
        Data: htmlMessage, /* required */
        Charset: 'UTF-8'
        },
        Text: {
        Data: 'Plaintext' /* required */
        }
      },
      Subject: { /* required */
        Data: subject, /* required */
        Charset: 'UTF-8'
      }
      },
      Source: 'kareendao88@gmail.com', /* required */
      ReplyToAddresses: [
      'kareendao88@gmail.com',
      /* more items */
      ]
  };

  // Send the email
  ses.sendEmail(params, function(err, data) {
    if(err) {
      console.log(err, err.stack); // an error occurred
    } else {
      context.done(null, "Message sent - ID: " + data.MessageId);
    }
  });

};

