let webex;
let receiveTranscriptionOption = true;
let transcript_final_result = {"transcript":""};
let meetings;
let current_meeting;


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

      let actionables = response["result"]["actionables"]
      let actionablesContainer = document.getElementById('actionablesContainer')
      actionablesContainer.innerHTML = `<div>${actionables}</div>`

      let time = response["result"]["agenda"]
      let timeContainer = document.getElementById('timeContainer')
      timeContainer.innerHTML = `<div>${time}</div>`
    }
  });
  
  xhr.open("POST", "http://127.0.0.1:3000/dynamic_query");
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.setRequestHeader('Access-Control-Allow-Origin','*');
  xhr.send(data);
}



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
      "",
  },
});

webex.once("ready", () => {
  console.log("Authentication#initWebex() :: Webex Ready");
});

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

const intervalID = setInterval(summary, 100000);

