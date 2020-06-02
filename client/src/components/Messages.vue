<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Messages</h1>
        <hr><br><br>
        <alert :message="msg"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.message-modal>
          New Message
          </button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Title</th>
              <th scope="col">Sender</th>
              <th scope="col">Receiver</th>
              <th scope="col">Content</th>
              <th scope="col">Created at</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
          <tr v-for="(message, index) in messages" :key="index">
                <td>{{ message.title }}</td>
                <td>{{ message.sender }}</td>
                <td>{{ message.receiver }}</td>
                <td>{{ message.message_body }}</td>
                <td>{{ message.creation_date }}</td>
                <td>
                <div class="btn-group" role="group">
                  <button
                    type="button"
                    class="btn btn-danger btn-sm"
                    v-on:click="onDeleteMessage(message)">
                      Delete
                  </button>
                </div>
                 </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="newMessageModal"
            id="message-modal"
            title="Send a new message"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-title-group"
                    label="Title:"
                    label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="text"
                        v-model="newMessageForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-receiver-group"
                      label="Receiver:"
                      label-for="form-receiver-input">
            <b-form-input id="form-receiver-input"
                          type="text"
                          v-model="newMessageForm.receiver"
                          required
                          placeholder="Enter receiver">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-message_body-group"
                      label="Message Content:"
                      label-for="form-message_body-input">
            <b-form-input id="form-message_body-input"
                          type="text"
                          v-model="newMessageForm.message_body"
                          required
                          placeholder="Enter Message Content">
            </b-form-input>
          </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  name: 'Messages',
  data() {
    return {
      token: '',
      messages: [],
      msg: '',
      showMessage: false,
      newMessageForm: {
        title: '',
        sender: '',
        receiver: '',
        message_body: '',
        creation_date: '',
      },
    };
  },
  methods: {
    isAuthenticate() {
      const token = localStorage.getItem('utoken');
      if (token) {
        this.token = token;
      }
    },
    getMessage() {
      const path = '/api/get_all';
      this.isAuthenticate();
      const config = {
        headers: {
          Authorization: `Bearer ${this.token}`,
        },
      };
      axios.get(path, config)
        .then((res) => {
          this.messages = res.data.messages;
          this.msg = res.data.msg;
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    newMessage(payload) {
      const path = '/api/write_message';
      this.isAuthenticate();
      const config = {
        headers: {
          Authorization: `Bearer ${this.token}`,
        },
      };
      axios.post(path, payload, config)
        .then((res) => {
          this.msg = res.data.msg;
          this.showMessage = true;
          this.getMessage();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getMessage();
        });
    },
    initForm() {
      this.newMessageForm.title = '';
      this.newMessageForm.sender = '';
      this.newMessageForm.receiver = '';
      this.newMessageForm.message_body = '';
      this.newMessageForm.creation_date = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.newMessageModal.hide();

      const payload = {
        title: this.newMessageForm.title,
        sender: this.newMessageForm.sender,
        receiver: this.newMessageForm.receiver,
        message_body: this.newMessageForm.message_body,
        creation_date: this.newMessageForm.creation_date,
      };
      this.newMessage(payload);
      this.initForm();
    },
    removeMessage(msgID) {
      const path = `/api/delete_message/${msgID}`;
      this.isAuthenticate();
      const config = {
        headers: {
          Authorization: `Bearer ${this.token}`,
        },
      };
      axios.delete(path, config)
        .then((res) => {
          this.showMessage = true;
          this.msg = res.data.msg;
          this.getMessage();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getMessage();
        });
    },
    onDeleteMessage(message) {
      this.removeMessage(message.msg_id);
    },
    onReset(evt) {
      evt.preventDefault();
      this.initForm();
    },
  },
  components: {
    alert: Alert,
  },
  created() {
    this.getMessage();
  },
};
</script>
