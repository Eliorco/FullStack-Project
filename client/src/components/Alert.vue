<template>
  <div>
    <b-alert variant="success" v-if="showMessage">{{ message }}</b-alert>
    <br>
  </div>
</template>
<script>
export default {
  props: ['message', 'showMessage'],
};
</script>
