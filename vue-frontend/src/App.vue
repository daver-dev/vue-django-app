<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <v-app>
    <v-app-bar :elevation="2">
      <v-app-bar-title>Notes</v-app-bar-title>
      <v-btn :to="{ path: '/' }" variant="text">Home</v-btn>
      <v-btn :to="{ path: '/notes/new' }" variant="text">New Note</v-btn>
    </v-app-bar>

    <v-main>
      <v-container>
        <RouterView />
      </v-container>
    </v-main>
  </v-app>
</template>
