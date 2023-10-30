let webex;
let receiveTranscriptionOption = true;
let transcript_final_result = {"transcript":""};
let meetings;
let current_meeting;
let actionables="";
var ACCESS_TOKEN = "";
let is_bot = false;
let botEmailID = "";
let time_interval = 60000;
let interval = 1
let botIntervalID;

function summary() {
  // WARNING: For POST requests, body is set to null by browsers.
  console.log(transcript_final_result["transcript"])
  var data = JSON.stringify({
    "module_name": "openai",
    "method_type": "module_function",
    "method_name": "process_transcript",
    "args": [
      transcript_final_result["transcript"]
    ]
  });
  
  var xhr = new XMLHttpRequest();
  xhr.withCredentials = false;
  
  xhr.addEventListener("readystatechange", function() {
    if(this.readyState === 4) {
      response = JSON.parse(this.responseText)
      console.log(response);
      let summary = response["result"]["summary"] 
      let summaryContainer = document.getElementById('summaryContainer')
      summaryContainer.innerHTML = `<div>${summary}</div>`

      actionables = response["result"]["actionables"]
      let actionablesContainer = document.getElementById('actionablesContainer')
      actionablesContainer.innerHTML = `<div>${actionables}</div>`

      let time = response["result"]["agenda"]
      let timeContainer = document.getElementById('timeContainer')
      timeContainer.innerHTML = `<div>${time}</div>`

      // index.html
    }
  });
  
  xhr.open("POST", "http://127.0.0.1:3000/dynamic_query");
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.setRequestHeader('Access-Control-Allow-Origin','*');
  xhr.send(data);
}


function bot_response() {
  // WARNING: For POST requests, body is set to null by browsers. "blazetranscriptionbot@webex.bot"
  
    console.log("sending actionables to bot")
    let data = JSON.stringify({
      "toPersonEmail": botEmailID ,
      "text": actionables,
      
    });
    
    var xhr = new XMLHttpRequest();
    xhr.withCredentials = false;
    
    

    xhr.open("POST", "https://webexapis.com/v1/messages");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader('Authorization',`Bearer ${ACCESS_TOKEN}`);
    xhr.send(data);
  
  
}

// Send function to send keys/ids to the REST API 
function submitForm() {
  var webexId = document.getElementById("access-token").value;
  botEmailID = document.getElementById("bot-email-id").value;
  interval = document.getElementById("time-interval").value;

  if (botEmailID !== "") {
    is_bot = true
    if (interval !== ""){
      time_interval = 60000 * interval
    }
  }
  if(is_bot===true){
    if(!botIntervalID){
      botIntervalID = setInterval(bot_response, time_interval);
    }
    
  }

  // Call big scrip tto use WebexID key to register the mtg 

  ACCESS_TOKEN = webexId;  
  document.getElementById("iniform").style.display = "none";
  registerMeeting();


}

function registerMeeting() {

  console.log("Entered script, got access token"); 
  console.log(ACCESS_TOKEN);

  initWebex(); 
  console.log("Initialized Webex"); 

  setTimeout(function() {
      register();
      console.log("Register meeting");
  }, 2000); 

  
}

function initWebex(){
  webex = window.webex = Webex.init({
    config: {
      logger: {
        level: "debug",
      },
      meetings: {
        reconnection: {
          enabled: true,
        },
        enableRtx: true,
        experimental: {
          enableUnifiedMeetings: true,
        },
      },
      // Any other sdk config we need
    },
    credentials: {
      access_token:
        ACCESS_TOKEN,
    },
  });
  
  webex.once("ready", () => {
    console.log("Authentication#initWebex() :: Webex Ready");
  });
}



function register(){
  webex.meetings.register().then(() => {
    console.log("successful registered");
    webex.meetings
      .syncMeetings()
      .then(
        () =>
          new Promise((resolve) => {
            setTimeout(() => resolve(), 3000);
          })
      )
      .then(() => {
        console.log(
          "MeetingsManagement#collectMeetings() :: successfully collected meetings"
        );
        meetings = webex.meetings.getAllMeetings();
  
        if (webex.meetings.registered) {
          console.log(meetings);
          current_meeting = meetings[Object.keys(meetings)[0]];
          console.log(current_meeting);
          current_meeting.on(
            "meeting:receiveTranscription:started",
            (payload) => {
              if (payload["type"]=="transcript_final_result"){
                transcript_final_result["transcript"] = transcript_final_result["transcript"] + ", " + payload["transcription"];
                
              }
             
              console.log(transcript_final_result)
              
            }
          );
        }
        const joinOptions = {
          moveToResource: false,
          resourceId: webex.devicemanager._pairedDevice
            ? webex.devicemanager._pairedDevice.identity.id
            : undefined,
          receiveTranscription: receiveTranscriptionOption,
        };
  
        current_meeting.join(joinOptions);
      });
  });
}


const intervalID = setInterval(summary, 10000);

