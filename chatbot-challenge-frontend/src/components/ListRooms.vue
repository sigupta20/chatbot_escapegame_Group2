<script setup>
import { config } from '../../config'
</script>

<template>
    <div class="content-box">
        <h1>Chatbot Challenge</h1>
        <!--<ul class="nav">
          <li>
            <RouterLink to="/">Escape Rooms</RouterLink>
            </li>
          <li>
            <RouterLink to="/about">About</RouterLink>
            </li>
        </ul>-->
        <p>&nbsp;</p>

        <h2>Choose your escape room</h2>
        <div class="rooms">
          <template v-for="room in config.rooms">
            <a :href="'/room/' + room.id">{{ room.escape_room_name }}</a>
          </template>
        </div>
    </div>
</template>

