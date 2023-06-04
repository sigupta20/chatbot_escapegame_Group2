<script>
import { config } from '../../config'
import {v4 as uuidv4} from 'uuid';

// show a single message
var isLoadingChatMessage = false;

export default {

  data() {
    this.room = null;
    for (var i = 0; i < config.rooms.length; i++) {
      if (config.rooms[i]["id"] == this.$route.params.roomId) {
        this.room = config.rooms[i];
      }
    }

    let d = {
      "messagebox_caption": "Type here what you want to do...",
      "send_button_caption": "Do",
    }
    if( this.room["messagebox_caption"] != undefined ){
      d["messagebox_caption"] = this.room["messagebox_caption"];
    }
    if( this.room["send_button_caption"] != undefined ){
      d["send_button_caption"] = this.room["send_button_caption"];
    }
    console.log(d);
    return d;
  },
  methods: {

   displayMessage(msg, sender) {
      if (sender != "user" & sender != "bot") {
        console.error("bad sender " + sender);
      }

      let div = $("<div>")
        .addClass("chat_bubble")
        .addClass(sender)
        .appendTo($(".chat"))
        .html(msg);

      let name = "";
      if (sender == "user") {
        if( this.room["user_name"] != undefined){
          name = this.room["user_name"];
        } else{
          name = "You";
        }
        if( this.room["user-avatar"] != undefined){
          let img = $("<img/>")
            .attr("src", "/user-assets/" + this.room["user-avatar"])
            .addClass("avatar")
            .addClass("avatar-right")
            .appendTo(div)
        }
      } else {
        if( this.room["chatbot_name"] != undefined){
          name = this.room["chatbot_name"];
        } else{
          name = "Game Master";
        }
        if( this.room["chatbot-avatar"] != undefined){
          let img = $("<img/>")
            .attr("src", "/user-assets/" + this.room["chatbot-avatar"])
            .addClass("avatar")
            .addClass("avatar-left")
            .appendTo(div)
        }
      }
      $("<div>")
        .addClass("name")
        .html(name)
        .prependTo(div);
    },
    // send a message to rasa
    sendMessage() {
      let message = $(".messagebox").val();

      if( message.trim() == "" ){
        return;
      }

      if( isLoadingChatMessage ){
        return;
      }
      isLoadingChatMessage = true;
      let url = this.room["api_url"] + "/webhooks/rest/webhook";

      this.displayMessage(message, "user");
      let data = {
        "sender": this.session_id,
        "message": message
      };

      var that = this;
      $.ajax({
        url: url,
        type: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: false,
        success: function (result) {
          isLoadingChatMessage = false;
          $(".messagebox").val("");
          for (var i = 0; i < result.length; i++) {
            if (result[i]["text"] != "undefined") {
              that.displayMessage(result[i]["text"], "bot");
              window.scrollTo(0, document.body.scrollHeight);
            }
          }
        },
        error: function(result){
          isLoadingChatMessage = false;
          alert("error connecting to the server.");
        }
      });
    },
  },

  created() {
    this.session_id = uuidv4();
    
    if (this.room != null) {
      if (this.room["background-image"] != undefined) {
        //let path = require("/public/background-images/" + this.room["background-image"]);
        let path = "url(/user-assets/" + this.room["background-image"] + ")";
        $("body").css("background-image", path);
      }
    }

    let that = this;

    $(document).ready(function () {

      // display welcome message
      that.displayMessage(that.room["welcome-message"], "bot");

      // listen to enter key on message input field
      $('.messagebox').keypress(function (e) {
        if (e.keyCode == 13) {
          that.sendMessage();
        }
      });

      // send button click function
      $(".send_button").click(function (e) {
        e.preventDefault();
        that.sendMessage();
      });

      $(".header").hide();
    });
  }
};
</script>

<template>
  <div class="chat">
    <div>
      <a href="/" class="close_room">
        <img src="/public/close.png" alt="x" />
      </a>
    </div>
  </div>
  <div class="separator"></div>
  <div class="input_area row footer">
    
    <input type="text" class="messagebox" :placeholder="messagebox_caption" />
    <input type="button" :value="send_button_caption" class="send_button" />
  </div>

</template>
