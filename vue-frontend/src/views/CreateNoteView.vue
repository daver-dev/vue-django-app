<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const form = ref()
const title = ref('')
const body = ref('')
const error = ref<string | null>(null)

const requiredRule = (v: string) => !!v || 'This field is required'

async function submitNote() {
  error.value = null

  const { valid } = await form.value.validate()
  if (!valid) return

  try {
    const response = await fetch('http://localhost:8000/api/notes/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: title.value, body: body.value }),
    })

    if (!response.ok) {
      throw new Error(`Failed to create note: ${response.status}`)
    }

    router.push('/')
  } catch (err) {
    error.value = 'Could not create note. Please try again.'
    console.error(err)
  }
}
</script>

<template>
  <v-row justify="center">
    <v-col cols="12" sm="8" md="6" lg="4">
      <v-card>
        <v-card-text>
          <v-form ref="form" @submit.prevent="submitNote">
            <v-text-field v-model="title" label="Title" :rules="[requiredRule]" />
            <v-textarea v-model="body" label="Body" :rules="[requiredRule]" />
            <v-alert v-if="error" type="error" density="compact" class="mb-4">{{ error }}</v-alert>
            <v-btn type="submit" color="primary" block>Create note</v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>
