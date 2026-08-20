<script setup lang="ts">
import type { Note } from '@/types/note'
import { onMounted, ref } from 'vue'

const notes = ref<Note[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const response = await fetch('http://localhost:8000/api/notes/')
    if (!response.ok) {
      throw new Error(`Failed to fetch notes: ${response.status}`)
    }
    notes.value = await response.json()
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <v-list v-if="!loading && notes.length" lines="two">
    <v-list-item v-for="note in notes" :key="note.id" :title="note.title" :subtitle="note.body" />
  </v-list>

  <v-empty-state
    v-else-if="!loading"
    icon="mdi-note-outline"
    title="No notes yet"
    text="Create your first note to see it here."
  />
</template>
